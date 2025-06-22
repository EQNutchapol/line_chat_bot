# run.py
import threading
import time
from flask import Flask
from linebot import LineBotApi, WebhookHandler
from pyngrok import ngrok

# Import config and blueprints
from config import LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, NG_GROK_DOMAIN
from bot_handlers import bot_bp, init_bot
from admin_routes import admin_bp, init_admin

# --- Main App Setup ---
app = Flask(__name__, template_folder='templates')

# Check if credentials are set
if "YOUR_CHANNEL_SECRET" in LINE_CHANNEL_SECRET or "YOUR_CHANNEL_ACCESS_TOKEN" in LINE_CHANNEL_ACCESS_TOKEN:
    print("FATAL ERROR: Please update your LINE credentials in config.py before running.")
    exit()

# --- Global Objects ---
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
waiting_users = {}  # Shared data storage

# --- Initialize and Register Blueprints ---
# Pass the necessary objects to each blueprint
init_bot(handler, line_bot_api, waiting_users)
init_admin(line_bot_api, waiting_users)

app.register_blueprint(bot_bp)
app.register_blueprint(admin_bp)


def run_flask_app():
    # Run Flask app on port 5001
    app.run(port=5001, host="127.0.0.1")


if __name__ == "__main__":
    port = 5001

    # Run Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    time.sleep(2)  # Give the server a moment to start

    try:
        public_url = ngrok.connect(port, domain=NG_GROK_DOMAIN).public_url

        print("--- ngrok tunnel is active ---")
        print(f"!!! IMPORTANT: Webhook URL: {public_url}/callback")
        print(f"Admin Panel: {public_url}/admin")
        print("Press CTRL+C to stop the program.")

        flask_thread.join()

    except Exception as e:
        print(f"An error occurred while starting ngrok: {e}")
