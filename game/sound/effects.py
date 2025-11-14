"""
Play preset sound effects.
"""
from audioplayer import AudioPlayer

from game import relative_path


def get_effect_names():
    return (
        "mouse_click",
    )


def get_effects(path: str = "assets"):
    """
    Return a dictionary of AudioPlayers for sound effects from get_effect_names().

    :param path: a string representing the relative path from the project root
                 default: "assets"
    :precondition: path must be a valid path-like string
    :precondition: get_effect_names must be defined and return a container of strings
    :postcondition: get a dictionary of AudioPlayers for sound effects from get_effect_names()
    :precondition: the sound effects are taken from project_root/<path>
    :postcondition: the dictionary is in the form <sound effect name>: <AudioPlayer object>
    :raise FileNotFoundError: if effect file doesn't exist
    :return: a dictionary with <sound effect name>: <AudioPlayer object> pairs
    """
    return {
        effect_name: AudioPlayer(relative_path(f"{path}/{effect_name}.wav"))
        for effect_name in get_effect_names()}


def main():
    """
    Drive the program.
    """
    get_effects()["mouse_click"].play(block=True)


if __name__ == '__main__':
    main()
