"""
Main loop for a burrow session.
THIS IS AN EXAMPLE FILE AND INCOMPLETE. REFERENCE scene/seedos_burrow.py for current progress
"""
import copy
import itertools
import random

from game import relative_path
from game.seedOS.burrow.burrow import (
    spawn_entity, get_entity_types, draw_board, load_board_from_file)
from game.seedOS.burrow.drivers import targeted_action, get_drivers
from game.terminal.input import poll_key_press
from game.terminal.screen import clear_screen
from game.utilities import get_direction_vectors, sum_vectors


# Template code
def start_burrow_session(game_data, file_path):
    file = game_data["seed_system"]["file_tree"][file_path]
    try:
        burrow_data = file["data"]["burrow"]
    except KeyError:
        with open(relative_path("assets/default_board.txt"), "r") as board_file:
            board = load_board_from_file(board_file)
        player_spawn = (3, 1)
    else:
        with open(burrow_data["board_src"], "r") as board_file:
            board = load_board_from_file(board_file)
        player_spawn = burrow_data["player_spawn"]
    aphid_entity = spawn_entity(board=board, position=player_spawn, entity=get_entity_types()["player"])
    aphid_entity["drivers"] = copy.copy(game_data["seed_system"]["aphid"]["drivers"])
    # Randomize the drivers every burrow session so player has to adapt with different strategies
    random.shuffle(aphid_entity["drivers"])
    # Iterate over cycled drivers. User gets to take as many turns as their current level before the environment turn.
    aphid_entity["moves"] = itertools.cycle(aphid_entity["drivers"])
    max_moves_left = game_data["seed_system"]["aphid_entity"]["privilege"]
    while True:
        clear_screen()
        draw_board(board)
        moves_left = max_moves_left
        while moves_left > 0:
            current_action = next(aphid_entity["moves"])
            inputted = poll_key_press(game_data["key_input"])
            try:
                action_direction = get_direction_vectors()[inputted]
            except KeyError:
                continue
            current_action(board, aphid_entity, sum_vectors(action_direction, aphid_entity["position"]))
            moves_left -= 1
        environment_turn(board, aphid_entity, aphid_entity["position"])


@targeted_action
def environment_turn(_, source_entity, target_entities):
    for target in target_entities:
        if target["type"] == "pickup":
            source_entity["health"] += target["heal"]
            continue
        if target["type"] == "corruption":
            source_entity["health"] -= target["heal"]
            continue
        if target["type"] == "goal" and source_entity["name"] == "player":
            return "win"
    return None
