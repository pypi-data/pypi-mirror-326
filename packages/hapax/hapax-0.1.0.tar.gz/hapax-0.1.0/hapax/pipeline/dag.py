"""
DAG-based pipeline system for Hapax.
Allows defining complex workflows with parallel execution and branching.
"""
from typing import Dict, List, Any, Optional, Callable, TypeVar, Generic, Union, Set
from dataclasses import dataclass, field
import asyncio
from enum import Enum
from abc import ABC, abstractmethod
import networkx as nx
from opentelemetry import trace
from ..observability.llm import LLMTracer

T = TypeVar('T')  # Type for node input
U = TypeVar('U')  # Type for node output

class ExecutionMode(str, Enum):
    """Execution mode for pipeline nodes."""
    SEQUENTIAL = "sequential"  # Execute in sequence
    PARALLEL = "parallel"    # Execute in parallel
    CONCURRENT = "concurrent"  # Execute concurrently but don't wait

class BranchCondition(ABC):
    """Base class for branch conditions in pipeline."""
    @abstractmethod
    async def evaluate(self, input_data: Any) -> bool:
        """Evaluate the condition."""
        pass

class SimpleBranchCondition(BranchCondition):
    """Simple branch condition using a callable."""
    def __init__(self, condition: Callable[[Any], bool]):
        self.condition = condition
    
    async def evaluate(self, input_data: Any) -> bool:
        return self.condition(input_data)

@dataclass
class PipelineNode(Generic[T, U]):
    """A node in the pipeline DAG."""
    name: str
    func: Callable[[T], U]
    inputs: List[str] = field(default_factory=list)
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    condition: Optional[BranchCondition] = None
    retry_count: int = 0
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    async def execute(
        self,
        input_data: T,
        tracer: Optional[LLMTracer] = None
    ) -> U:
        """Execute the node with tracing."""
        if tracer:
            with tracer.tracer.start_as_current_span(f"node_{self.name}") as span:
                span.set_attribute("pipeline.node.name", self.name)
                span.set_attribute(
                    "pipeline.node.execution_mode",
                    self.execution_mode.value
                )
                try:
                    if asyncio.iscoroutinefunction(self.func):
                        result = await self.func(input_data)
                    else:
                        result = self.func(input_data)
                    return result
                except Exception as e:
                    span.set_attribute("error", str(e))
                    raise
        else:
            if asyncio.iscoroutinefunction(self.func):
                return await self.func(input_data)
            return self.func(input_data)

class DAGPipeline:
    """A DAG-based pipeline with flexible execution modes."""
    
    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()
        self.tracer = LLMTracer(f"pipeline.{name}")
    
    def add_node(
        self,
        node: PipelineNode,
        dependencies: Optional[List[Union[str, tuple[str, BranchCondition]]]] = None
    ):
        """Add a node to the pipeline with optional dependencies."""
        self.graph.add_node(node.name, node=node)
        
        if dependencies:
            for dep in dependencies:
                if isinstance(dep, tuple):
                    dep_name, condition = dep
                    self.graph.add_edge(
                        dep_name,
                        node.name,
                        condition=condition
                    )
                else:
                    self.graph.add_edge(dep_name, node.name)
    
    def get_execution_groups(self) -> List[Set[str]]:
        """Get groups of nodes that can be executed together."""
        groups = []
        executed = set()
        
        while len(executed) < len(self.graph.nodes):
            group = set()
            for node in self.graph.nodes:
                if node not in executed:
                    predecessors = set(self.graph.predecessors(node))
                    if predecessors.issubset(executed):
                        group.add(node)
            
            if not group:
                raise ValueError("Circular dependency detected")
            
            groups.append(group)
            executed.update(group)
        
        return groups
    
    async def execute(
        self,
        initial_input: Any = None
    ) -> Dict[str, Any]:
        """Execute the pipeline."""
        results = {}
        if initial_input is not None:
            results["__input__"] = initial_input
        
        with self.tracer.tracer.start_as_current_span(
            f"pipeline_{self.name}"
        ) as pipeline_span:
            try:
                # Get execution groups
                groups = self.get_execution_groups()
                
                # Execute groups in order
                for group in groups:
                    tasks = []
                    
                    # Create tasks for each node in the group
                    for node_name in group:
                        node = self.graph.nodes[node_name]["node"]
                        
                        # Get input data
                        if not node.inputs:
                            input_data = initial_input
                        else:
                            input_data = {
                                input_name: results[input_name]
                                for input_name in node.inputs
                                if input_name in results
                            }
                        
                        # Check conditions
                        skip_node = False
                        for pred in self.graph.predecessors(node_name):
                            edge_data = self.graph.edges[pred, node_name]
                            if "condition" in edge_data:
                                condition: BranchCondition = edge_data["condition"]
                                if not await condition.evaluate(results[pred]):
                                    skip_node = True
                                    break
                        
                        if skip_node:
                            continue
                        
                        # Create execution task
                        task = asyncio.create_task(
                            node.execute(input_data, self.tracer)
                        )
                        tasks.append((node_name, task))
                    
                    # Wait for tasks based on execution mode
                    for node_name, task in tasks:
                        node = self.graph.nodes[node_name]["node"]
                        
                        if node.execution_mode != ExecutionMode.CONCURRENT:
                            try:
                                if node.timeout:
                                    results[node_name] = await asyncio.wait_for(
                                        task,
                                        timeout=node.timeout
                                    )
                                else:
                                    results[node_name] = await task
                            except Exception as e:
                                pipeline_span.set_attribute(
                                    f"error.{node_name}",
                                    str(e)
                                )
                                raise
                
                return results
            
            except Exception as e:
                pipeline_span.set_attribute("error", str(e))
                raise

def branch_if(condition: Union[BranchCondition, Callable[[Any], bool]]) -> BranchCondition:
    """Create a branch condition."""
    if isinstance(condition, BranchCondition):
        return condition
    return SimpleBranchCondition(condition)
