from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

import sys
import os
import json

#Import the HR policy Agent implementation in this wrapper
import hr_policy_agent

class HRPolicyAgentExecutor(AgentExecutor):
    "Executes functions of the HR policy agent."

    def __init__(self):
        print("HRPolicyAgentExecutor initialized")
        
    @override
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,) -> None:

        user_input = json.loads(context.get_user_input())
        print("prompt received: ", user_input.get("prompt"))
        # Call the HR policy agent function
        result = await hr_policy_agent.run_hr_policy_agent(
                        prompt=user_input.get("prompt"))
        
        print("Result received: ", result)
        await event_queue.enqueue_event(new_agent_text_message(result))

    @override
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,) -> None:
        
        raise Exception("Not implemented")

if __name__ == "__main__":

    hr_policy_skill = AgentSkill(
        id="HRPolicySkill",
        name="HR Policy Agent Skills",
        description="Answers questions about HR policies.",
        tags=["HR", "policy"],
        examples=[
            "What is the policy on remote work?",
            "What are the vacation days allowed?",
        ],
    )

    hr_policy_agent_card = AgentCard(
        name="HR Policy Agent",
        description="Answers questions about HR policies.",
        url="http://localhost:9001/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[hr_policy_skill],
    )
    
    hr_policy_request_handler = DefaultRequestHandler(
        agent_executor=HRPolicyAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    hr_policy_server = A2AStarletteApplication(
        agent_card=hr_policy_agent_card,
        http_handler=hr_policy_request_handler,
    )

    # Start the Server
    import uvicorn
    uvicorn.run(hr_policy_server.build(), 
                host="0.0.0.0", 
                port=9001, 
                log_level="info")