import re

from openai.types.responses import ResponseTextDeltaEvent

# This helper method displays an "Thinking..." message while waiting for a final response from a streamed
# run and then prints the final response when it is received.
async def display_streamed_message_result(result, prefix=""):
    max_dots = 20
    starting_text = "Thinking"
    for i in range(max_dots):
        starting_text += ' '

    thinking_text = starting_text
    num_dots = 0
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(thinking_text, end="\r")
            num_dots += 1
            thinking_text = thinking_text.strip() + '.'
            if num_dots > max_dots:
                num_dots = 0
                thinking_text = starting_text

    # Clear the console line
    print('', end="\x1b[1K\r", flush=True)

    print(prefix + result.final_output.content)
    print('')

