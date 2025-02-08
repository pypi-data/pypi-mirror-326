"""Core workflow system with validation and tracing."""
from typing import Any, Callable, List, Optional, Union, get_args, get_origin, TypeVar, GenericAlias
from dataclasses import dataclass, field
import inspect
import asyncio
import time
import os
import types
from opentelemetry import trace as telemetry
from opentelemetry.trace import Status, StatusCode
from ..observability.llm import LLMTracer

Input = TypeVar('Input')
Output = TypeVar('Output')

def is_compatible_type(output_type: Any, input_type: Any, *, is_return_type: bool = False) -> bool:
    """Check if output_type is compatible with input_type.
    
    For function parameters (is_return_type=False), we use contravariance:
    - If a function accepts type T, it can accept any supertype of T
    
    For return types (is_return_type=True), we use covariance:
    - If a function returns type T, it can return any subtype of T
    """
    # Handle inspect._empty (unspecified type annotations)
    if output_type == inspect._empty or input_type == inspect._empty:
        return True

    # Handle Any type
    if input_type == Any or output_type == Any:
        return True
    
    # Handle Optional types
    if get_origin(input_type) == Union:
        input_args = get_args(input_type)
        if type(None) in input_args:
            # If input is Optional[T], output must be T or Optional[T]
            non_none_type = next(t for t in input_args if t is not type(None))
            if get_origin(output_type) == Union:
                output_args = get_args(output_type)
                if type(None) in output_args:
                    # Both are Optional, check the non-None types
                    output_non_none = next(t for t in output_args if t is not type(None))
                    return is_compatible_type(output_non_none, non_none_type, is_return_type=is_return_type)
            # Check if output type is compatible with the non-None input type
            return is_compatible_type(output_type, non_none_type, is_return_type=is_return_type)

    # Handle generic types
    if isinstance(output_type, GenericAlias) and isinstance(input_type, GenericAlias):
        output_origin = get_origin(output_type)
        input_origin = get_origin(input_type)
        if output_origin != input_origin:
            return False
        
        output_args = get_args(output_type)
        input_args = get_args(input_type)
        if len(output_args) != len(input_args):
            return False
        
        # For each type argument, check compatibility with appropriate variance
        return all(
            is_compatible_type(o, i, is_return_type=is_return_type)
            for o, i in zip(output_args, input_args)
        )

    # Handle subclass relationships for regular types
    try:
        if is_return_type:
            # For return types (covariance), output_type should be a subtype of input_type
            return issubclass(output_type, input_type)
        else:
            # For parameter types (contravariance), input_type should be a subtype of output_type
            return issubclass(input_type, output_type)
    except TypeError:
        # If issubclass fails (e.g., with special types), fall back to equality
        return output_type == input_type

def validate_callable(func: Callable) -> None:
    """Validate a callable's signature and attributes."""
    # Get the actual function for bound methods
    if inspect.ismethod(func):
        actual_func = func.__func__
        sig = inspect.signature(actual_func)
    else:
        actual_func = func
        sig = inspect.signature(actual_func)
    
    # Must have exactly one parameter (excluding self for methods)
    params = list(sig.parameters.values())
    
    # Handle methods by removing self/cls
    if inspect.ismethod(func) or isinstance(func, types.MethodType):
        params = params[1:]  # Remove 'self'
    elif inspect.isfunction(actual_func) and hasattr(actual_func, '__qualname__'):
        # Handle staticmethod and classmethod
        if 'staticmethod' in actual_func.__qualname__ or 'classmethod' in actual_func.__qualname__:
            if len(params) > 0 and params[0].name in ('self', 'cls'):
                params = params[1:]
    
    # Handle *args
    if any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params):
        raise ValueError(
            f"Function {actual_func.__name__} cannot use *args, "
            f"must take exactly one parameter"
        )
    
    # Must have exactly one parameter
    if len(params) != 1:
        raise ValueError(
            f"Function {actual_func.__name__} must take exactly one parameter, "
            f"got {len(params)}: {[p.name for p in params]}"
        )
    
    # Must have type hints
    first_param = params[0]
    if first_param.annotation == inspect.Parameter.empty:
        raise ValueError(
            f"Function {actual_func.__name__} parameter {first_param.name} "
            f"must have a type hint"
        )
    
    if sig.return_annotation == inspect.Parameter.empty:
        raise ValueError(
            f"Function {actual_func.__name__} must have a return type hint"
        )

