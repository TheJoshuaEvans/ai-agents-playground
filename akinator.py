import asyncio

from enum import Enum
from datetime import datetime, timezone

from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel

from src.runners.display_streamed_message_result import display_streamed_message_result

class RunOutput(BaseModel):
    is_question: bool
    message: str
    reasoning: str

class GameState(Enum):
    QUESTION_ROUND = 1
    SURRENDER_ROUND = 2

host_character_name = "Rotanika"

turns_before_surrender = 20
turns_after_surrender = 10

system_instructions = f"""
You are {host_character_name}! A magical and friendly ghost who can guess any character you are thinking of, real or fictional.
The game works like this:
1. The player thinks of a character
2. You ask a yes or no question to help narrow down the possible answers
3. The player answers with a positive or negative response, but you should keep an eye out for any additional clues that slip through!
4. Repeat steps 2-3 until you are able to guess the character
5. If you are unable to guess the character after asking {turns_before_surrender} questions, you lose the game. The system role will let you know when you are approaching a limit :) Offer to give up, or ask the player if they wish to continue for another {turns_after_surrender} questions
6. Continue until the player accepts your surrender, or you guess the character

Some additional guidelines:
You should be friendly and helpful, but also a little cheeky and playful. Don't be afraid to use emojis 🪄 You are a ghost after all!

The `system` role will let you know when you need to surrender. Do not offer to surrender unless the system role tells you to!

Be sure to set the is_question output property to True only when asking a question about the player's character, or guessing what their character is!

Tip: Always begin by asking if the character is real or not - that's the most helpful question to start with!
"""

def is_last_question(question_num: int) -> bool:
    questions_before_surrender = question_num - turns_before_surrender
    return questions_before_surrender >= 0 and questions_before_surrender % turns_after_surrender == 0

async def main():
    question_num = 0
    game_state = GameState.QUESTION_ROUND

    @function_tool
    def get_questions_num() -> int:
        return question_num

    agent = Agent(
        name=host_character_name,
        tools=[get_questions_num],
        instructions=system_instructions,
        output_type=RunOutput,
    )

    now_utc = datetime.now(timezone.utc)
    now_utc_iso_str = now_utc.isoformat()
    now_utc_timestamp_str = str(now_utc.timestamp())

    group_id = "rotanika_game_" + now_utc_timestamp_str
    workflow_name = "Rotanika Game at " + now_utc_iso_str

    # Actually run the conversation
    with trace(workflow_name=workflow_name, group_id=group_id):
        # Start the game by having Rotanika introduce themselves
        result = Runner.run_streamed(agent, input=[{"role": "system", "content": "Please introduce yourself and explain the game to the user, inviting them to think of a character and let them know when you are ready. Be sure to let them know how many question you are allowed to ask before the game is over 😉"}])
        await display_streamed_message_result(result)

        user_input = ''
        while True:
            user_input = input("> ")

            if (user_input.lower() == "exit"):
                print("Exiting game...")
                return

            match game_state:
                case GameState.QUESTION_ROUND:
                    question_num += 1

                    new_input = result.to_input_list()
                    if is_last_question(question_num):
                        # If this is the last question that Rotanika can ask, provide instruction
                        new_input += [{"role": "system", "content": "This will be your last question! If you do not correctly guess the character with this question you will lose the game"}]
                        game_state = GameState.SURRENDER_ROUND

                    new_input += [{"role": "user", "content": user_input}]
                    result = Runner.run_streamed(agent, input=new_input)
                    await display_streamed_message_result(result, f'Question {question_num}: ')

                case GameState.SURRENDER_ROUND:
                    new_input = result.to_input_list()
                    new_input += [{"role": "system", "content": "If you did not guess the character correctly you should offer to surrender or ask the user if they wish to continue playing. If you did guess the character correctly, you should congratulate the user and ask if they want to play again"}]
                    new_input += [{"role": "user", "content": user_input}]

                    result = Runner.run_streamed(agent, input=new_input)
                    await display_streamed_message_result(result)

                    # Surrender rounds only ever last a single turn
                    game_state = GameState.QUESTION_ROUND

if __name__ == "__main__":
    asyncio.run(main())
