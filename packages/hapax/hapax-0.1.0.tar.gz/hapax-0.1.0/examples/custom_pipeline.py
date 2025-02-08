"""Example of creating custom resource types in Hapax's pipeline system."""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import asyncio
from hapax.pipeline.base import (
    ResourceDefinition,
    ValidationResult,
    Pipeline,
    Resource,
    PipelineManager
)

# Example: Custom HTTP Endpoint Resource
@dataclass
class EndpointConfig:
    url: str
    method: str = "GET"
    headers: Dict[str, str] = None
    body: Dict[str, Any] = None

@dataclass
class EndpointState:
    last_status: int
    response_time: float
    is_healthy: bool

class HTTPEndpointResource(ResourceDefinition[EndpointConfig, EndpointState]):
    @property
    def type_name(self) -> str:
        return "http_endpoint"
    
    async def validate_config(self, config: EndpointConfig) -> ValidationResult:
        errors = []
        warnings = []
        
        if not config.url.startswith(("http://", "https://")):
            errors.append("URL must start with http:// or https://")
        
        if config.method not in ["GET", "POST", "PUT", "DELETE"]:
            errors.append("Invalid HTTP method")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def plan(
        self,
        config: EndpointConfig,
        current_state: Optional[EndpointState] = None
    ) -> List[str]:
        changes = []
        
        if not current_state:
            changes.append(f"Create new endpoint monitoring for {config.url}")
        elif current_state and not current_state.is_healthy:
            changes.append(f"Retry unhealthy endpoint {config.url}")
        
        return changes
    
    async def apply(self, config: EndpointConfig) -> EndpointState:
        # Simulate HTTP request
        await asyncio.sleep(0.1)  # Simulate network delay
        return EndpointState(
            last_status=200,
            response_time=0.1,
            is_healthy=True
        )

# Example: Custom Data Processor Resource
@dataclass
class ProcessorConfig:
    input_format: str
    output_format: str
    transformations: List[str]

@dataclass
class ProcessorState:
    processed_items: int
    last_run: float
    status: str

class DataProcessorResource(ResourceDefinition[ProcessorConfig, ProcessorState]):
    @property
    def type_name(self) -> str:
        return "data_processor"
    
    async def validate_config(self, config: ProcessorConfig) -> ValidationResult:
        errors = []
        warnings = []
        
        supported_formats = ["json", "csv", "xml"]
        if config.input_format not in supported_formats:
            errors.append(f"Input format must be one of {supported_formats}")
        if config.output_format not in supported_formats:
            errors.append(f"Output format must be one of {supported_formats}")
        
        if not config.transformations:
            warnings.append("No transformations specified")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def plan(
        self,
        config: ProcessorConfig,
        current_state: Optional[ProcessorState] = None
    ) -> List[str]:
        changes = []
        
        if not current_state:
            changes.append("Initialize new data processor")
        else:
            changes.append("Update existing processor configuration")
        
        return changes
    
    async def apply(self, config: ProcessorConfig) -> ProcessorState:
        # Simulate processing
        await asyncio.sleep(0.2)
        return ProcessorState(
            processed_items=100,
            last_run=0.2,
            status="completed"
        )

async def main():
    # Create pipeline manager
    manager = PipelineManager()
    
    # Register custom resource types
    manager.register_resource_type(HTTPEndpointResource())
    manager.register_resource_type(DataProcessorResource())
    
    # Create a pipeline with custom resources
    pipeline = Pipeline("custom_pipeline")
    
    # Add an HTTP endpoint resource
    endpoint = Resource(
        name="api_endpoint",
        type="http_endpoint",
        config=EndpointConfig(
            url="https://api.example.com/data",
            method="POST",
            headers={"Content-Type": "application/json"}
        )
    )
    pipeline.add_resource(endpoint)
    
    # Add a data processor that depends on the endpoint
    processor = Resource(
        name="data_transformer",
        type="data_processor",
        config=ProcessorConfig(
            input_format="json",
            output_format="csv",
            transformations=["normalize", "validate"]
        ),
        depends_on=["api_endpoint"]
    )
    pipeline.add_resource(processor)
    
    try:
        # Validate the pipeline
        validation = await manager.validate_pipeline(pipeline)
        if validation.warnings:
            print("\nWarnings:")
            for warning in validation.warnings:
                print(f"- {warning}")
        
        if not validation.is_valid:
            print("\nValidation failed:")
            for error in validation.errors:
                print(f"- {error}")
            return
        
        # Show planned changes
        print("\nPlanned changes:")
        plans = await manager.plan(pipeline)
        for resource_name, changes in plans.items():
            print(f"\n{resource_name}:")
            for change in changes:
                print(f"- {change}")
        
        # Apply the pipeline
        print("\nApplying pipeline...")
        results = await manager.apply(pipeline)
        
        print("\nResults:")
        for resource_name, state in results.items():
            print(f"\n{resource_name}:")
            print(f"State: {state}")
    
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