@dataclass
class Step:
    """A step in a workflow."""
    func: Callable
    name: Optional[str] = None

    def __post_init__(self):
        """Validate the step after initialization."""
        if not isinstance(self.func, types.LambdaType):
            validate_callable(self.func)
        if self.name is None:
            self.name = getattr(self.func, '__name__', 'anonymous')

    async def execute(self, input_data: Any) -> Any:
        """Execute the step with the given input data."""
        result = self.func(input_data)
        if asyncio.iscoroutine(result):
            return await result
        return result

    @property
    def func_name(self) -> str:
        """Return the name of the function for tracing."""
        return self.name

@dataclass
class Workflow:
    """A workflow that executes steps in sequence."""
    steps: List[Union['Step', 'ParallelStep', 'ConditionalStep']] = field(default_factory=list)
    _tracer: Optional[LLMTracer] = field(default=None, init=False)
    
    def __post_init__(self):
        """Initialize the tracer."""
        self._tracer = LLMTracer("workflow")
    
    def add(self, func: Union[Callable, 'ParallelStep', 'ConditionalStep']) -> 'Workflow':
        """Add a step to the workflow."""
        if isinstance(func, (ParallelStep, ConditionalStep)):
            self.steps.append(func)
        else:
            self.steps.append(Step(func))
        return self
    
    def map(self, funcs: List[Callable]) -> 'Workflow':
        """Add a parallel step to the workflow."""
        self.steps.append(ParallelStep(funcs))
        return self
    
    def when(self, condition: Callable[[Any], bool], *, then: Callable[['Workflow'], 'Workflow'], else_: Optional[Callable[['Workflow'], 'Workflow']] = None) -> 'Workflow':
        """Add a conditional step to the workflow."""
        then_branch = Workflow()
        then(then_branch)
        
        else_branch = None
        if else_:
            else_branch = Workflow()
            else_(else_branch)
        
        self.steps.append(ConditionalStep(condition, then_branch, else_branch))
        return self
    
    async def run(self, input_data: Any, trace: bool = False) -> Any:
        """Execute the workflow with the given input."""
        validate_workflow(self)
        
        if trace:
            tracer = telemetry.get_tracer(__name__)
            with tracer.start_span("workflow.execute") as span:
                span.set_attribute("workflow.step_count", len(self.steps))
                try:
                    start_time = time.perf_counter()
                    result = await self._execute_steps(input_data, span)
                    duration = time.perf_counter() - start_time
                    span.set_attribute("workflow.duration_seconds", duration)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(e)
                    span.set_attribute("error.message", str(e))
                    span.set_attribute("error.type", e.__class__.__name__)
                    raise
        
        return await self._execute_steps(input_data)

    async def _execute_steps(self, input_data: Any, parent_span: Optional[telemetry.Span] = None) -> Any:
        """Execute workflow steps sequentially."""
        current_data = input_data
        
        for step in self.steps:
            if parent_span:
                tracer = telemetry.get_tracer(__name__)
                with tracer.start_span(f"step.{step.func_name}", context=parent_span) as span:
                    span.set_attribute("step.name", step.func_name)
                    span.set_attribute("step.type", step.__class__.__name__)
                    span.set_attribute("step.input_type", str(type(current_data).__name__))
                    
                    try:
                        start_time = time.perf_counter()
                        if isinstance(step, ConditionalStep):
                            current_data = await step.execute(current_data, span)
                        elif isinstance(step, ParallelStep):
                            current_data = await step.execute(current_data, span)
                        else:
                            current_data = await step.execute(current_data)
                        duration = time.perf_counter() - start_time
                        span.set_attribute("step.duration_seconds", duration)
                        span.set_attribute("step.output_type", str(type(current_data).__name__))
                        
                        # Record file operations if present
                        if isinstance(current_data, str) and os.path.exists(current_data):
                            span.set_attribute("file.path", current_data)
                            span.set_attribute("file.size", os.path.getsize(current_data))
                        
                        span.set_status(Status(StatusCode.OK))
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR))
                        span.record_exception(e)
                        span.set_attribute("error.message", str(e))
                        span.set_attribute("error.type", e.__class__.__name__)
                        raise
            else:
                if isinstance(step, ConditionalStep):
                    current_data = await step.execute(current_data)
                elif isinstance(step, ParallelStep):
                    current_data = await step.execute(current_data)
                else:
                    current_data = await step.execute(current_data)
        
        return current_data

