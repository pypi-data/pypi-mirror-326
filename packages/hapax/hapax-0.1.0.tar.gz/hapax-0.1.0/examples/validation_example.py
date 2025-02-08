"""Example demonstrating Hapax's advanced pipeline validation."""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import asyncio
from hapax.pipeline.base import (
    ResourceDefinition,
    ValidationIssue,
    Pipeline,
    Resource,
    PipelineManager
)
from hapax.pipeline.validation import ValidationLevel

# Define strongly typed configurations and states
@dataclass
class TextProcessorConfig:
    input_format: str
    transformations: List[str]

@dataclass
class TextProcessorState:
    output_text: str
    format: str

@dataclass
class StorageConfig:
    path: str
    format: str  # Must match TextProcessor's output format

@dataclass
class StorageState:
    stored_items: int
    total_size: int

# Define resource types with strong validation
class TextProcessorResource(ResourceDefinition[TextProcessorConfig, TextProcessorState]):
    @property
    def type_name(self) -> str:
        return "text_processor"
    
    async def validate_config(self, config: TextProcessorConfig) -> Optional[ValidationIssue]:
        if not config.transformations:
            return ValidationIssue(
                level=ValidationLevel.ERROR,
                message="At least one transformation must be specified",
                details={"transformations": config.transformations}
            )
        
        valid_formats = ["txt", "json", "xml"]
        if config.input_format not in valid_formats:
            return ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"Invalid input format. Must be one of: {valid_formats}",
                details={"format": config.input_format}
            )
        
        return None
    
    async def plan(self, config: TextProcessorConfig, current_state: Optional[TextProcessorState] = None) -> List[str]:
        return [f"Apply transformation: {t}" for t in config.transformations]
    
    async def apply(self, config: TextProcessorConfig) -> TextProcessorState:
        # Simulate processing
        await asyncio.sleep(0.1)
        return TextProcessorState(
            output_text="processed text",
            format=config.input_format
        )

class StorageResource(ResourceDefinition[StorageConfig, StorageState]):
    @property
    def type_name(self) -> str:
        return "storage"
    
    async def validate_config(self, config: StorageConfig) -> Optional[ValidationIssue]:
        if not config.path.startswith("/"):
            return ValidationIssue(
                level=ValidationLevel.ERROR,
                message="Storage path must be absolute",
                details={"path": config.path}
            )
        
        valid_formats = ["txt", "json", "xml"]
        if config.format not in valid_formats:
            return ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"Invalid storage format. Must be one of: {valid_formats}",
                details={"format": config.format}
            )
        
        return None
    
    async def plan(self, config: StorageConfig, current_state: Optional[StorageState] = None) -> List[str]:
        return [f"Initialize storage at {config.path}"]
    
    async def apply(self, config: StorageConfig) -> StorageState:
        # Simulate storage
        await asyncio.sleep(0.1)
        return StorageState(
            stored_items=1,
            total_size=1024
        )

async def main():
    # Create pipeline manager
    manager = PipelineManager()
    
    # Register resource types
    manager.register_resource_type(TextProcessorResource())
    manager.register_resource_type(StorageResource())
    
    # Create a pipeline with type mismatches to demonstrate validation
    pipeline = Pipeline("validation_test")
    
    # Add text processor
    processor = Resource(
        name="processor",
        type="text_processor",
        config=TextProcessorConfig(
            input_format="json",
            transformations=["normalize"]
        )
    )
    pipeline.add_resource(processor)
    
    # Add storage with mismatched format (will cause validation error)
    storage = Resource(
        name="storage",
        type="storage",
        config=StorageConfig(
            path="/data/output",
            format="csv"  # This will fail validation
        ),
        depends_on=["processor"]
    )
    pipeline.add_resource(storage)
    
    try:
        # Try to validate the pipeline
        print("Validating pipeline...")
        issues = await manager.validate_pipeline(pipeline)
        
        # This won't be reached if there are errors
        print("\nValidation successful!")
        if issues:
            print("\nWarnings:")
            for issue in issues:
                print(f"- {issue.message}")
        
        # Try to apply the pipeline
        print("\nApplying pipeline...")
        results = await manager.apply(pipeline)
        print("\nResults:", results)
    
    except ValueError as e:
        print(f"\nValidation failed:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
