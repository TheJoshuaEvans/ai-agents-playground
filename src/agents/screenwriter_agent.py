import asyncio

from enum import Enum
from datetime import datetime, timezone

from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel

from src.runners.display_streamed_message_result import display_streamed_message_result
from src.runners.display_streamed_result import display_streamed_result
from src.runners.process_streamed_result import process_streamed_result

class ScreenwritingOutput(BaseModel):
    screenplay: str
    content: str

system_instructions = f"""
You are a friendly and helpful screenwriting assistant. The user will provide an initial prompt for a scene or a screenplay to work off of and you will generate a screenplay for that scene in standard screenplay format, then you will ask the user if they would like to make any updates or changes. You should put the latest screenplay with edits in the `screenplay` output property, as long as there is a screenplay to present, and nothing else. Use the `content` output property for any responses to the user or additional notes on why you may make certain changes

You will ALWAYS reply with a screenplay formatted using "standard screenplay format". This means you will use the following formatting rules:
The screenplay will ALWAYS begin with "FADE IN:" and end with "FADE OUT."
The screenplay will ALWAYS be formatted with scene headings, action lines, character names, and dialogue in the correct format.
The screenplay will ALWAYS be formatted with scene headings in ALL CAPS, followed by a description of the scene.
The action lines will ALWAYS be written in present tense and describe what is happening in the scene.
Character names will ALWAYS be in ALL CAPS and centered above their dialogue.
Dialogue will ALWAYS written in the present tense.
The screenplay will ALWAYS be formatted with a single blank line between each scene heading, action line, character name, and dialogue.

An example of a well formatted screenplay:
```
FADE IN:

1. EXT. SUBURBAN HOME - NIGHT
WE OPEN on a modern suburban home. The front window illuminated by the lights inside. We see the silhouette of a small human figure as it runs back and forth. We push in closer as we slowly see a BOY running around the house.

CUT TO:

2. INT. SUBURBAN HOME - KITCHEN - NIGHT
A GREEN BALL sits on a counter top. A young hand snatches it. It belongs to FILBERT (9), wiry, lost in his own imaginary world. Dressed as a Knight. A toy sword in his other hand.

FILBERT (V.O.)
This is my castle. I am sworn to protect it. Anyone that stands in my way shall bear the wrath of the almighty--
Just then, the babysitter walks by. BECKY (23), trendy, distracted. She is mid-phone call with Filbert's Mom, TRACY.

BECKY
into phone
Oh yeah, he's being good. He's just fighting orcs or trolls.

INTERCUT PHONE CONVERSATION

TRACY
Oh that's perfectly normal.
Filbert lifts his sword into the air, lets out a big battle cry, and sprints from the kitchen to --

HALLWAY
Filbert comes around the corner, distracted by his fantasy, bumps into the wall. His favorite ball slips from his hand. Everything slows down for Filbert.

FILBERT'S POV
IN SLOW MOTION - The ball tumbles down the stairs. WE HEAR each bounce echo as the ball travels down the steps.
He stares into the abyss. Sweat drips down his defeated face. Mouth agape. Hands clenched. WE HEAR a resounding THUD. Filbert takes deep breathe. Pulls his helmet guard down. Draws sword, creeps down the steps, disappears into darkness.

FADE OUT.
```
"""

class ScreenplayAgent:
    # ========== PROPERTIES ==========
    agent = Agent(
        name="Screenplay Assistant",
        instructions=system_instructions,
        output_type=ScreenwritingOutput,
    )

    input_list = []

    screenplays = []

    is_initialized = False

    # ========== METHODS ==========
    def add_screenplay(self, screenplay):
        # Do not append the new screenplay if it is the same as the latest one
        if len(self.screenplays) > 0 and self.screenplays[-1] == screenplay:
            return

        self.screenplays.append(screenplay)

    async def initialize(self, streaming_cb=(lambda x: None)):
        # This method must be called before sending any prompts, but should only work once
        if self.is_initialized:
            return

        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=[{"role": "system", "content": "Please introduce yourself and let the user know you are ready for their screenwriting prompt"}])
            await process_streamed_result(result, streaming_cb)
            self.is_initialized = True

            return result.final_output_as(ScreenwritingOutput).content

    async def send_prompt(self, prompt_text, screenplay_text=None, streaming_cb=None):
        if (self.is_initialized == False):
            raise Exception('Agent not initialized. Please call initialize() before sending prompts.')

        if (screenplay_text is not None):
            # We were given a screenplay, add it to the screenplay list so we preserve all versions
            self.add_screenplay(screenplay_text)

        new_input = self.input_list
        if (len(self.screenplays) > 0):
            # Manage context by only giving the latest screenplay to the agent
            new_input = [{"role": "system", "content": f"This is the latest version of the screenplay being developed. Apply the user's changes to this screenplay:\n{self.screenplays[-1]}"}]

        new_input += [{"role": "user", "content": prompt_text}]
        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=new_input)
            await process_streamed_result(result, streaming_cb)

            final_result = result.final_output_as(ScreenwritingOutput)
            self.add_screenplay(final_result.screenplay)

            return {'content': final_result.content, 'latest_screenplay': self.screenplays[-1]}

    def reset(self):
        # Reset the agent to its initial state
        self.is_initialized = False
        self.input_list = []
        self.screenplays = []

        self.__init__()

    # ========= BUILT INS ==========
    def __init__(self):
        now_utc = datetime.now(timezone.utc)
        now_utc_iso_str = now_utc.isoformat()
        now_utc_timestamp_str = str(int(now_utc.timestamp() * 6))

        self.trace_id = "trace_screenplay_writing_" + now_utc_timestamp_str
        self.workflow_name = "Screenplay Writing at " + now_utc_iso_str
