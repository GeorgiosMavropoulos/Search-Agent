### the main file which calls the agent to start
from agent.agent import Agent
import asyncio
#main class
async def main():
   

    #create an agent's object
    agent = Agent()

    #send your question to the agent
    question = "Please save in a txt file the text `Today is a new day`"
    #call the chatbot method to chat
    await agent.chatbot(question)

#execute main
asyncio.run(main())