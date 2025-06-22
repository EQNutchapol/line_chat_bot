# game_logic.py
import random
from config import SPYFALL_LOCATIONS, INSIDER_WORDS


def assign_spyfall_roles(player_ids, player_names, num_groups):
    """
    Assigns roles for Spyfall based on groups.
    - Each group gets a unique location and has one spy.
    - All spies know who the other spies are.
    - Returns a tuple containing:
      1. A list of (user_id, message) assignments for the bot to send.
      2. A detailed dictionary of the game results for the admin page.
    """

    players = list(zip(player_ids, player_names))
    random.shuffle(players)

    # Distribute players into groups
    groups = [[] for _ in range(num_groups)]
    for i, player in enumerate(players):
        groups[i % num_groups].append(player)

    # Prepare data structures
    message_assignments = []
    game_results = {
        "spy_group": [],
        "civilian_groups": []
    }

    # First pass: Identify all spies
    all_spies = []
    for group in groups:
        if group:
            all_spies.append({"id": group[0][0], "name": group[0][1]})

    # Add the consolidated spy list to the results
    game_results["spy_group"] = [spy["name"] for spy in all_spies]

    # Second pass: Assign roles, generate messages, and build detailed results
    available_locations = list(SPYFALL_LOCATIONS.items())
    random.shuffle(available_locations)

    for i, group in enumerate(groups):
        if not group:
            continue

        location, available_careers = available_locations[i]
        random.shuffle(available_careers)

        spy_player_id, spy_player_name = group[0]
        civilian_players = group[1:]

        # Create message for the spy
        other_spy_names = [s["name"] for s in all_spies if s["id"] != spy_player_id]
        spy_message = "คุณคือ Spy! 🕵️‍♂️\nภารกิจของคุณและทีมของคุณคือการแทรกซึมกลุ่มอื่น ๆ ให้ครบทุกกลุ่ม โดยห้ามให้ใครรู้ว่าคุณคือ Spy"
        if other_spy_names:
            spy_message += f"\n\nSpy ในกลุ่มอื่น ๆ คือ: {', '.join(other_spy_names)}"
        message_assignments.append((spy_player_id, spy_message))

        # Create civilian group details for the results page
        civilian_group_details = {
            "location": location,
            "members": []
        }

        # Add this group's spy to the group details for display
        civilian_group_details["members"].append(f"{spy_player_name} (Spy)")

        # Create messages and details for civilians
        for j, (civilian_id, civilian_name) in enumerate(civilian_players):
            career = available_careers[j % len(available_careers)]
            civilian_message = f"สถานที่: {location}\nบทบาทของคุณ: {career}"
            message_assignments.append((civilian_id, civilian_message))
            civilian_group_details["members"].append(f"{civilian_name} (Role: {career})")

        game_results["civilian_groups"].append(civilian_group_details)

    return message_assignments, game_results


def assign_insider_roles(player_ids):
    """Assigns roles for Insider and returns a list of (user_id, message) tuples."""
    assignments = []
    secret_word = random.choice(INSIDER_WORDS)
    insider_id = player_ids[0]
    people_ids = player_ids[1:]

    # Insider's message
    insider_message = f"คุณคือ Insider! 🤫\nคำลับคือ: \"{secret_word}\"\nพยายามชี้นำให้คนอื่นทายคำนี้ให้ถูก โดยห้ามให้ใครรู้ว่าคุณรู้คำใบ้"
    assignments.append((insider_id, insider_message))

    # Civilians' message
    civilian_message = "คุณคือชาวบ้านธรรมดา 🙋‍♀️\nร่วมมือกับคนอื่นเพื่อหาคำลับให้เจอ แต่ระวัง! มีคนหนึ่งในพวกเรารู้คำใบ้อยู่แล้ว (Insider)"
    for uid in people_ids:
        assignments.append((uid, civilian_message))

    return assignments
