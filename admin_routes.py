# admin_routes.py
import random
from flask import Blueprint, jsonify, request, render_template
from linebot.models import TextSendMessage
from game_logic import assign_spyfall_roles, assign_insider_roles
from config import SPYFALL_LOCATIONS  # Import location data for validation

admin_bp = Blueprint('admin', __name__, template_folder='templates')
line_bot_api = None
waiting_users = None


def init_admin(api, users):
    """Initializes the blueprint with necessary objects."""
    global line_bot_api, waiting_users
    line_bot_api = api
    waiting_users = users


@admin_bp.route("/admin")
def admin_panel():
    # Flask will now look for 'admin.html' in the 'templates' folder.
    return render_template('admin.html')


@admin_bp.route("/api/users")
def get_users():
    return jsonify(waiting_users)


@admin_bp.route("/api/clear_lobby", methods=['POST'])
def clear_lobby():
    waiting_users.clear()
    print("Admin cleared the lobby.")
    return jsonify({'status': 'success', 'message': 'Lobby cleared.'})


@admin_bp.route("/api/start_game", methods=['POST'])
def start_game():
    data = request.get_json()
    game_type = data.get('game')
    player_ids = list(waiting_users.keys())
    num_players = len(player_ids)
    random.shuffle(player_ids)

    assignments = []
    if game_type == 'spyfall':
        # The number of spies now represents the number of groups.
        num_groups = int(data.get('num_spies', 1))

        # --- NEW VALIDATION ---
        # Prevents setting more groups than available unique locations.
        if num_groups > len(SPYFALL_LOCATIONS):
            return jsonify({'status': 'error',
                            'message': f'Number of groups ({num_groups}) cannot exceed the number of available locations ({len(SPYFALL_LOCATIONS)}).'})

        if num_groups > num_players or num_groups < 1:
            return jsonify(
                {'status': 'error', 'message': f'Invalid number of groups ({num_groups}) for {num_players} players.'})

        player_names = [waiting_users[uid] for uid in player_ids]
        assignments = assign_spyfall_roles(player_ids, player_names, num_groups)

    elif game_type == 'insider':
        if num_players < 3:
            return jsonify({'status': 'error', 'message': 'Insider game requires at least 3 players.'})
        assignments = assign_insider_roles(player_ids)

    else:
        return jsonify({'status': 'error', 'message': 'Invalid game type.'})

    # Send messages to all players
    for user_id, message in assignments:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    waiting_users.clear()
    return jsonify({'status': 'success', 'message': 'Game started!'})
