import asyncio
import time

from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, trace

from src.agents.plot_overview_agent import PlotOverviewAgent

def output_stream_text(text: str) -> None:
    print(text, end="", flush=True)

async def main():
    agent = PlotOverviewAgent()

    print('Initializing agent...')
    initialize_result = await agent.initialize(story_bible="""
Characters:
- Jumpy: A well-aged but still sprightly rabbit who use to have a tendency to slack off whenever the opportunity arose. He is now a wise old rabbit who has learned the value of hard work and responsibility.
- Lumber: An ancient tortoise who has always been a hard and diligent worker. He is now a wise old tortoise who has learned the value of taking breaks and enjoying life.

Location:
The forest: A lush and vibrant forest filled with trees, flowers, and wildlife. It is a place of beauty and tranquility. A path runs through the forest that the forest animals use for impromptu races
""", streaming_cb=output_stream_text)
    print('\n')
    print('Agent initial response: ' + initialize_result)
    print('\n')

    print('> ', end="", flush=True)
    user_input = input()

    prompt_result = await agent.send_prompt(user_input, streaming_cb=output_stream_text)
    print('\n')
    print('Prompt comments: ' + prompt_result.content)
    print('Plot Overview: ' + prompt_result.plot_overview)
    print('\n')

if __name__ == "__main__":
    asyncio.run(main())
