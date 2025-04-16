import os

from datetime import datetime, timezone

from agents import Agent, Runner, function_tool, trace
from nicegui import app, binding, ui
from pydantic import BaseModel

from src.agents.screenwriter_agent import ScreenplayAgent
from src.runners.display_streamed_message_result import display_streamed_message_result
from src.runners.display_streamed_result import display_streamed_result
from src.utils.double_newline import double_newline

@binding.bindable_dataclass
class ScreenplayData:
    # Don't reset the screenplay UI element when resetting the data
    screenplay_ui = None

    def reset(self):
        self.is_thinking = False
        self.raw_output = ""
        self.prompt_text = ""
        self.latest_screenplay = ""
        self.conversation_log = []
        self.user_name = "User"
        self.has_edited_screenplay = False
        self.has_received_screenplay = False

        self.now_utc = datetime.now(timezone.utc)
        self.now_utc_iso_str = self.now_utc.isoformat()
        self.now_utc_timestamp_str = str(int(self.now_utc.timestamp() * 6))

    def add_to_conversation_log(self, text: str, user: str) -> None:
        stamp = datetime.now(timezone.utc).isoformat()
        avatar = f'https://robohash.org/{agent_name}' if user == agent_name else f'https://robohash.org/{user}?set=set4'

        self.conversation_log.append({"name": user, "text": text, "stamp": stamp, "avatar": avatar})

    def __init__(self):
        self.reset()

screenplay_agent = ScreenplayAgent()
data = ScreenplayData()

agent_name = "Super Screenplay Assistant"

# =================== HELPERS ===================
def add_output_stream_text(text: str) -> None:
    data.raw_output += text

async def do_thinking(coroutine):
    data.is_thinking = True
    prompt_and_button.refresh()
    response = await coroutine
    data.is_thinking = False
    prompt_and_button.refresh()

    return response

# =================== UI ELEMENTS ===================
@ui.refreshable
def conversation_log_ui() -> None:
    if len(data.conversation_log) > 0:
        for log_entry in reversed(data.conversation_log):
            ui.chat_message(log_entry['text'], name=log_entry['name'], avatar=log_entry['avatar'], stamp=log_entry['stamp'])

@ui.refreshable
def screenplay_ui() -> None:
    if screenplay_agent.is_initialized == False:
        data.screenplay_ui = ui.textarea('').style('width: 100%')
        data.screenplay_ui.enabled = False
    else:
        ui.markdown('## Latest Screenplay')
        data.screenplay_ui = ui.textarea('', on_change=handle_screenplay_ui_change).bind_value(data, 'latest_screenplay').classes('font-mono').style('width: 100%')
        grow_screenplay_ui()
    ui.separator()

@ui.refreshable
def prompt_and_button() -> None:
    if data.is_thinking:
        ui.spinner(size='lg')
    elif screenplay_agent.is_initialized == False:
        ui.button('Get Started!', on_click=initialize).style('width: 20%')
    else:
        ui.textarea('Update Screenplay').bind_value(data, 'prompt_text').classes('w-full')
        ui.button('Send', on_click=send_prompt).style('width: 20%')

@ui.refreshable
def previous_versions() -> None:
    def handle_click(i):
        data.latest_screenplay = screenplay_agent.screenplays[i]

    if len(screenplay_agent.screenplays) > 0:
        with ui.dropdown_button('Previous Versions', auto_close=True):
            for i, screenplay in enumerate(screenplay_agent.screenplays):
                ui.item(f"Version {i+1}", on_click=lambda i=i: handle_click(i))

# =================== EVENT HANDLERS ===================
def grow_screenplay_ui():
    ui.run_javascript(f'getHtmlElement({data.screenplay_ui.id}).style.height = "5px"')
    ui.run_javascript(f'getHtmlElement({data.screenplay_ui.id}).style.height = (getHtmlElement({data.screenplay_ui.id}).scrollHeight) + "px"')

def handle_screenplay_ui_change():
    grow_screenplay_ui()
    data.has_edited_screenplay = True

async def initialize():
    initial_response_text = await do_thinking(screenplay_agent.initialize(add_output_stream_text))
    add_output_stream_text('\n\n')
    data.add_to_conversation_log(initial_response_text, agent_name)
    conversation_log_ui.refresh()
    screenplay_ui.refresh()

async def reset():
    screenplay_agent.reset()
    data.reset()
    reset_dialog.close()
    prompt_and_button.refresh()
    conversation_log_ui.refresh()

async def send_prompt():
    prompt_text = data.prompt_text

    # Add the prompt text to the log, then clear the prompt text
    data.add_to_conversation_log(prompt_text, data.user_name)
    conversation_log_ui.refresh()

    data.prompt_text = ''

    # Send the prompt to the agent with our version of the latest screenplay if it was edited
    response = await do_thinking(screenplay_agent.send_prompt(
        prompt_text,
        screenplay_text=data.latest_screenplay if data.has_edited_screenplay == True else None,
        streaming_cb=add_output_stream_text
    ))
    data.has_received_screenplay = True
    add_output_stream_text('\n\n')

    # Add the full response to the log
    data.add_to_conversation_log(response['content'], agent_name)
    data.latest_screenplay = response['latest_screenplay']
    previous_versions.refresh()
    screenplay_ui.refresh()
    conversation_log_ui.refresh()

    data.has_edited_screenplay = False

# =================== MAIN BODY ===================
with ui.dialog() as reset_dialog, ui.card():
    ui.label('Are you SURE you want to reset?')
    with ui.row():
        ui.button('Reset', on_click=reset)
        ui.space()
        ui.button('Cancel', on_click=reset_dialog.close)

with ui.card().classes('w-full'):
    ui.markdown('# Super Screenplay Assistant 3000')
    previous_versions()

    with ui.splitter(value=70).classes('w-full') as splitter:
        with splitter.before:
            screenplay_ui()
        with splitter.after:
            with ui.card_section().classes('w-full max-h-screen'):
                ui.markdown('## Conversation Log')
                conversation_log_ui()

    with ui.card_section().classes('w-full'):
        with ui.column():
            prompt_and_button()

with ui.card().classes('w-4/5'):
    ui.markdown('### Raw Output Stream')
    ui.markdown('').bind_content(data, 'raw_output').classes('w-full font-mono')

with ui.card().classes('w-1/5'):
    ui.markdown('## Settings')
    dark = ui.dark_mode(value=True)
    ui.label('Switch mode:')
    with ui.row():
        ui.button('Dark', on_click=dark.enable)
        ui.button('Light', on_click=dark.disable)
    ui.input(label='User Name', placeholder='User').bind_value(data, 'user_name').classes('w-full')
    ui.button('Reset', on_click=reset_dialog.open).style('width: 20%')

# ui.run(on_air=os.environ['ON_AIR_IO_KEY'])
ui.run(title='Super Screenplay Assistant 3000')
