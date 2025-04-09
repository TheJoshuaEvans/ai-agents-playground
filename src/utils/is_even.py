import asyncio

from agents import InputGuardrailTripwireTriggered, GuardrailFunctionOutput, InputGuardrail, Agent, Runner
from pydantic import BaseModel

from src.agents.number_identifier_agent import generate_number_identifier_agent

# This is the most cursed thing I could possibly think to make omfg
# Let's go CRAZY

async def is_even(num):
    class NumberGuardrailOutput(BaseModel):
        is_number: bool
        reasoning: str

    number_guardrail_agent = Agent(
        name="Number Guardrail",
        instructions="Check if the user is presenting input that could be converted into a number somehow",
        output_type=NumberGuardrailOutput,
    )

    async def is_number_guardrail(ctx, agent, input_data):
        result = await Runner.run(number_guardrail_agent, input_data, context=ctx.context)
        final_output = result.final_output_as(NumberGuardrailOutput)
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_number,
        )

    strict_number_guardrail_agent = Agent(
        name="Strict Number Guardrail",
        instructions="Check if the user provides numerical input. If the fail if the user provides anything other than a number.",
        output_type=NumberGuardrailOutput,
    )

    async def is_strict_number_guardrail(ctx, agent, input_data):
        result = await Runner.run(strict_number_guardrail_agent, input_data, context=ctx.context)
        final_output = result.final_output_as(NumberGuardrailOutput)
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_number,
        )

    is_even_agent = Agent(
        name="Is Even",
        handoff_description="Determines if a number is even or odd",
        instructions="Check if the number provided is even or odd. Return only the strings 'even' if even and 'odd' if odd.",
        input_guardrails=[
            InputGuardrail(guardrail_function=is_strict_number_guardrail),
        ],
    )

    number_identifier_agent = Agent(
        name="Number Identifier",
        instructions="""
            You take the user's input and hand off the number it represents to the is_even_agent. Only send
            numerals and do not include any units. For example, if the user inters "The number of legs on a dog",
            you would send with "4". If the user enters "The top speed of a cheetah", you would
            send with "75".
        """,
        handoffs=[is_even_agent],
        input_guardrails=[
            InputGuardrail(guardrail_function=is_number_guardrail),
        ],
    )

    result = await Runner.run(number_identifier_agent, num)
    return result.final_output == 'even'
    