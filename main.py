### the main file which calls the agent to start
from agent.agent import Agent
import asyncio
#main class
async def main():
   

    #create an agent's object
    agent = Agent()
    #call the chatbot method to chat
    await agent.chatbot()

#execute main
asyncio.run(main())