@dataclass
class ParallelStep:
    """A step that executes multiple functions in parallel."""
    funcs: List[Callable]
    _func_name: str = field(default="parallel_execution", init=False)
    
    def __post_init__(self):
        """Validate the functions after initialization."""
        for func in self.funcs:
            validate_callable(func)
    
    async def execute(self, input_data: Any, parent_span: Optional[telemetry.Span] = None) -> List[Any]:
        """Execute all functions in parallel with the same input data."""
        if isinstance(input_data, list) and len(input_data) == len(self.funcs):
            # Distribute input data across functions
            if parent_span:
                tasks = [
                    asyncio.create_task(self._execute_with_span(func, data, parent_span))
                    for func, data in zip(self.funcs, input_data)
                ]
            else:
                tasks = [
                    asyncio.create_task(Step(func).execute(data))
                    for func, data in zip(self.funcs, input_data)
                ]
        else:
            # Pass same input to all functions
            if parent_span:
                tasks = [
                    asyncio.create_task(self._execute_with_span(func, input_data, parent_span))
                    for func in self.funcs
                ]
            else:
                tasks = [
                    asyncio.create_task(Step(func).execute(input_data))
                    for func in self.funcs
                ]
        return await asyncio.gather(*tasks)

    async def _execute_with_span(self, func: Callable, input_data: Any, parent_span: telemetry.Span) -> Any:
        """Execute a function with tracing."""
        tracer = telemetry.get_tracer(__name__)
        with tracer.start_span(f"parallel.{func.__name__}", context=parent_span) as span:
            span.set_attribute("step.name", func.__name__)
            span.set_attribute("step.type", "ParallelFunction")
            span.set_attribute("step.input_type", str(type(input_data).__name__))
            
            try:
                start_time = time.perf_counter()
                result = await Step(func).execute(input_data)
                duration = time.perf_counter() - start_time
                span.set_attribute("step.duration_seconds", duration)
                span.set_attribute("step.output_type", str(type(result).__name__))
                
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                span.set_attribute("error.message", str(e))
                span.set_attribute("error.type", e.__class__.__name__)
                raise
    
    @property
    def func(self) -> Callable:
        """Return a function that executes all parallel steps."""
        return lambda x: x  # Dummy function for tracing
    
    @property
    def func_name(self) -> str:
        """Return the name of the function for tracing."""
        return self._func_name

@dataclass
class ConditionalStep:
    """A step that executes one of two branches based on a condition."""
    condition: Callable[[Any], bool]
    then_branch: 'Workflow'
    else_branch: Optional['Workflow'] = None
    _func_name: str = field(init=False)
    
    def __post_init__(self):
        """Validate the condition."""
        validate_callable(self.condition)
        self._func_name = getattr(self.condition, '__name__', 'condition')
    
    async def execute(self, input_data: Any, span: Optional[telemetry.Span] = None) -> Any:
        """Execute the appropriate branch based on the condition."""
        if self.condition(input_data):
            return await self.then_branch.run(input_data, trace=True)
        elif self.else_branch:
            return await self.else_branch.run(input_data, trace=True)
        return input_data
    
    @property
    def func(self) -> Callable:
        """Return a function that executes the conditional step."""
        return self.condition
    
    @property
    def func_name(self) -> str:
        """Return the name of the function for tracing."""
        return self._func_name

def validate_workflow(workflow: "Workflow") -> None:
    """Validate a workflow's steps and their type compatibility."""
    if not workflow.steps:
        raise ValueError("Workflow must have at least one step")
    
    # Validate each step's callable
    for step in workflow.steps:
        if not isinstance(step.func, types.LambdaType):
            validate_callable(step.func)
    
    # Check type compatibility between steps
    for i in range(len(workflow.steps) - 1):
        current_step = workflow.steps[i]
        next_step = workflow.steps[i + 1]

        # Get the actual functions for bound methods
        if inspect.ismethod(current_step.func):
            current_func = current_step.func.__func__
        else:
            current_func = current_step.func
            
        if inspect.ismethod(next_step.func):
            next_func = next_step.func.__func__
        else:
            next_func = next_step.func
        
        # Get return type of current step and parameter type of next step
        current_return = inspect.signature(current_func).return_annotation
        next_param = list(inspect.signature(next_func).parameters.values())[0].annotation

        # Check return type compatibility (covariance)
        # For return types, current_return should be a subtype of next_param
        if not is_compatible_type(current_return, next_param, is_return_type=True):
            raise TypeError(
                f"Step {i+1} return type {current_return} is not compatible with "
                f"step {i+2} parameter type {next_param}"
            )
