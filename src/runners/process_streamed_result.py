from openai.types.responses import ResponseTextDeltaEvent

"""
This module will pass the raw delta of streamed events to a callback function
"""
async def process_streamed_result(result, cb=(lambda x: None)):
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            cb(event.data.delta)
