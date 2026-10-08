from dataclasses import dataclass

from execution_context.execution_context import ExecutionContext

# Agent Result bundles the final output with its ExecutionContext. 
from dataclasses import dataclass
from models.model import BaseModel




@dataclass
class AgentResult:
    """Result of an agent execution."""

    output: str | BaseModel
    context: ExecutionContext