"""
Burrow inside a file.
"""
import copy
import itertools
import random
from sys import stderr

from game.ansi_actions.style import style
from game.seedOS.burrow.burrow import load_board_from_file, draw_board, spawn_entity, get_entity_types
from game.seedOS.burrow.drivers import targeted_action, get_drivers
from game.terminal.draw import draw_text_box
from game.terminal.input import poll_key_press
from game.terminal.screen import clear_screen, get_screen_size
from game.seedOS.console import display_message_history, send_message, send_messages
from game.utilities import get_direction_vectors, sum_vectors


def get_seedos_burrow_scene():
    """
    Return the data dictionary for the seedOS burrow scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS burrow scene
    :return: a dictionary representing the data for the seedOS burrow scene
    """
    status = ""
    board = {}
    aphid_entity = {}
    max_moves_left = 1

    def open_seedos_burrow(game_data: dict) -> None:
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS burrow
        """
        nonlocal status, board, aphid_entity, max_moves_left
        clear_screen()
        display_message_history(game_data["seed_system"])
        file_data = game_data["seed_system"]["active_file"]["data"]
        actual_file_path = file_data["board_src"]
        try:
            with open(actual_file_path, "r") as actual_file:
                board = load_board_from_file(actual_file)
        except FileNotFoundError:
            print(f"|System Error|\nCannot find board file: {actual_file_path}", file=stderr)
            status = "File Corrupted"
        else:
            aphid_entity = spawn_entity(board, file_data["player_spawn"], get_entity_types()["player"])
            aphid_entity["drivers"] = copy.copy(game_data["seed_system"]["aphid"]["drivers"])
            aphid_entity["health"] = aphid_entity["max_health"]
            # Randomize the drivers every burrow session so player has to adapt with different strategies
            random.shuffle(aphid_entity["drivers"])
            # Iterate over cycled drivers
            aphid_entity["moves"] = itertools.cycle(aphid_entity["drivers"])
            # User gets to take as many turns as their current level before the environment turn.
            max_moves_left = len(aphid_entity["drivers"])
            aphid_entity["state"] = "alive"

        send_messages(game_data["seed_system"], (
            f"Running: {style(game_data['seed_system']['active_file']['name'], 'yellow')}",
            "Done!"), 1)

    def exit_seedos_burrow(game_data: dict) -> None:
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: exit the seedOS burrow scene
        """
        clear_screen()
        if aphid_entity["state"] == "win":
            game_data["progress"].add("challenge_win")
            game_data["progress"].add(f"won_{game_data['seed_system']['active_file']['name']}")
        elif aphid_entity["state"] == "dead":
            game_data["progress"].add("challenge_loss")
        else:
            game_data["progress"].add("challenge_exited_unexpectedly")
        game_data["progress"].add(f"did_{game_data['seed_system']['active_file']['name']}")

    def update_seedos_burrow(game_data):
        """
        Return the next scene to run after the seedOS burrow.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS burrow scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            if status:
                send_message(game_data["seed_system"], style("|An error occurred|", "red"))
                return "seedos_console"
            clear_screen()
            player_turn(game_data, board, aphid_entity, max_moves_left)
            environment_turn(board, aphid_entity, aphid_entity["position"])
            if aphid_entity["state"] != "alive":
                return "seedos_console"

    return {
        "name": "seedos_burrow",
        "open": open_seedos_burrow,
        "update": update_seedos_burrow,
        "exit": exit_seedos_burrow}


def player_turn(game_data, board, player, max_moves):
    moves_left = max_moves
    while moves_left > 0:
        current_action = next(player["moves"])
        draw_board(board, (3, 1))
        display_player_stats(player, current_action, moves_left)
        inputted = poll_key_press(game_data["key_input"])
        try:
            action_direction = get_direction_vectors()[inputted]
        except KeyError:
            continue
        get_drivers()[current_action](board, player, sum_vectors(action_direction, player["position"]))
        moves_left -= 1


@targeted_action
def environment_turn(board, source_entity, target_entities):
    for target in target_entities:
        if target["type"] == "pickup":
            source_entity["health"] += target["heal"]
        elif target["type"] == "corruption":
            source_entity["health"] -= target["base_damage"]
            if source_entity["health"] <= 0:
                source_entity["state"] = "dead"
        elif target["type"] == "goal" and source_entity["name"] == "player":
            source_entity["state"] = "win"
        else:
            continue


def display_player_stats(player, move, moves_left):
    """
    Display the current player stats to the screen.

    :param player: a dictionary representing the player entity
    :param move: a string representing the current action being taken by teh player
    :param moves_left: an integer representing the moves left in the player's current turn
    :precondition: player must be a dictionary with the key-value pairs
                       "drivers": <list of strings>
                       "health": <integer>
                       "max_health": <integer>
    :precondition: move must be a string
    :precondition: moves_left must be an integer
    :postcondition: display the player's stats to the screen
    """
    window = get_screen_size()
    text = (
        f"Goal: End your turn on the {style('G', 'yellow')}\n"
        f"Current Action: {style(move, 'blue')}\n"
        f"All Actions: {' -> '.join((player['drivers']))}\n"
        f"Actions Left: {moves_left}\n"
        f"APHID HP: {
        style(str(player['health']), 'green' if player['health'] > 5 else 'red')}/{player['max_health']}\n")
    draw_text_box(column=4, row=window[1] - 6, width=window[0], height=6, text=text)

