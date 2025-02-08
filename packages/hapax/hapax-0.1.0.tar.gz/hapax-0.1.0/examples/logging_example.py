"""Example demonstrating Hapax's logging capabilities."""
from hapax.core import obs, set_default_log_level, LogLevel

# Set default log level for all spans
set_default_log_level(LogLevel.INFO)

@obs(log_level="DEBUG")  # Override with DEBUG level
def process_data(data: str) -> str:
    return data.upper()

@obs(log_level=LogLevel.WARNING)  # Using enum directly
def risky_operation():
    # This will inherit WARNING level
    return process_data("warning test")

@obs()  # Will inherit parent's log level or default INFO
def nested_operation():
    # This span will have INFO level
    result1 = process_data("hello")  # This span will have DEBUG level
    
    # This span will have WARNING level
    result2 = risky_operation()
    
    return result1, result2

@obs(log_level="ERROR")
def failing_operation():
    raise ValueError("Something went wrong!")

if __name__ == "__main__":
    # Configure loguru format to show trace context
    from loguru import logger
    
    # Add custom format with trace context
    logger.remove()
    logger.add(
        lambda msg: print(msg),
        format="<level>{level}</level> | <cyan>{extra[span_id]}</cyan> "
        "| <yellow>parent={extra[parent_id]}</yellow> | {message}",
    )
    
    try:
        # Run operations with different log levels
        results = nested_operation()
        print("\nResults:", results)
        
        # This will generate an error log
        failing_operation()
    except Exception as e:
        print(f"\nCaught error: {e}")
