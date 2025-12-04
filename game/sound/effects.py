"""
Play preset sound effects.
"""
import random

from audioplayer import AudioPlayer

from game import relative_path


def get_effect_names():
    """
    Return a tuple of existing sound effect names.

    :postcondition: get the names of existing sound effects
    :return: a tuple representing the names of existing sound effects

    >>> get_effect_names() == (
    ... "mouse_click",
    ... "honk")
    True
    """
    return (
        "mouse_click",
        "honk",
        "music"
    )


def init_effects(path="assets"):
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


def get_effects(sound_effects={}):
    """
     Return a dictionary of AudioPlayers.

    Initializes persistent AudioPlayers if <sound_effects> is empty.

    :param sound_effects: a dictionary representing the group of sound effects to add to
    :precondition: sound_effects must be a dictionary
    :postcondition: get <sound_effects> updated with predefined AudioPlayers if they don't already exist
    :return: a dictionary representing the combined group of sound effects
    """
    if not set(init_effects()) <= set(sound_effects):
        sound_effects.update(init_effects())
    return sound_effects


def chance_sound(effect_name, chance, sound_effects=None):
    """
    Play a sound effect based on random chance.

    Can be used to space sounds out or make more natural rhythms.

    :param effect_name: a string representing the name of the effect to play
    :param chance: a float representing the chance from [0, 1] that the sound effect will be played
    :param sound_effects: a dictionary representing the group of sound effects to add to
    :precondition: effect_name must be a string in the keys of the effects dictionary being used
    :precondition: sound_effects must be a valid, non-empty dictionary of form: <name>: <AudioPlayer>,
                   or None if using the default effects dictionary
    :postcondition: play <effect name> from <sound_effects> or default dictionary based on <chance>
    """
    if random.random() < chance:
        if sound_effects:
            sound_effects[effect_name].play(block=False)
        else:
            get_effects()[effect_name].play(block=False)


def main():
    """
    Drive the program.
    """
    for sound_effect in get_effects().values():
        sound_effect.play(block=True)

    input()
    get_effects()["mouse_click"].play()
    input()
    get_effects()["mouse_click"].play()
    input()
    get_effects()["mouse_click"].play()
    input()


if __name__ == '__main__':
    main()
