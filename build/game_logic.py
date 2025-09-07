import random
from build.config import SPYFALL_LOCATIONS, CHARADE_WORDS, TABOO_WORDS


def assign_spyfall_roles(player_ids, player_names, num_groups):
    """
    Assigns roles for Spyfall and prepares words and initial scores for each group.
    """

    players = list(zip(player_ids, player_names))
    random.shuffle(players)

    groups = [[] for _ in range(num_groups)]
    for i, player in enumerate(players):
        groups[i % num_groups].append(player)

    message_assignments = []
    game_results = {
        "game_type": "spyfall",
        "spy_group": [],
        "civilian_groups": []
    }

    all_spies = []
    for group in groups:
        if group:
            all_spies.append({"id": group[0][0], "name": group[0][1]})
    game_results["spy_group"] = [spy["name"] for spy in all_spies]

    available_locations = random.sample(list(SPYFALL_LOCATIONS.items()), num_groups)
    shuffled_charades = random.sample(CHARADE_WORDS, len(CHARADE_WORDS))
    shuffled_taboos = random.sample(TABOO_WORDS, len(TABOO_WORDS))

    for i, group in enumerate(groups):
        if not group:
            continue

        location, available_careers = available_locations[i]
        random.shuffle(available_careers)

        charade_words_for_group = shuffled_charades[i * 15: (i + 1) * 15]
        taboo_words_for_group = shuffled_taboos[i * 5: (i + 1) * 5]

        spy_player_id, spy_player_name = group[0]
        civilian_players = group[1:]

        other_spy_names = [s["name"] for s in all_spies if s["id"] != spy_player_id]
        spy_message = "คุณคือ Spy! 🕵️‍♂️\nภารกิจของคุณคือการหาให้ได้ว่าทุกคนอยู่ที่ไหน โดยห้ามให้ใครรู้ว่าคุณคือสปาย"
        if other_spy_names:
            spy_message += f"\n\nสปายในกลุ่มอื่นๆ คือ: {', '.join(other_spy_names)}"
        message_assignments.append((spy_player_id, spy_message))

        civilian_group_details = {
            "id": i + 1,
            "location": location,
            "members": [{"id": spy_player_id, "name": spy_player_name, "role": "Spy"}],
            "charades": charade_words_for_group,
            "taboos": taboo_words_for_group,
            "score": 0
        }

        for j, (civilian_id, civilian_name) in enumerate(civilian_players):
            career = available_careers[j % len(available_careers)]
            civilian_message = f"สถานที่: {location}\nบทบาทของคุณ: {career}"
            message_assignments.append((civilian_id, civilian_message))
            civilian_group_details["members"].append({"id": civilian_id, "name": civilian_name, "role": career})

        game_results["civilian_groups"].append(civilian_group_details)

    return message_assignments, game_results


def assign_taboo_words(groups_of_players):
    """
    Generates words for a new round of Taboo using pre-existing groups of players.
    """
    game_results = {
        "game_type": "taboo",
        "groups": []
    }

    shuffled_charades = random.sample(CHARADE_WORDS, len(CHARADE_WORDS))
    shuffled_taboos = random.sample(TABOO_WORDS, len(TABOO_WORDS))

    for i, group_players in enumerate(groups_of_players):
        if not group_players:
            continue

        charade_words_for_group = shuffled_charades[i * 15: (i + 1) * 15]
        taboo_words_for_group = shuffled_taboos[i * 5: (i + 1) * 5]

        game_results["groups"].append({
            "id": i + 1,
            "players": group_players,  # The players list already contains {'id':..., 'name':...}
            "charades": charade_words_for_group,
            "taboos": taboo_words_for_group,
            "score": 0
        })

    return game_results
