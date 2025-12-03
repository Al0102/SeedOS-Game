"""
Main scene manager.
"""
from game.scene import init_scenes


def get_scenes(scenes={}):
    """
     Return a dictionary of scene data dictionaries.

    Initializes persistent scene data if <scenes> is empty from:
    {
        "startup",
        "main_menu",
        "seedOS_login"
        "seedOS_console",
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

