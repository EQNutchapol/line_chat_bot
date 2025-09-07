import random
import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from linebot.models import TextSendMessage
from build.game_logic import assign_spyfall_roles, assign_taboo_words
from build.config import SPYFALL_LOCATIONS

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

@admin_bp.route("/leaderboard", methods=['POST'])
def show_leaderboard():
    scores_data = request.form.get('scores_data')
    if scores_data:
        scores = json.loads(scores_data)
        ranked_groups = sorted(scores, key=lambda x: x['score'], reverse=True)

        original_groups = game_results_data.get('civilian_groups') or game_results_data.get('groups', [])

        for group in ranked_groups:
            # Find the original group data by matching the integer ID
            original_group = next((g for g in original_groups if g.get('id') == group.get('id')), None)

            # THE FIX IS HERE: We now ensure the full list of player objects is passed.
            if original_group:
                group['players'] = original_group.get('members', original_group.get('players', []))
            else:
                group['players'] = []

        return render_template('leaderboard.html', ranked_groups=ranked_groups)
    return "No score data received.", 400

@admin_bp.route("/new_taboo_game", methods=['POST'])
def start_new_taboo_game():
    """Starts a new round of Taboo with selected groups."""
    global game_results_data
    selected_group_ids = request.form.getlist('selected_groups')

    if not selected_group_ids:
        return "No groups selected. Please go back and select at least one group.", 400

    groups_for_new_round = []
    for group_id in selected_group_ids:
        player_data_json = request.form.get(f"group_{group_id}_players")
        if player_data_json:
            try:
                players_in_group = json.loads(player_data_json)
                groups_for_new_round.append(players_in_group)
            except json.JSONDecodeError:
                return "Error decoding player data.", 400

    if not groups_for_new_round:
        return "Could not find player data for the selected groups.", 400

    results = assign_taboo_words(groups_for_new_round)
    game_results_data = results

    return redirect(url_for('admin.show_results'))

@admin_bp.route("/api/users")
def get_users():
    return jsonify(waiting_users)


@admin_bp.route("/api/clear_lobby", methods=['POST'])
def clear_lobby():
    global game_results_data
    waiting_users.clear()
    game_results_data = {}
    return jsonify({'status': 'success', 'message': 'Lobby cleared.'})

# --- NEW TESTING ENDPOINT ---
# This route is specifically for the test script and does not require a signature.
@admin_bp.route("/api/test/add_user", methods=['POST'])
def test_add_user():
    data = request.get_json()
    user_id = data.get("user_id")
    user_name = data.get("name")
    if user_id and user_name:
        waiting_users[user_id] = user_name
        print(f"Test user added: {user_name} ({user_id})")
        return jsonify({"status": "success", "name": user_name})
    return jsonify({"status": "error", "message": "Missing user_id or name"}), 400


@admin_bp.route("/api/start_game", methods=['POST'])
def start_game():
    global game_results_data
    data = request.get_json()
    player_ids = list(waiting_users.keys())
    num_players = len(player_ids)

    player_names = [waiting_users[uid] for uid in player_ids]
    num_groups = int(data.get('num_spies', 1))

    if num_groups > num_players or num_groups < 1:
        return jsonify(
            {'status': 'error', 'message': f'Invalid number of groups ({num_groups}) for {num_players} players.'})
    if num_groups > len(SPYFALL_LOCATIONS):
        return jsonify({'status': 'error',
                        'message': f'Number of groups ({num_groups}) cannot exceed available locations ({len(SPYFALL_LOCATIONS)}).'})

    assignments, results = assign_spyfall_roles(player_ids, player_names, num_groups)
    game_results_data = results

    for user_id, message in assignments:
        try:
            # line_bot_api.push_message(user_id, TextSendMessage(text=message))
            print("ff")
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    return jsonify({'status': 'success', 'redirect_url': '/results'})

