from openai.types.responses import ResponseTextDeltaEvent

# This helper method displays streamed raw responses as they are received
async def display_streamed_result(result):
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print('\n')
