### the main file which calls the agent to start
from agent.agent import Agent
from fastapi import FastAPI
import asyncio
from routes.routes import router  as agent_router



app = FastAPI()

app.include_router(agent_router)

