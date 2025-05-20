import asyncio
import json

# from prompt_to_storyboard.agents.screenplay_agent import PlotOverviewAgent
from prompt_to_storyboard.agents.screenplay_agent import ScreenplayAgent
from prompt_to_storyboard.agents.storyboard_prompts_agent import StoryboardPromptsAgent
from prompt_to_storyboard.agents.storyboard_images_agent import StoryboardImagesAgent

from prompt_to_storyboard.utils.get_file import get_file
from prompt_to_storyboard.utils.write_file import write_file

INITIAL_PROMPT_FILE = "./prompt_to_storyboard/assets/initial_prompt.txt"
STORY_BIBLE_FILE = "./prompt_to_storyboard/assets/story_bible.txt"
# PLOT_OVERVIEW_FILE = "./prompt_to_storyboard/assets/screenplay.txt"
SCREENPLAY_FILE = "./prompt_to_storyboard/assets/screenplay.txt"
STORYBOARD_PROMPTS_FILE = "./prompt_to_storyboard/assets/storyboard_prompts.txt"

def output_stream_text(text: str) -> None:
    print(text, end="", flush=True)

async def main():
    screenplay_agent = ScreenplayAgent()
    storyboard_prompts_agent = StoryboardPromptsAgent()
    storyboard_images_agent = StoryboardImagesAgent()

    initial_prompt = get_file(INITIAL_PROMPT_FILE)
    story_bible = get_file(STORY_BIBLE_FILE)
    screenplay = get_file(SCREENPLAY_FILE)
    storyboard_prompts = get_file(STORYBOARD_PROMPTS_FILE)

    print('Story Bible:')
    print(story_bible)
    print('=========================\n')

    print('Initial Prompt:')
    print(initial_prompt)
    print('=========================\n')

    if screenplay == "":
        print('No screenplay available. Generating one...')

        prompt_result = await screenplay_agent.generate_screenplay(
            initial_prompt, story_bible, streaming_cb=output_stream_text
        )
        screenplay = prompt_result.screenplay
        comments = prompt_result.comments
        print('Comments:')
        print(comments)
        print('=========================\n')

        write_file(SCREENPLAY_FILE, screenplay)
    else:
        print('Screenplay detected. Skipping generation.\n')

    if storyboard_prompts == "":
        print('No storyboard prompts available. Generating...')

        prompt_result = await storyboard_prompts_agent.generate_storyboard_prompts(
            initial_prompt, story_bible, streaming_cb=output_stream_text
        )
        storyboard_prompts = prompt_result.storyboard_prompts

        write_file(STORYBOARD_PROMPTS_FILE, json.dumps(storyboard_prompts))
    else:
        storyboard_prompts = json.loads(storyboard_prompts)
        print('Storyboard prompts detected. Skipping generation.\n')

    print('Generating storyboard images...\n')
    storyboard_images_agent.generate_storyboard_images(
        storyboard_prompts, story_bible,
    )

if __name__ == "__main__":
    asyncio.run(main())
