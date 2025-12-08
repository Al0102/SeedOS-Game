"""
Primary game loop for file navigation.
"""
from game.ansi_actions.style import style
from game.progress import handle_progress
from game.terminal.screen import clear_screen
from game.seedOS.command import send_command
from game.seedOS.console import display_message_history, start_prompt_user, send_message, send_messages, \
    do_validated_prompt


def get_seedos_console_scene():
    """
    Return the data dictionary for the seedOS console scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS console scene
    :return: a dictionary representing the data for the seedOS console scene
    """
    status = None

    def open_seedos_console(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS console
        """
        nonlocal status
        clear_screen()
        status = handle_progress(game_data)
        game_data["seed_system"]["active_program"] = None
        game_data["seed_system"]["active_file"] = None
        display_message_history(game_data["seed_system"])

    def update_seedos_console(game_data):
        """
        Return the next scene to run after the seedOS console.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS console scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        if status:
            return status
        while True:
            inputted_prompt = do_validated_prompt(game_data, None)
            if inputted_prompt is None:
                continue
            result = send_command(game_data["seed_system"], inputted_prompt)
            if result["code"] == "success" and game_data["seed_system"]["active_program"]:
                send_message(
                    game_data["seed_system"],
                    f"Running... {game_data["seed_system"]["active_program"]}")
                return game_data["seed_system"]["active_program"]
            display_message_history(game_data["seed_system"])

    return {
        "name": "seedos_console",
        "open": open_seedos_console,
        "update": update_seedos_console,
        "exit": None}
