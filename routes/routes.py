from fastapi import APIRouter, status, HTTPException
from agent.agent import Agent
from models.model import QuestionRequest
import traceback


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Create an instance of the agent
agent = Agent()

#port endpoint to interact with the agent
@router.post("/", status_code=status.HTTP_200_OK)
async def interact(request: QuestionRequest):
    try:
        # Call the chatbot method
        response = await agent.chatbot(request.question)

        return {
            "response": response
        }
    ##return  an exception is sth goes wrong
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while establishing connection with the agent: {e}"
        )