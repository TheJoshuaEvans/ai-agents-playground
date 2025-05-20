from datetime import datetime, timezone

from agents import Agent, Runner, trace
from pydantic import BaseModel

from prompt_to_storyboard.utils.process_streamed_result import process_streamed_result

class ScreenplayOutput(BaseModel):
    screenplay: str
    comments: str

system_instructions = f"""
You will take a story prompt from a user and a story bible from the system, and write a screenplay in for the story, in paragraph form, based on the prompt and story bible.

The screenplay MUST be in Fountain format, and MUST include all the details needed to generate a complete screenplay, including the setting, characters, and actions.
The screenplay should be detailed and specific, focusing on the visuals and actions of the characters.
You must ALWAYS ensure that the screenplay is consistent with the story bible.

ALWAYS put the screenplay in the 'screenplay' field of the output, and any other relevant information or commentary in the 'comments' field.

This is an example of a screenplay in Fountain format:
```
Title:
    BRICK & STEEL
    FULL RETIRED
Credit: Written by
Author: Stu Maschwitz
Source: Story by KTM
Draft date: 1/20/2012

EXT. BRICK'S PATIO - DAY

A gorgeous day. The sun is shining. But BRICK BRADDOCK, retired police detective, is sitting quietly, contemplating -- something.

The SCREEN DOOR slides open and DICK STEEL, his former partner and fellow retiree, emerges with two cold beers.

STEEL
Beer's ready!

BRICK
Are they cold?

STEEL
Does a bear crap in the woods?

Steel sits. They laugh at the dumb joke.

STEEL
(beer raised)
To retirement.

BRICK
To retirement.

They drink long and well from the beers.

And then there's a long beat.
Longer than is funny.
Long enough to be depressing.

The men look at each other.

STEEL
Screw retirement.

BRICK ^
Screw retirement.

SMASH CUT TO:

INT. TRAILER HOME - DAY

This is the home of THE BOY BAND, AKA DAN and JACK. They too are drinking beer, and counting the take from their last smash-and-grab. Money, drugs, and ridiculous props are strewn about the table.

JACK
(in Vietnamese, subtitled)
*Did you know Brick and Steel are retired?*

DAN
Then let's retire them.
_Permanently_.

Jack begins to argue vociferously in Vietnamese (?), But mercifully we…

CUT TO:

EXT. BRICK'S POOL - DAY

Steel, in the middle of a heated phone call:

STEEL
They're coming out of the woodwork!
(pause)
No, everybody we've put away!
(pause)
Point Blank Sniper?

.SNIPER SCOPE POV

From what seems like only INCHES AWAY. _Steel's face FILLS the *Leupold Mark 4* scope_.

STEEL
The man's a myth!

Steel turns and looks straight into the cross-hairs.

STEEL
(oh crap)
Hello…

CUT TO:

.OPENING TITLES

> BRICK BRADDOCK <
> & DICK STEEL IN <

> BRICK & STEEL <
> FULL RETIRED <

SMASH CUT TO:

EXT. WOODEN SHACK - DAY

COGNITO, the criminal mastermind, is SLAMMED against the wall.

COGNITO
Woah woah woah, Brick and Steel!

Sure enough, it's Brick and Steel, roughing up their favorite usual suspect.

COGNITO
What is it you want with me, DICK?

Steel SMACKS him.

STEEL
Who's coming after us?

COGNITO
Everyone's coming after you mate! Scorpio, The Boy Band, Sparrow, Point Blank Sniper…

As he rattles off the long list, Brick and Steel share a look. This is going to be BAD.

CUT TO:

INT. GARAGE - DAY

BRICK and STEEL get into Mom's PORSCHE, Steel at the wheel. They pause for a beat, the gravity of the situation catching up with them.

BRICK
This is everybody we've ever put away.

STEEL
(starting the engine)
So much for retirement!

They speed off. To destiny!

CUT TO:

EXT. PALATIAL MANSION - DAY

An EXTREMELY HANDSOME MAN drinks a beer. Shirtless, unfortunately.

His minion approaches offscreen:

MINION
We found Brick and Steel!

HANDSOME MAN
I want them dead. DEAD!

Beer flies.

> BURN TO PINK.

> THE END <
```
"""

class ScreenplayAgent:
    # ========== PROPERTIES ==========
    agent: Agent

    # ========== METHODS ==========
    async def generate_screenplay(self, prompt_text, story_bible = '', streaming_cb=None):
        input = ''
        if (story_bible != ""):
            input = [{"role": "system", "content": f"This is the story bible associated with the user's prompt. Ensure the generated screenplay is consistent with this content:\n{story_bible}"}]
        else:
            input = [{"role": "system", "content": "There is no story bible information available for this prompt."}]

        input += [{"role": "user", "content": prompt_text}]
        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=input)
            await process_streamed_result(result, streaming_cb)

            final_result = result.final_output_as(ScreenplayOutput)

            return final_result

    # ========= BUILT INS ==========
    def __init__(self):
        now_utc = datetime.now(timezone.utc)
        now_utc_iso_str = now_utc.isoformat()
        now_utc_timestamp_str = str(int(now_utc.timestamp() * 6))

        self.trace_id = "trace_screenplay_writing_" + now_utc_timestamp_str
        self.workflow_name = "Screenplay Writing at " + now_utc_iso_str

        self.agent = Agent(
            name="Screenplay Assistant",
            instructions=system_instructions,
            output_type=ScreenplayOutput,
            model="gpt-4.1"
        )
