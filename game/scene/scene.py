"""
Main scene manager.
"""
from game.scene.scenes import (
    startup, main_menu, quit,
    seedos_signup, seedos_login, seedos_console, seedos_shutdown, seedos_look, seedos_burrow
)


def init_scenes():
    """
    Return a dictionary of scene data dictionaries for the game.

    :postcondition: get a dictionary of well-formed scene data dictionaries
    :return: a dictionary of scene data dictionaries representing the game's scenes
    """
    return {
        "startup": startup.get_startup_scene(),
        "main_menu": main_menu.get_main_menu_scene(),
        "quit": quit.qet_quit_scene(),
        "seedos_login": seedos_login.get_seedos_login_scene(),
        "seedos_signup": seedos_signup.get_seedos_signup_scene(),
        "seedos_console": seedos_console.get_seedos_console_scene(),
        "seedos_shutdown": seedos_shutdown.get_seedos_shutdown_scene(),
        "seedos_look": seedos_look.get_seedos_look_scene(),
        "seedos_burrow": seedos_burrow.get_seedos_burrow_scene(),
        # "seedos_unlock": seedos_look.get_seedos_look_scene()
    }



def get_scenes(scenes={}):
    """
     Return a dictionary of scene data dictionaries.

    Initializes persistent scene data if <scenes> is empty from:
    {
        "startup",
        "main_menu",
        "seedos_login"
        "seedos_console",
    }

    :param scenes: a dictionary representing the game's scenes
    :precondition: scenes must be a dictionary
    :postcondition: get <scenes> updated with predefined scene dictionaries if they don't already exist
    :return: a dictionary representing the combined group of sound effects

    >>> get_scenes() == init_scenes()
    True
    >>> existing_scenes = {"scene_1": {"name": "scene_1"}}
    >>> get_scenes(existing_scenes) == existing_scenes.update(init_scenes())
    True
    """
    if not set(init_scenes()) <= set(scenes):
        scenes.update(init_scenes())
    return scenes

