"""
Create new seed system and APHID scene.
"""
from game.ansi_actions.style import style
from game.save import save_data_to_file
from game.seedOS import init_seed_system, init_aphid
from game.seedOS.console import (
    send_messages, do_validated_prompt, do_menu_prompt, press_any_key_to_continue)
from game.terminal.screen import clear_screen


def get_seedos_signup_scene():
    """
    Return the data dictionary for the seedOS signup scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS signup scene
    :return: a dictionary representing the data for the seedOS signup scene
    """

    def open_seedos_signup(game_data):
        """
        Start the signup sequence.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: start the signup sequence
        """
        game_data["seed_system"] = init_seed_system()
        clear_screen()

    def exit_seedos_signup(game_data):
        """
        Cleans the scene before it is switched.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: exit the seedOS signup scene
        """
        game_data["progress"].add("just_loaded")
        game_data["progress"].add("new_user")

    def update_seedos_signup(game_data):
        """
        Return the next scene to run after the seedOS signup.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the seedOS signup scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        # Get user's name
        send_messages(game_data["seed_system"], (
            "Installing seedOS...",
            "Hatching APHID...",
            style("Done!", "green"),
            "Enter your name:"))
        name = do_validated_prompt(
            game_data,
            lambda name_output: len(name_output.strip()) != 0 and not "\033" in name_output)
        game_data["seed_system"]["aphid"] = init_aphid(name)

        # Ask user if they want to save their new game to a file
        send_messages(game_data["seed_system"], (
            style(f"Successfully registered APHID: {name}", "green"),
            "Save game data to file (this will overwrite existing files of the same name)?"))
        confirm_result = do_menu_prompt(
            game_data,
            "Yes", "No need, I'm beating this in one go")
        if confirm_result == "Yes":
            # Display saving success status
            send_messages(game_data["seed_system"], (
                save_data_to_file(game_data),
                "Starting SeedOS..."))
        send_messages(game_data["seed_system"], (
            "Initializing seedOS ecosystem, this may take a while...",
            "Polishing tools... ",
            "Plucking weeds...",
            "Digging holes...",
            "Planting the seed drive...",
            "Feeding the APHID...",
            "Refilling nectar...",
            "Spinning webs...",
            "Letting in sun...",
            "Watching grass grow...",
            "Building ShellSpace...",
            "Done!",
        ), 1)
        press_any_key_to_continue(game_data)

        return "seedos_console"

    return {
        "name": "seedos_signup",
        "open": open_seedos_signup,
        "update": update_seedos_signup,
        "exit": exit_seedos_signup}

