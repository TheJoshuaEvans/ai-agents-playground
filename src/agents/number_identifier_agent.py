import asyncio

from agents import GuardrailFunctionOutput, InputGuardrail, Agent, Runner
from pydantic import BaseModel

class NumberGuardrailOutput(BaseModel):
    is_number: bool
    reasoning: str

number_guardrail_agent = Agent(
    name="Number Guardrail",
    instructions="Check if the user is presenting input that can be represented as a number",
    output_type=NumberGuardrailOutput,
)

async def is_number_guardrail(ctx, agent, input_data):
    result = await Runner.run(number_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(NumberGuardrailOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_number,
    )

def generate_number_identifier_agent(handoffs = []):
    return Agent(
        name="Number Identifier",
        instructions="""
        You take the user's input and respond with the number of that represents that input. Only respond with
        numerals and do not include any units. For example, if the user inters "The number of legs on a dog",
        you would respond with "4". If the user enters "The top speed of a cheetah", you would
        respond with "75".
        """,
        handoffs=handoffs,
        input_guardrails=[
            InputGuardrail(guardrail_function=is_number_guardrail),
        ],
    )
