### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import acompletion
import os
import asyncio
import os
#import prompts
from prompts.prompts import prompts as pr

import json

##load available tools
from tools_schemas.calculator_tool_schema import CalculatorTool as calc
from tools_schemas.websearch_tool_schema import WebSearch as w_search
from tools_schemas.generate_tool_definitions import ToolDefinitions
##import tools


##agent class
class Agent:
    def __init__(self):
     ##load the model and api url           
     self.ollama_model = os.getenv("ollama_model")
     self.ollama_url = os.getenv("ollama_url")
     #create this array to store the messages in order to allow the agent to access them. Artificial memory :D 
     self.messages = []    

     #limit the agent to execute 10 concurrent requests only
     self.semaphore = asyncio.Semaphore(10)

     ##define a list with the tool definition to feed it to the model
     self.tool_functions = [calc.calculator, w_search.web_search]

     #create the tools registry
     self.tool_registry = {fn.__name__: fn for fn in self.tool_functions}

     ##access the tool definitions
     self.tool_definitions = [ToolDefinitions.function_to_tool_definition(fn) for fn in self.tool_functions]


     ##define a function to execute tools and return their results
    def tool_execution(self,tools, tool_call):
      ##get executed tool's name
      function_name = tool_call.function.name
      #get parameters to pass as arguments to the tools
      function_args = json.loads(tool_call.function.arguments)
      #delegate tool's result into a variable
      tool_result = tools[function_name](**function_args)
      #return the result
      return tool_result


    #agent loop
    async def agent_loop(self,question):
     
      self.messages = [
        {"role": "system", "content": pr.system_prompt},
        {"role": "user", "content": question}
    ]
       
      #create a loop to send back the updated information to the LLM
      while True:
        
        response = await acompletion(
            model=f'ollama_chat/{self.ollama_model}',
            messages=self.messages,
            tools=self.tool_definitions
            
        )

        #delegate into a variable LLM's message
        assistant_message = response.choices[0].message
        
        

        #if a tool was called return the final response with tools
        if self.handle_tool_calls(assistant_message):

           continue##return to the loop

        else:
           #if no tools calls store the original answer
           self.messages.append({"role": "assistant", "content": assistant_message.content})
                                 
           return assistant_message.content

    #method to handle tool calls
    def handle_tool_calls(self, ai_response) -> bool: 
        #if model did not called a tool return false
        if not ai_response.tool_calls:
            return False

        if ai_response.tool_calls:
           self.messages.append({
            "role": "assistant",
            "content": ai_response.content or None,
            "tool_calls": ai_response.tool_calls
        })
           for tool_call in ai_response.tool_calls:
                tool_result = self.tool_execution(self.tool_registry, tool_call)
                ##append the messages into message list
                self.messages.append({
                    "role": "tool", 
                    "content": str(tool_result), 
                    "tool_call_id": tool_call.id
                })
        
        return True
                                      

    #call the agent
    async def chatbot(self,question: str):
     
     """LLM call with rate limiting and automatic retry."""
     async with self.semaphore: #use semaphore to implement rate limiting
       
       
          #return the final response
        final_response = await self.agent_loop(question)
        print(final_response)
        return final_response
           


       
                          
                        
        
    

   





