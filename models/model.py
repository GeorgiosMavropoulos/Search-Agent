### Define models to enable structured output both for llms and user's input
from pydantic import BaseModel

## create extracted info class for testing
class ExtractedInfo(BaseModel):
     name: str
     email: str
     phone: str | None = None