from datetime import datetime, timezone

from agents import Agent, Runner, trace
from pydantic import BaseModel

from src.runners.process_streamed_result import process_streamed_result

system_instructions = """
You are an assistant that takes a plot overview and story bible, and generates a screenplay based on them.
The story bible is a collection of information about the characters, locations, and other relevant details that may be relevant to the screenplay.
The plot overview is a description of the actions that take place in the story.
The plot overview will not have dialogue, so you should generate all dialogue as needed.

The generated screenplay MUST be in Fountain format, and MUST be a complete screenplay, including all scenes, characters, and dialogue.
A properly formatted screenplay should look like the following:
```
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
DO NOT use the above example as story inspiration. ONLY use it to understand formatting requirements
"""

class ScreenplayOutput(BaseModel):
    screenplay: str
    content: str

class OverviewToScreenplayAgent:
    # ========== PROPERTIES ==========
    agent = None

    # ========== METHODS ==========
    async def send_prompt(self, story_bible, plot_overview, streaming_cb=None):
        prompt_text = f"""Please generate a screenplay. This is the story bible:\n{story_bible}\nThis is the plot overview:\n{plot_overview}\n"""
        new_input = [{"role": "user", "content": prompt_text}]

        with trace(workflow_name=self.workflow_name, trace_id=self.trace_id):
            result = Runner.run_streamed(self.agent, input=new_input)
            await process_streamed_result(result, streaming_cb)

            final_result = result.final_output_as(ScreenplayOutput)

            return final_result

    # ========= BUILT INS ==========
    def __init__(self):
        now_utc = datetime.now(timezone.utc)
        now_utc_iso_str = now_utc.isoformat()
        now_utc_timestamp_str = str(int(now_utc.timestamp() * 6))

        self.trace_id = "trace_plot_overview_to_screenplay_converting_" + now_utc_timestamp_str
        self.workflow_name = "Plot Overview Converting to Screenplay at " + now_utc_iso_str

        self.agent = Agent(
            name="Plot Overview to Screenplay Converter",
            instructions=system_instructions,
            output_type=ScreenplayOutput,
        )
