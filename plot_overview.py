import asyncio
import time

from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, trace

from src.agents.plot_overview_agent import PlotOverviewAgent
from src.assets.story_bible import story_bible

def output_stream_text(text: str) -> None:
    print(text, end="", flush=True)

async def main():
    agent = PlotOverviewAgent()

    print('Initializing agent...')
    initialize_result = await agent.initialize(story_bible, streaming_cb=output_stream_text)
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
