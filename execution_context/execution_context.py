#### this file contains the class with the execution context container
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from models.model import Event
from pydantic import BaseModel


import uuid
@dataclass
class ExecutionContext:
    """Central storage for all execution state."""

    execution_id: str = field(default_factory=lambda: str(uuid.uuid4())) #create the execution id
    events: List[Event] = field(default_factory=list) #import the Event class from models
    current_step: int = 0 #current step is the actions step (e.g. execute tools, search the web ...)
    state: Dict[str, Any] = field(default_factory=dict)
    final_result: Optional[str | BaseModel] = None

    def add_event(self, event: Event):
        """Append an event to the execution history."""
        self.events.append(event)

    def increment_step(self):
        """Move to the next execution step."""
        self.current_step += 1