### Define models to enable structured output both for llms and user's input
from pydantic import BaseModel

## create extracted info class for testing
class ExtractedInfo(BaseModel):
     name: str
     email: str
     phone: str | None = None


#create a model to experiment with GAIA
class GaiaOutput(BaseModel):
     is_solvable: bool
     unsolvable_reason: str = ""
     final_answer: str = ""