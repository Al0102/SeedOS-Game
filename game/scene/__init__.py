"""
Game scenes (systems).
"""
from game.scene import startup, main_menu


def init_scenes():
    """
    Return a dictionary of scene data dictionaries for the game.

    :postcondition: get a dictionary of well-formed scene data dictionaries
    :return: a dictionary of scene data dictionaries representing the game's scenes
    """
    return {
        "startup": startup.get_startup_scene(),
        "main_menu": main_menu.get_main_menu_scene(),
    }

