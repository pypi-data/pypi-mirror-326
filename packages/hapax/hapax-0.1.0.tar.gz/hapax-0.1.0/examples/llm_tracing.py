"""Example demonstrating Hapax's observability system with LLM providers."""
from hapax.core import obs, set_default_log_level, LogLevel, get_metrics
import asyncio
import random
from typing import Optional

class MockLLMProvider:
    def __init__(self, name: str, failure_rate: float = 0.2):
        self.name = name
        self.failure_rate = failure_rate
    
    async def complete(self, prompt: str) -> str:
        if random.random() < self.failure_rate:
            raise Exception(f"{self.name} provider failed")
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate API latency
        return f"Response from {self.name}: {prompt}"

class LLMManager:
    def __init__(self):
        self.providers = {
            "openai": MockLLMProvider("openai"),
            "anthropic": MockLLMProvider("anthropic"),
            "cohere": MockLLMProvider("cohere")
        }
        self.current_provider = "openai"
    
    @obs(endpoint="/v1/completions")
    async def try_provider(self, provider: str, prompt: str) -> Optional[str]:
        try:
            return await self.providers[provider].complete(prompt)
        except Exception:
            return None
    
    @obs(name="llm_completion", endpoint="/v1/completions")
    async def complete_with_fallback(self, prompt: str) -> str:
        """Try multiple providers with fallback."""
        # Try primary provider first
        result = await self.try_provider(self.current_provider, prompt)
        if result:
            return result
        
        # Try fallback providers
        for provider in self.providers:
            if provider != self.current_provider:
                result = await self.try_provider(provider, prompt)
                if result:
                    self.current_provider = provider  # Switch to working provider
                    return result
        
        raise Exception("All providers failed")

async def main():
    # Set up logging and manager
    set_default_log_level(LogLevel.INFO)
    manager = LLMManager()
    
    # Process some prompts
    prompts = [
        "Tell me a joke",
        "Write a poem",
        "Explain quantum physics"
    ]
    
    for prompt in prompts:
        try:
            result = await manager.complete_with_fallback(prompt)
            print(f"\nPrompt: {prompt}")
            print(f"Result: {result}")
        except Exception as e:
            print(f"\nError processing prompt '{prompt}': {e}")
    
    # Print collected metrics
    print("\nMetrics collected:")
    for metric in get_metrics():
        print(f"\n{metric.name}")
        print(f"  Type: {metric.type}")
        print(f"  Value: {metric.value}")
        print(f"  Labels: {metric.labels}")

if __name__ == "__main__":
    asyncio.run(main())
