"""Example usage of Hapax observability system."""
from hapax.core import obs

@obs("process_text", input_type="text")
def process_text(text: str) -> str:
    return text.upper()

@obs()  # Uses function name as span name
def nested_operation():
    result = process_text("hello world")
    return result

if __name__ == "__main__":
    # Example of using the tracing system
    result = nested_operation()
    print(f"Result: {result}")
    
    # Access trace information
    from hapax.core import get_trace_context
    
    context = get_trace_context()
    for span_id, span in context.spans.items():
        print(f"\nSpan: {span.name}")
        print(f"ID: {span.id}")
        print(f"Parent ID: {span.parent_id}")
        print(f"Duration: {(span.end_time - span.start_time) * 1000:.2f}ms")
        print(f"Attributes: {span.attributes}")
