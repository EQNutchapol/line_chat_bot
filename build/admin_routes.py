# admin_routes.py
import random
from flask import Blueprint, jsonify, request, render_template
from linebot.models import TextSendMessage
from game_logic import assign_spyfall_roles, assign_insider_roles
from config import SPYFALL_LOCATIONS

admin_bp = Blueprint('admin', __name__, template_folder='../templates')
line_bot_api = None
waiting_users = None
game_results_data = {}


def init_admin(api, users):
    global line_bot_api, waiting_users
    line_bot_api = api
    waiting_users = users


@admin_bp.route("/admin")
def admin_panel():
    return render_template('admin.html')


@admin_bp.route("/results")
def show_results():
    return render_template('results.html', results=game_results_data)


@admin_bp.route("/api/users")
def get_users():
    return jsonify(waiting_users)


@admin_bp.route("/api/clear_lobby", methods=['POST'])
def clear_lobby():
    global game_results_data
    waiting_users.clear()
    game_results_data = {}
    return jsonify({'status': 'success', 'message': 'Lobby cleared.'})


@admin_bp.route("/api/start_game", methods=['POST'])
def start_game():
    global game_results_data
    data = request.get_json()
    game_type = data.get('game')
    player_ids = list(waiting_users.keys())
    num_players = len(player_ids)

    if game_type == 'spyfall':
        num_groups = int(data.get('num_spies', 1))
        if num_groups > len(SPYFALL_LOCATIONS):
            return jsonify({'status': 'error',
                            'message': f'Number of groups ({num_groups}) cannot exceed available locations ({len(SPYFALL_LOCATIONS)}).'})
        if num_groups > num_players or num_groups < 1:
            return jsonify(
                {'status': 'error', 'message': f'Invalid number of groups ({num_groups}) for {num_players} players.'})

        player_names = [waiting_users[uid] for uid in player_ids]

        # The game logic function now returns both messages and results
        assignments, results = assign_spyfall_roles(player_ids, player_names, num_groups)
        game_results_data = results

        # Send messages to players
        for user_id, message in assignments:
            try:
                line_bot_api.push_message(user_id, TextSendMessage(text=message))
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

        return jsonify({'status': 'success', 'redirect_url': '/results'})

    # (Insider logic remains the same for now)
    elif game_type == 'insider':
        # ... insider logic ...
        return jsonify({'status': 'error', 'message': 'Insider results page not implemented.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid game type.'})
