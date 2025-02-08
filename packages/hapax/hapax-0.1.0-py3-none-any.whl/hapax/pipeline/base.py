"""
Base classes for Hapax's extensible pipeline system.
Allows users to define their own resource types and validation rules.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Type, TypeVar, Generic, get_type_hints
import asyncio
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from .validation import PipelineValidator, ValidationIssue, ValidationLevel, format_validation_issues

T = TypeVar('T')  # Type for resource configuration
S = TypeVar('S')  # Type for resource state

@dataclass
class ValidationResult:
    """Result of a resource validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class ResourceDefinition(ABC, Generic[T, S]):
    """Base class for defining custom resource types."""
    
    @property
    @abstractmethod
    def type_name(self) -> str:
        """The unique name of this resource type."""
        pass
    
    @abstractmethod
    async def validate_config(self, config: T) -> ValidationIssue:
        """
        Validate the resource configuration.
        
        Args:
            config: The configuration to validate
            
        Returns:
            ValidationIssue indicating if the config is valid
        """
        pass
    
    @abstractmethod
    async def plan(self, config: T, current_state: Optional[S] = None) -> List[str]:
        """
        Plan the changes needed to reach desired state.
        
        Args:
            config: The desired configuration
            current_state: The current state (if any)
            
        Returns:
            List of planned changes
        """
        pass
    
    @abstractmethod
    async def apply(self, config: T) -> S:
        """
        Apply the configuration and return the new state.
        
        Args:
            config: The configuration to apply
            
        Returns:
            The new state after applying changes
        """
        pass
    
    def get_input_type(self) -> Optional[Type]:
        """Get the input type for this resource."""
        hints = get_type_hints(self.__class__)
        return hints.get("config")
    
    def get_output_type(self) -> Optional[Type]:
        """Get the output type for this resource."""
        hints = get_type_hints(self.__class__)
        return hints.get("state")

@dataclass
class Resource(Generic[T, S]):
    """A resource instance in the pipeline."""
    name: str
    type: str
    config: T
    depends_on: List[str] = field(default_factory=list)
    state: Optional[S] = None

@dataclass
class Pipeline:
    """A pipeline of resources with dependencies."""
    name: str
    resources: Dict[str, Resource] = field(default_factory=dict)
    _graph: Dict[str, List[str]] = field(default_factory=dict)
    _validator: PipelineValidator = field(default_factory=PipelineValidator)
    
    def add_resource(self, resource: Resource):
        """Add a resource to the pipeline."""
        self.resources[resource.name] = resource
        self._graph[resource.name] = resource.depends_on
    
    async def validate(self, resource_definitions: Dict[str, ResourceDefinition]) -> List[ValidationIssue]:
        """
        Validate the pipeline configuration.
        
        This performs comprehensive validation including:
        - Resource type validation
        - Morphism compatibility
        - Dependency cycle detection
        - Individual resource configuration validation
        
        Args:
            resource_definitions: Dictionary of available resource definitions
            
        Returns:
            List of validation issues found
        
        Raises:
            ValueError: If validation fails with errors
        """
        # Perform pipeline-level validation
        issues = await self._validator.validate_pipeline(
            self.resources,
            resource_definitions
        )
        
        # Perform individual resource validation
        for name, resource in self.resources.items():
            definition = resource_definitions.get(resource.type)
            if definition:
                result = await definition.validate_config(resource.config)
                if result:
                    issues.append(result)
        
        # If there are any errors, raise with formatted message
        errors = [i for i in issues if i.level == ValidationLevel.ERROR]
        if errors:
            raise ValueError(
                f"Pipeline validation failed:\n{format_validation_issues(issues)}"
            )
        
        return issues
    
    def get_execution_order(self) -> List[List[str]]:
        """Get the execution order of resources in parallel stages."""
        executed = set()
        stages = []
        
        while len(executed) < len(self.resources):
            stage = []
            for name, resource in self.resources.items():
                if name not in executed and all(dep in executed for dep in resource.depends_on):
                    stage.append(name)
            if not stage:
                raise ValueError("Unable to resolve dependencies")
            stages.append(stage)
            executed.update(stage)
        
        return stages

class PipelineManager:
    """Manages pipeline execution and resource definitions."""
    
    def __init__(self):
        self.resource_definitions: Dict[str, ResourceDefinition] = {}
        self.tracer = trace.get_tracer(__name__)
    
    def register_resource_type(self, definition: ResourceDefinition):
        """Register a new resource type."""
        self.resource_definitions[definition.type_name] = definition
    
    async def validate_pipeline(self, pipeline: Pipeline) -> List[ValidationIssue]:
        """Validate an entire pipeline."""
        return await pipeline.validate(self.resource_definitions)
    
    async def plan(self, pipeline: Pipeline) -> Dict[str, List[str]]:
        """Plan changes for all resources in the pipeline."""
        # Validate before planning
        await self.validate_pipeline(pipeline)
        
        plans = {}
        for resource in pipeline.resources.values():
            definition = self.resource_definitions.get(resource.type)
            if not definition:
                continue
            
            with self.tracer.start_as_current_span(f"plan_{resource.name}") as span:
                try:
                    changes = await definition.plan(resource.config, resource.state)
                    plans[resource.name] = changes
                    span.set_status(Status(StatusCode.OK))
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        
        return plans
    
    async def apply(self, pipeline: Pipeline) -> Dict[str, Any]:
        """Apply a pipeline configuration."""
        with self.tracer.start_as_current_span(f"apply_pipeline_{pipeline.name}") as span:
            try:
                # Validate pipeline before applying
                await self.validate_pipeline(pipeline)
                
                # Get execution order
                stages = pipeline.get_execution_order()
                
                # Execute stages in order
                results = {}
                for stage in stages:
                    # Execute resources in this stage in parallel
                    tasks = []
                    for resource_name in stage:
                        resource = pipeline.resources[resource_name]
                        definition = self.resource_definitions[resource.type]
                        
                        task = asyncio.create_task(
                            self._apply_resource(resource, definition)
                        )
                        tasks.append((resource_name, task))
                    
                    # Wait for all resources in this stage
                    for resource_name, task in tasks:
                        try:
                            results[resource_name] = await task
                        except Exception as e:
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                            raise ValueError(
                                f"Failed to apply resource {resource_name}: {e}"
                            )
                
                span.set_status(Status(StatusCode.OK))
                return results
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
    
    async def _apply_resource(
        self,
        resource: Resource,
        definition: ResourceDefinition
    ) -> Any:
        """Apply a single resource with tracing."""
        with self.tracer.start_as_current_span(
            f"apply_{resource.type}_{resource.name}"
        ) as span:
            try:
                span.set_attribute("resource.name", resource.name)
                span.set_attribute("resource.type", resource.type)
                
                result = await definition.apply(resource.config)
                resource.state = result
                
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_attribute("error", str(e))
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
