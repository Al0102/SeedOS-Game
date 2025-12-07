"""
Primary game loop for file navigation.
"""
from io import StringIO
from sys import stderr

from game.ansi_actions.style import style
from game.terminal.draw import create_text_area, draw_text_box
from game.terminal.input import poll_key_press
from game.terminal.screen import clear_screen, get_screen_size
from game.seedOS.command import send_command
from game.seedOS.console import display_message_history, send_message, send_messages, \
    do_validated_prompt


def get_seedos_look_scene():
    """
    Return the data dictionary for the seedOS look scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS look scene
    :return: a dictionary representing the data for the seedOS look scene
    """
    hints_text = (
            style('Up/Down to scroll through lines', 'yellow') +
            f"\n{style('q to quit', 'red')}")
    file_text = "Nothing's here..."
    read_index = 0

    def open_seedos_look(game_data: dict) -> None:
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS look
        """
        nonlocal file_text, read_index
        clear_screen()
        display_message_history(game_data["seed_system"])
        actual_file_path = game_data["seed_system"]["active_file"]["data"]["text_src"]
        try:
            with open(actual_file_path, "r") as actual_file:
                file_text = actual_file.readlines()
        except FileNotFoundError:
            print(f"|System Error|\nCannot find text file: {actual_file_path}", file=stderr)
            file_text = "File Corrupted"
        read_index = 0
        send_messages(game_data["seed_system"], (
            f"Opening: {style(game_data['seed_system']['active_file']['name'], 'yellow')}",
            "Done!"), 1)

    def exit_seedos_look(game_data):
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: exit the seedOS look scene
        """
        clear_screen()
        handle_progress(game_data)

    def update_seedos_look(game_data):
        """
        Return the next scene to run after the seedOS look.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS look scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        nonlocal read_index
        while True:
            clear_screen()
            # Hints text box
            draw_text_box(
                column=4, row=get_screen_size()[1] - 3, width=get_screen_size()[0], height=3,
                text=hints_text, overwrite=True)
            # Messages text box
            messages_height = get_screen_size()[1] - 5
            displayed_text = file_text[read_index:min(read_index + messages_height, len(file_text))]
            draw_text_box(
                column=4, row=1, width=get_screen_size()[0], height=messages_height,
                text="".join(displayed_text), overwrite=True)
            # Input
            inputted = poll_key_press(game_data["key_input"])
            if inputted == "up":
                read_index = max(0, read_index - 1)
            if inputted == "down":
                read_index = max(0, min(len(file_text) - messages_height, read_index + 1))
            if inputted == "q":
                return "seedos_console"

    return {
        "name": "seedos_look",
        "open": open_seedos_look,
        "update": update_seedos_look,
        "exit": exit_seedos_look}


def handle_progress(game_data):
    progress = game_data["progress"]
    if progress["new_user"] and game_data["seed_system"]["active_file"]["name"] == "Welcome":
        progress["new_user"] = False
        game_data["seed_system"]["aphid"]["privilege"] = max(1, game_data["seed_system"]["aphid"]["privilege"])
        send_messages(game_data["seed_system"], (
            "",
            style("Unlocking access...", 'yellow'),
            "...",
            style("APHID has unlocked privilege level 1!", "black", "background_yellow")))
        send_message(
            game_data["seed_system"],
            style("Press any key to continue", "background_yellow", "black", "rapid_blink"))
        poll_key_press(game_data["key_input"])
