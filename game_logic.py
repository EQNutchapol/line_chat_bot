# game_logic.py
import random
from config import SPYFALL_LOCATIONS, INSIDER_WORDS


def assign_spyfall_roles(player_ids, player_names, num_groups):
    """
    Assigns roles for Spyfall based on groups.
    - Each group gets a *unique* location.
    - If num_groups < total locations, some locations will be unused.
    """
    assignments = []

    # Combine player IDs and names, then shuffle them for random group assignment.
    players = list(zip(player_ids, player_names))
    random.shuffle(players)

    # Distribute players into groups in a round-robin fashion for equal distribution.
    groups = [[] for _ in range(num_groups)]
    for i, player in enumerate(players):
        groups[i % num_groups].append(player)

    # Get all available locations and shuffle them to ensure randomness.
    # This is the key part of the new logic.
    available_locations = list(SPYFALL_LOCATIONS.items())
    random.shuffle(available_locations)

    # Process each group, assigning a unique location from the shuffled list.
    for i, group in enumerate(groups):
        if not group:  # Skip if a group happens to be empty.
            continue

        # Assign a unique, shuffled location to each group.
        location, available_careers = available_locations[i]
        random.shuffle(available_careers)  # Shuffle careers for random assignment.

        # The first person in the shuffled group list becomes the spy.
        spy_player_id, spy_player_name = group[0]

        # All other players in the group are civilians.
        civilian_players = group[1:]

        # Generate and store the assignment message for the spy.
        spy_message = "คุณคือ Spy! 🕵️‍♂️\nภารกิจของคุณคือการหาให้ได้ว่าทุกคนอยู่ที่ไหน โดยห้ามให้ใครรู้ว่าคุณคือสปาย"
        assignments.append((spy_player_id, spy_message))

        # Generate and store assignments for all civilians in the group.
        for j, (civilian_id, civilian_name) in enumerate(civilian_players):
            # Assign a unique career. If we run out of unique careers, cycle them.
            career = available_careers[j % len(available_careers)]
            civilian_message = f"สถานที่: {location}\nบทบาทของคุณ: {career}"
            assignments.append((civilian_id, civilian_message))

    return assignments


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
