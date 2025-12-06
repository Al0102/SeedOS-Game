"""
Startup boot sequence and cool stuff.
"""
from game.terminal.screen import get_screen_size, clear_screen


def get_startup_scene():
    """
    Return the data dictionary for the startup scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the startup scene
    :return: a dictionary representing the data for the startup scene
    """

    def update_startup(_):
        """
        Return the next scene to run after the startup.

        None is returned to signify program exit.

        :postcondition: run the startup scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            clear_screen()
            print(
                f"Current size: {get_screen_size()} | Adjust to at least (100, 35) for the best experience.\n"
                "Enter 'y' to continue, 'n' to exit, and any key to reload screen size.\n")
            choice = input("> ")
            if choice is None:
                continue
            choice = choice.lower()
            if choice == "y":
                return "main_menu"
            if choice == "n":
                return "quit"

    return {
        "name": "startup",
        "open": None,
        "update": update_startup,
        "exit": None}

