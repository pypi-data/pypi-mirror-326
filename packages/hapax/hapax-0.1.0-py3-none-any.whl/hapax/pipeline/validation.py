"""
Advanced validation system for Hapax pipelines.
Ensures type safety and compatibility of resource transformations.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Type, Set, TypeVar, Generic
import inspect
from types import GenericAlias
import typing
import asyncio
from enum import Enum

class ValidationLevel(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    level: ValidationLevel
    message: str
    resource_name: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TypeValidationContext:
    """Context for type validation across the pipeline."""
    input_types: Dict[str, Type]
    output_types: Dict[str, Type]
    dependencies: Dict[str, List[str]]
    type_constraints: Dict[str, List[Type]]

class TypeValidator:
    """Validates type compatibility between resources."""
    
    @staticmethod
    def get_type_hints(obj: Any) -> Dict[str, Type]:
        """Get type hints for an object, handling generics."""
        try:
            return typing.get_type_hints(obj)
        except Exception:
            return {}
    
    @staticmethod
    def is_compatible(source_type: Type, target_type: Type) -> bool:
        """Check if source type is compatible with target type."""
        # Handle Optional types
        if typing.get_origin(target_type) is typing.Union:
            target_args = typing.get_args(target_type)
            if type(None) in target_args:
                # It's an Optional[T], check compatibility with T
                target_type = next(t for t in target_args if t is not type(None))
        
        # Handle generic types
        if isinstance(source_type, GenericAlias) and isinstance(target_type, GenericAlias):
            source_origin = typing.get_origin(source_type)
            target_origin = typing.get_origin(target_type)
            if source_origin != target_origin:
                return False
            
            source_args = typing.get_args(source_type)
            target_args = typing.get_args(target_type)
            return all(
                TypeValidator.is_compatible(s, t)
                for s, t in zip(source_args, target_args)
            )
        
        # Handle subclass relationships
        try:
            return issubclass(source_type, target_type)
        except TypeError:
            # If types are not comparable, they're not compatible
            return False

class PipelineValidator:
    """Validates entire pipeline configuration and morphisms."""
    
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def add_issue(
        self,
        level: ValidationLevel,
        message: str,
        resource_name: Optional[str] = None,
        **details
    ):
        """Add a validation issue."""
        self.issues.append(ValidationIssue(
            level=level,
            message=message,
            resource_name=resource_name,
            details=details
        ))
    
    async def validate_resource_types(
        self,
        resource_definitions: Dict[str, Any],
        resources: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate resource type definitions and their usage."""
        for name, resource in resources.items():
            if resource.type not in resource_definitions:
                self.add_issue(
                    ValidationLevel.ERROR,
                    f"Unknown resource type: {resource.type}",
                    name
                )
                continue
            
            definition = resource_definitions[resource.type]
            
            # Validate config type
            config_type = self.get_config_type(definition)
            if config_type and not isinstance(resource.config, config_type):
                self.add_issue(
                    ValidationLevel.ERROR,
                    f"Invalid config type. Expected {config_type}, got {type(resource.config)}",
                    name
                )
    
    async def validate_morphisms(
        self,
        resources: Dict[str, Any],
        resource_definitions: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate morphisms between resources."""
        context = self.build_validation_context(resources, resource_definitions)
        
        for name, resource in resources.items():
            # Check each dependency
            for dep_name in resource.depends_on:
                if dep_name not in resources:
                    self.add_issue(
                        ValidationLevel.ERROR,
                        f"Missing dependency: {dep_name}",
                        name
                    )
                    continue
                
                # Validate type compatibility
                if dep_name in context.output_types and name in context.input_types:
                    source_type = context.output_types[dep_name]
                    target_type = context.input_types[name]
                    
                    if not TypeValidator.is_compatible(source_type, target_type):
                        self.add_issue(
                            ValidationLevel.ERROR,
                            "Type mismatch between resources",
                            name,
                            source=dep_name,
                            source_type=str(source_type),
                            target_type=str(target_type)
                        )
    
    async def validate_cycles(self, resources: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate that there are no cycles in the dependency graph."""
        visited = set()
        temp = set()
        
        async def visit(name: str, path: List[str]) -> bool:
            if name in temp:
                cycle = path[path.index(name):] + [name]
                self.add_issue(
                    ValidationLevel.ERROR,
                    f"Circular dependency detected: {' -> '.join(cycle)}",
                    name,
                    cycle=cycle
                )
                return False
            
            if name in visited:
                return True
            
            temp.add(name)
            path.append(name)
            
            resource = resources[name]
            for dep in resource.depends_on:
                if not await visit(dep, path):
                    return False
            
            temp.remove(name)
            visited.add(name)
            path.pop()
            return True
        
        for name in resources:
            if name not in visited:
                await visit(name, [])
    
    @staticmethod
    def build_validation_context(
        resources: Dict[str, Any],
        resource_definitions: Dict[str, Any]
    ) -> TypeValidationContext:
        """Build context for type validation."""
        context = TypeValidationContext(
            input_types={},
            output_types={},
            dependencies={},
            type_constraints={}
        )
        
        for name, resource in resources.items():
            definition = resource_definitions.get(resource.type)
            if not definition:
                continue
            
            # Get input/output types from resource definition
            type_hints = TypeValidator.get_type_hints(definition)
            if "config" in type_hints:
                context.input_types[name] = type_hints["config"]
            if "state" in type_hints:
                context.output_types[name] = type_hints["state"]
            
            context.dependencies[name] = resource.depends_on
        
        return context
    
    @staticmethod
    def get_config_type(definition: Any) -> Optional[Type]:
        """Get the configuration type for a resource definition."""
        if hasattr(definition, "__orig_bases__"):
            for base in definition.__orig_bases__:
                if hasattr(base, "__args__"):
                    return base.__args__[0]
        return None
    
    async def validate_pipeline(
        self,
        resources: Dict[str, Any],
        resource_definitions: Dict[str, Any]
    ) -> List[ValidationIssue]:
        """Validate the entire pipeline."""
        self.issues = []
        
        # Run all validations
        await asyncio.gather(
            self.validate_resource_types(resource_definitions, resources),
            self.validate_morphisms(resources, resource_definitions),
            self.validate_cycles(resources)
        )
        
        return self.issues

def format_validation_issues(issues: List[ValidationIssue]) -> str:
    """Format validation issues into a readable string."""
    if not issues:
        return "Pipeline validation successful! No issues found."
    
    result = []
    for level in ValidationLevel:
        level_issues = [i for i in issues if i.level == level]
        if level_issues:
            result.append(f"\n{level.upper()}S:")
            for issue in level_issues:
                msg = f"- {issue.message}"
                if issue.resource_name:
                    msg = f"[{issue.resource_name}] {msg}"
                if issue.details:
                    msg += f"\n  Details: {issue.details}"
                result.append(msg)
    
    return "\n".join(result)
