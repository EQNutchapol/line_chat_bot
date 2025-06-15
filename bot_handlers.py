# bot_handlers.py
from flask import Blueprint, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# We will pass the 'handler', 'line_bot_api', and 'waiting_users' from the main script
bot_bp = Blueprint('bot', __name__)
handler = None
line_bot_api = None
waiting_users = None

def init_bot(bot_handler, api, users):
    """Initializes the blueprint with necessary objects and registers the message handler."""
    global handler, line_bot_api, waiting_users
    handler = bot_handler
    line_bot_api = api
    waiting_users = users

    # --- THE FIX IS HERE ---
    # We register the handler function here, instead of using a decorator.
    # This ensures `handler` is not None when we call .add()
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message_event(event):
        handle_message(event)

@bot_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# This is now a regular function, not decorated at the module level.
def handle_message(event):
    user_id = event.source.user_id
    user_name = event.message.text.strip()

    if user_id in waiting_users:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"You are already registered as '{waiting_users[user_id]}'. Please wait.")
        )
    else:
        waiting_users[user_id] = user_name
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Hello, '{user_name}'! You have successfully joined the waiting room. Please wait.")
        )