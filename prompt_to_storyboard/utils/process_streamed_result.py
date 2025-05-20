from openai.types.responses import ResponseTextDeltaEvent

async def process_streamed_result(result, cb=(lambda x: None)):
    """
    This module will pass the raw delta of streamed events to a callback function
    """
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            cb(event.data.delta)
