### the main file which calls the agent to start
from agent.agent import Agent
import asyncio
#main class
async def main():
   

    #create an agent's object
    agent = Agent()

    #send your question to the agent
    question = """
Create a SQL file named customers.sql.

The file must contain a CREATE TABLE statement for a table named customers
with the following columns:

1. id:
   - INT
   - PRIMARY KEY
   - AUTO_INCREMENT

2. name:
   - CHAR(100)
   - NOT NULL

3. phone_number:
   - INT
   - NOT NULL
   - The phone number should have a maximum length of 10 digits.

Do not execute the SQL.
Only generate the SQL code and save it into the customers.sql file.
"""
    #call the chatbot method to chat
    await agent.chatbot(question)

#execute main
asyncio.run(main())