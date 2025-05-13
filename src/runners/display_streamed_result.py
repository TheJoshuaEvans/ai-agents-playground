from src.runners.process_streamed_result import process_streamed_result

# This helper method displays streamed raw responses as they are received
async def display_streamed_result(result):
    await process_streamed_result(result, lambda x: print(x, end='', flush=True))
    print('\n')
