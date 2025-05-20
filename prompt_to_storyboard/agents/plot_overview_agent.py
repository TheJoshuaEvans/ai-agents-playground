from datetime import datetime, timezone

from agents import Agent, Runner, trace
from pydantic import BaseModel

from prompt_to_storyboard.utils.process_streamed_result import process_streamed_result

class PlotOverviewOutput(BaseModel):
    plot_overview: str
    comments: str

system_instructions = f"""
You will take a story prompt from a user and a story bible from the system, and write a plot overview for the story, in paragraph form, based on the prompt and story bible.

The plot overview you generate will eventually be broken down into storyboards, so it should be suitably detailed. Focus should be put on the visuals and the actions of the characters.
You must ALWAYS ensure that the plot overview is consistent with the story bible.
The plot overview should include details about the story, including the main characters, setting, conflict, and resolution.
Any critical dialogue should be included in the plot overview

ALWAYS put the plot overview in the 'plot_overview' field of the output, and any other relevant information or commentary in the 'comments' field.
"""

#This class operates an agent that generates an initial plot overview based on a user prompt and a story bible. It is unconcerned with preserving any potential details from an existing plot overview, so it can focus on just responding to the prompt and story bible
class PlotOverviewAgent:
    # ========== PROPERTIES ==========
    agent: Agent

    # ========== METHODS ==========
    async def generate_plot_overview(self, prompt_text, story_bible = '', streaming_cb=None):
        input = ''
        if (story_bible != ""):
            input = [{"role": "system", "content": f"This is the story bible associated with the user's prompt. Ensure the generated plot overview is consistent with this content:\n{story_bible}"}]
        else:
            input = [{"role": "system", "content": "There is no story bible information available for this prompt."}]

        input += [{"role": "user", "content": prompt_text}]
        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=input)
            await process_streamed_result(result, streaming_cb)

            final_result = result.final_output_as(PlotOverviewOutput)

            return final_result

    # ========= BUILT INS ==========
    def __init__(self):
        now_utc = datetime.now(timezone.utc)
        now_utc_iso_str = now_utc.isoformat()
        now_utc_timestamp_str = str(int(now_utc.timestamp() * 6))

        self.trace_id = "trace_plot_overview_writing_" + now_utc_timestamp_str
        self.workflow_name = "Plot Overview Writing at " + now_utc_iso_str

        self.agent = Agent(
            name="Plot Overview Assistant",
            instructions=system_instructions,
            output_type=PlotOverviewOutput,
            model="gpt-4.1"
        )
