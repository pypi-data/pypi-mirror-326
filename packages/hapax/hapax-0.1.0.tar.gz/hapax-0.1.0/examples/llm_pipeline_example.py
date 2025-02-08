"""Example of a type-safe LLM pipeline using Qwen model.

This example demonstrates how to build a proper, type-safe pipeline for LLM inference
with proper validation at each step. It shows:

1. How to define proper types for each step
2. How to validate inputs and outputs
3. How to handle errors gracefully
4. How to add observability
5. How to make the pipeline extensible
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from hapax.workflow import Workflow, validate_workflow
from hapax.pipeline import Pipeline, PipelineResource, ResourceConfig, ResourceState

@dataclass
class PromptConfig:
    """Configuration for prompt construction."""
    system_prompt: str
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9

@dataclass
class QwenConfig(ResourceConfig):
    """Configuration for Qwen model."""
    model_name: str = "Qwen/Qwen2.5-7B-Instruct-1M"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    max_length: int = 2048
    prompt_config: PromptConfig = PromptConfig(
        system_prompt="You are a helpful AI assistant."
    )

@dataclass
class QwenState(ResourceState):
    """State of the Qwen model resource."""
    model: Optional[AutoModelForCausalLM] = None
    tokenizer: Optional[AutoTokenizer] = None

class QwenResource(PipelineResource[QwenConfig, QwenState]):
    """Resource for managing Qwen model lifecycle."""
    
    def type_name(self) -> str:
        return "qwen"
    
    def validate_config(self, config: QwenConfig) -> None:
        """Validate the configuration."""
        if config.max_length > 4096:
            raise ValueError("max_length cannot exceed 4096")
        if not (0 <= config.prompt_config.temperature <= 1.0):
            raise ValueError("temperature must be between 0 and 1")
        if not (0 <= config.prompt_config.top_p <= 1.0):
            raise ValueError("top_p must be between 0 and 1")
    
    def plan(self, config: QwenConfig, current_state: Optional[QwenState] = None) -> List[str]:
        """Plan the changes needed."""
        changes = []
        if not current_state or not current_state.model:
            changes.append(f"Load Qwen model {config.model_name}")
        return changes
    
    def apply(self, config: QwenConfig) -> QwenState:
        """Apply the configuration and return the new state."""
        tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            config.model_name,
            device_map=config.device,
            torch_dtype=torch.float16
        )
        return QwenState(model=model, tokenizer=tokenizer)

def validate_input(user_input: str) -> str:
    """Validate and clean user input."""
    if not user_input.strip():
        raise ValueError("Input cannot be empty")
    return user_input.strip()

def construct_prompt(
    user_input: str,
    config: PromptConfig
) -> str:
    """Construct a prompt following Qwen's format."""
    return f"""<|im_start|>system
{config.system_prompt}
<|im_end|>
<|im_start|>user
{user_input}
<|im_end|>
<|im_start|>assistant
"""

def generate_response(
    prompt: str,
    state: QwenState,
    config: QwenConfig
) -> str:
    """Generate response from the model."""
    inputs = state.tokenizer(prompt, return_tensors="pt").to(config.device)
    outputs = state.model.generate(
        **inputs,
        max_length=config.max_length,
        temperature=config.prompt_config.temperature,
        top_p=config.prompt_config.top_p,
        pad_token_id=state.tokenizer.pad_token_id,
    )
    response = state.tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<|im_start|>assistant")[-1].strip()

def validate_output(response: str) -> Dict[str, Any]:
    """Validate and structure the model output."""
    if not response.strip():
        raise ValueError("Model produced empty response")
    
    return {
        "response": response,
        "length": len(response),
        "status": "success"
    }

def create_llm_workflow(config: QwenConfig, state: QwenState) -> Workflow:
    """Create a workflow for LLM inference with proper validation."""
    workflow = Workflow()
    
    # Add each step with proper type annotations
    workflow.add(validate_input)
    workflow.add(lambda x: construct_prompt(x, config.prompt_config))
    workflow.add(lambda x: generate_response(x, state, config))
    workflow.add(validate_output)
    
    # Validate the workflow before returning
    validate_workflow(workflow)
    return workflow

def main():
    """Run the example pipeline."""
    # Create and configure the pipeline
    pipeline = Pipeline()
    
    # Add Qwen resource with configuration
    config = QwenConfig(
        prompt_config=PromptConfig(
            system_prompt="You are a helpful AI assistant that provides concise answers.",
            max_length=1024,
            temperature=0.7
        )
    )
    
    pipeline.add_resource("qwen", QwenResource(), config)
    
    # Apply the pipeline to initialize resources
    pipeline.validate()  # This will catch any configuration errors
    pipeline.apply()
    
    # Get the initialized state
    state = pipeline.get_resource_state("qwen", QwenState)
    
    # Create the workflow
    workflow = create_llm_workflow(config, state)
    
    # Example usage with error handling
    try:
        user_input = "What is the capital of France?"
        result = workflow.run(user_input, trace=True)
        print(f"Input: {user_input}")
        print(f"Output: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
