"""
Pre quit scene.
"""


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

    def update_quit(game_data):
        # save data
        # play quit animation
        return None

    return {
        "open": None,
        "update": update_quit,
        "close": None
    }
