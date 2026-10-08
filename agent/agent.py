### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env

#import prompts
from prompts.prompts import prompts as pr
import asyncio
##load available tools



from .agent_result import AgentResult
from .helper_methods import AgentHelperMethod

#impor the class with the method generate code file
from tools_schemas.generate_code_file_tool import GenerateCodeFile as generate_code
#import the class with the method write to txt

##import tools
from llm_communication_layer.communication_layer import LLMRequest, LlmClient, LlmResponse
from models.model import BaseTool,Message,ToolCall,ToolResult
from typing import List
from execution_context.execution_context import ExecutionContext,Event


##agent class
class Agent:
    def __init__( #create agent's constructor
        self,
        model: LlmClient,
        tools: List[BaseTool] = None,
        instructions: str = "",
        max_steps: int = 10,
        name: str = "agent",): 
     self.model = model
     self.instructions = instructions # System prompt that defines the agent’s behavior
     self.max_steps = max_steps # max steps the agent can take to solve a problem. this helps us to prevent infinity loops
     self.name = name
     self.tools = self._setup_tools(tools or []) #_setup_tools prepares tool list for use
    
    #set up agent tools 
    def _setup_tools(self, tools: List[BaseTool]) -> List[BaseTool]:
      return tools


    #run method is the main entry point which creates the execution environment, manages the think–act loop, and returns the result.
    async def run( self, user_input: str, context: ExecutionContext = None) -> AgentResult:
         #create or reuse context
      if context is None:
        context = ExecutionContext()

      #add user input as the first event
      user_event = Event(execution_id=context.execution_id,author="user",content=[Message(role="user",content=user_input)])

      context.add_event(user_event) #add user event into the event list

      #execute steps until completion or max steps reached
      while not context.final_result and context.current_step < self.max_steps:
         await self.step(context) #add this step into the execution context

         #check if the last event is a final response
         last_event = context.events[-1]
         if AgentHelperMethod._is_final_response(last_event):
            context.final_result = AgentHelperMethod._extract_final_result(last_event)

      return AgentResult(output=context.final_result, context=context) ##return the agent's response

    #helper method to detect whether the response from the llm is the final one
    def is_final_response(self,event:Event) -> bool:
      """Check if this event contains a final response."""
      #check if the agent made any tool call
      has_tool_calls =  any(isinstance(c, ToolCall) for c in event.content)
      #check if the agent got any tool results
      has_tool_results = any(isinstance(c,ToolResult)for c in event.content)
      return not has_tool_calls and not has_tool_results

    #method to extract final result
    def extract_final_result(self,event:Event)-> str:
      for item in event.content:
        if isinstance(item, Message) and item.role == "assistant":
            return item.content
      return None



result = asyncio(Agent.agent.run("What is 1234 * 5678?"))
print(result.output)                      # "7006652"
print(result.context.current_step) 






      


       
   
    
    

   
           


       
                          
                        
        
    

   