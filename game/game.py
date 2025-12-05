"""
The entry point for the game.
"""
from game.ansi_actions.cursor import set_cursor_visibility
from game.ansi_actions.style import style
from game.save import get_user_data_folder
from game.scene.scene import get_scenes
from game.terminal import input as terminal_input


def setup_game():
    """
    Get the data for running an instance of the game.

    The data is in a dictionary of form:
    {
        "key_input": <terminal input data dictionary>,
        "saves_path": <local save data folder path>,
        "previous_scene": None or <scene data dictionary>,
        "active_scene": <scene data dictionary>,
        "seed_system": None or <seedOS dictionary>,
        "progress": <dictionary of progress statuses>
    }

    :postcondition: get the data needed for the game to run
    :postcondition: create a local user data folder if it does not already exist
    :return: a dictionary representing the data needed for the game to run
    """
    game_data = {
        "key_input": terminal_input.init_key_input(),
        "saves_path": get_user_data_folder(),
        "previous_scene": None,
        "active_scene": get_scenes()["startup"],
        "seed_system": None,
        "progress": {}}
    return game_data


def game_loop(game_data):
    """
    Drive the main game loop.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition game_data: must be a well-formed dictionary of game data
    :postcondition: run the game
    """
    while True:
        if not game_data["active_scene"]["open"] is None:
            game_data["active_scene"]["open"](game_data)
        next_scene = game_data["active_scene"]["update"](game_data)
        if not game_data["active_scene"]["exit"] is None:
            game_data["active_scene"]["exit"](game_data)
        if next_scene is None:
            return
        game_data["previous_scene"] = game_data["active_scene"]
        try:
            game_data["active_scene"] = get_scenes()[next_scene]
        except KeyError:
            print(style(f"Scene is not defined: {next_scene}", "red"))
            return


def main():
    """
    Drive the program.
    """
    game_data = setup_game()
    set_cursor_visibility(show=False)
    try:
        game_loop(game_data)
    finally:
        print(style("Finished!", "reset"))
        set_cursor_visibility(show=True)


if __name__ == "__main__":
    main()

