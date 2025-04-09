import asyncio
import time

from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    thread_id = str(time.time())
    with trace(workflow_name="Conversation " + thread_id, group_id=thread_id):
        print('Beginning conversation.')
        user_input = input()
        result = Runner.run_streamed(agent, input=user_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        print('\n')

        user_input = input()
        while user_input.lower() != "exit":
            new_input = result.to_input_list() + [{"role": "user", "content": user_input}]
            result = Runner.run_streamed(agent, input=new_input)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
            print('\n')

            user_input = input()

if __name__ == "__main__":
    asyncio.run(main())
