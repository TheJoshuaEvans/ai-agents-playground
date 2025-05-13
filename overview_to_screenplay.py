import asyncio
import time

from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, trace

from src.agents.overview_to_screenplay_agent import OverviewToScreenplayAgent
from src.assets.story_bible import story_bible
from src.assets.plot_overview import plot_overview

def output_stream_text(text: str) -> None:
    print(text, end="", flush=True)

async def main():
    agent = OverviewToScreenplayAgent()

    prompt_result = await agent.send_prompt(story_bible, plot_overview, streaming_cb=output_stream_text)

    print('\n')
    print('Prompt comments:\n' + prompt_result.content + '\n')
    print('Screenplay:\n' + prompt_result.screenplay + '\n')
    print('\n')

if __name__ == "__main__":
    asyncio.run(main())
