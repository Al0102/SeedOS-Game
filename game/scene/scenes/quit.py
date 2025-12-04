"""
Pre quit scene.
"""
from time import sleep

from game.ansi_actions.style import style
from game.terminal.screen import clear_screen


def qet_quit_scene():
    """
    Return the data dictionary for the quit scene.

    Scene data dictionaries have the form:
    {
        "name": <string>,
        "open": <function or None>,
        "update": <function or None>,
        "exit": <function or None>
    }

    :postcondition: get data for the quit scene
    :return: a dictionary representing the data for the quit scene
    """

    def update_quit(_):
        """
        Return the next scene to run after the seedOS console.

        None is returned to signify program exit.

        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        # save data
        # play quit animation
        clear_screen()
        print(style("Shutting down...", "red"))
        sleep(1)
        print("See you next time!")
        return None

    return {
        "open": None,
        "update": update_quit,
        "exit": None
    }
