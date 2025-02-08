"""
Pipeline system for Hapax, inspired by Terraform's declarative approach
and integrated with OpenLLMetry for standardized tracing.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Type, Callable
import yaml
from enum import Enum
import inspect
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import asyncio

class ResourceType(str, Enum):
    LLM = "llm"
    VECTORDB = "vectordb"
    MEMORY = "memory"
    CHAIN = "chain"
    TOOL = "tool"

@dataclass
class Resource:
    type: ResourceType
    name: str
    provider: str
    config: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Pipeline:
    name: str
    resources: Dict[str, Resource] = field(default_factory=dict)
    _graph: Dict[str, List[str]] = field(default_factory=dict)
    
    def add_resource(self, resource: Resource):
        """Add a resource to the pipeline."""
        self.resources[resource.name] = resource
        self._graph[resource.name] = resource.depends_on
    
    async def validate(self) -> bool:
        """Validate the pipeline configuration."""
        # Check for circular dependencies
        visited = set()
        temp = set()
        
        async def visit(node: str) -> bool:
            if node in temp:
                return False  # Circular dependency
            if node in visited:
                return True
            
            temp.add(node)
            for dep in self._graph.get(node, []):
                if not await visit(dep):
                    return False
            temp.remove(node)
            visited.add(node)
            return True
        
        for node in self._graph:
            if not await visit(node):
                raise ValueError(f"Circular dependency detected in pipeline {self.name}")
        
        return True
    
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
    def __init__(self):
        self.pipelines: Dict[str, Pipeline] = {}
        self.resource_handlers: Dict[ResourceType, Dict[str, Callable]] = {
            rt: {} for rt in ResourceType
        }
        
        # Initialize OpenTelemetry tracer
        self.tracer = trace.get_tracer(__name__)
    
    def register_handler(
        self,
        resource_type: ResourceType,
        provider: str,
        handler: Callable
    ):
        """Register a handler for a specific resource type and provider."""
        self.resource_handlers[resource_type][provider] = handler
    
    async def apply_resource(self, resource: Resource) -> Dict[str, Any]:
        """Apply a single resource with tracing."""
        handler = self.resource_handlers[resource.type].get(resource.provider)
        if not handler:
            raise ValueError(
                f"No handler for {resource.type} provider {resource.provider}"
            )
        
        with self.tracer.start_as_current_span(
            f"apply_{resource.type}_{resource.name}"
        ) as span:
            try:
                span.set_attribute("resource.name", resource.name)
                span.set_attribute("resource.type", resource.type)
                span.set_attribute("resource.provider", resource.provider)
                
                if inspect.iscoroutinefunction(handler):
                    result = await handler(resource.config)
                else:
                    result = handler(resource.config)
                
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
    
    async def apply(self, pipeline: Pipeline) -> Dict[str, Any]:
        """Apply a pipeline configuration."""
        with self.tracer.start_as_current_span(f"apply_pipeline_{pipeline.name}") as span:
            try:
                # Validate pipeline
                await pipeline.validate()
                
                # Get execution order
                stages = pipeline.get_execution_order()
                
                # Execute stages in order
                results = {}
                for stage in stages:
                    # Execute resources in this stage in parallel
                    tasks = []
                    for resource_name in stage:
                        resource = pipeline.resources[resource_name]
                        task = asyncio.create_task(self.apply_resource(resource))
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

    @classmethod
    def from_yaml(cls, yaml_content: str) -> Pipeline:
        """Create a pipeline from YAML configuration."""
        config = yaml.safe_load(yaml_content)
        pipeline = Pipeline(name=config["name"])
        
        for resource_config in config.get("resources", []):
            resource = Resource(
                type=ResourceType(resource_config["type"]),
                name=resource_config["name"],
                provider=resource_config["provider"],
                config=resource_config.get("config", {}),
                depends_on=resource_config.get("depends_on", [])
            )
            pipeline.add_resource(resource)
        
        return pipeline
