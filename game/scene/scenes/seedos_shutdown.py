"""
Save and shutdown seedOS, then return to main main menu.
"""
from game.ansi_actions.style import style
from game.save import save_data_to_file
from game.sound.effects import get_effects
from game.seedOS.console import (
    display_message_history, draw_user_prompt,
    send_message, send_messages, do_validated_prompt)


def get_seedos_shutdown_scene():
    """
    Return the data dictionary for the seedOS shutdown scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the seedOS shutdown scene
    :return: a dictionary representing the data for the seedOS shutdown scene
    """

    def open_seedos_shutdown(game_data):
        """
        Reset the menu.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: open the seedOS shutdown scene
        """
        draw_user_prompt()
        display_message_history(game_data["seed_system"])

    def update_seedos_shutdown(game_data):
        """
        Return the next scene to run after the seedOS shutdown.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        # Get save preference
        send_messages(game_data["seed_system"], (
            "Getting ready to shutdown system...",
            style("Save game to file (this will overwrite the existing save data)? (yes/no)", "red")))
        confirm_save = do_validated_prompt(
            game_data,
            lambda choice: choice.strip().lower() in ("yes", "no")).strip().lower()
        if confirm_save == "yes":
            send_message(game_data["seed_system"], save_data_to_file(game_data))
        else:
            send_message(game_data["seed_system"], "Did not save data.")
        # Confirm shutdown
        send_messages(game_data["seed_system"], (
            "Choice confirmed.",
            style("Are you sure you want to shut down SeedOS? (yes/no)", "red")))
        confirm_shutdown = do_validated_prompt(
            game_data,
            lambda choice: choice.strip().lower() in ("yes", "no")).strip().lower()
        if confirm_shutdown == "yes":
            return "main_menu"
        else:
            send_messages(game_data["seed_system"], (
                "Canceling shutdown...",
                "Done!"))
            return "seedos_console"

    return {
        "name": "seedos_shutdown",
        "open": open_seedos_shutdown,
        "update": update_seedos_shutdown,
        "exit": None}
