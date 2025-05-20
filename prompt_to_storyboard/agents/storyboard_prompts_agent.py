from datetime import datetime, timezone

from agents import Agent, Runner, trace
from pydantic import BaseModel

from prompt_to_storyboard.utils.process_streamed_result import process_streamed_result

class StoryboardPrompt(BaseModel):
    prompt: str
    script: str

class StoryboardPromptsOutput(BaseModel):
    storyboard_prompts: list[StoryboardPrompt]

system_instructions = f"""
You will take a provided screenplay and story bible, and you will generate a list of prompts for the generation of storyboard images with based on the screenplay, in line with details in the story bible, for every shot that be used to tell the story.
Storyboard prompts should be generated for gpt-image-1
All events that are described in the screenplay MUST be included in the storyboard prompts.
The storyboard prompts MUST include all details about the shot being described, even if they are not visual in nature.
Each storyboard prompt MUST be written independently, and MUST NOT reference any other storyboard prompt.
Each storyboard prompt MUST have all the details needed to generate a complete storyboard image, including the setting, characters, and actions.
The storyboard prompts should be detailed and specific, focusing on the visuals and actions of the characters.
The storyboard prompts should refer to characters by their names and proper nouns should always be preferred over pronouns.

The storyboard prompts MUST be in the form of a list of StoryboardPrompt objects, with each object representing a single prompt, and MUST ALWAYS be added to the 'storyboard_prompts' field of the output.
Each StoryboardPrompt object MUST have the following fields:
- prompt: The prompt for the storyboard image
- script: The snippet of the screenplay that the prompt is based on. This MUST be taken directly from the screenplay, and MUST NOT be modified in any way.
"""

class StoryboardPromptsAgent:
    # ========== PROPERTIES ==========
    agent = None

    # ========== METHODS ==========
    async def generate_storyboard_prompts(self, plot_overview, story_bible, streaming_cb=None):
        input = [{"role": "system", "content": f"This is the story bible associated with the user's prompt. Ensure the generated storyboard prompts are consistent with this content:\n{story_bible}"}]

        input += [{"role": "user", "content": f"This is my screenplay. Please generate a list of prompts for storyboards based on this screenplay:\n{plot_overview}"}]
        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=input)
            await process_streamed_result(result, streaming_cb)

            final_result = result.final_output_as(StoryboardPromptsOutput)

            return final_result

    # ========= BUILT INS ==========
    def __init__(self):
        now_utc = datetime.now(timezone.utc)
        now_utc_iso_str = now_utc.isoformat()
        now_utc_timestamp_str = str(int(now_utc.timestamp() * 6))

        self.trace_id = "trace_storyboard_prompts_writing_" + now_utc_timestamp_str
        self.workflow_name = "Storyboard Prompts Writing at " + now_utc_iso_str

        self.agent = Agent(
            name="Storyboard Prompts Assistant",
            instructions=system_instructions,
            output_type=StoryboardPromptsOutput,
            model="gpt-4.1"
        )
