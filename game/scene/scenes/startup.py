"""
Startup boot sequence and cool stuff.
"""
from game.terminal.draw import create_text_area, draw_text_box
from game.terminal.input import pull_input, start_text_input, poll_key_press
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
    prompt_text_area = create_text_area(column=1, row=1, width=get_screen_size()[0], height=2, text="")
    update_confirm_prompt = start_text_input(3, 3)

    def open_startup(_):
        """
        Start text input for screen size confirmation.

        :postcondition: start text_input for screen size confirmation
        """
        nonlocal update_confirm_prompt
        clear_screen()
        update_confirm_prompt = start_text_input(3, 3)
        update_confirm_prompt("escape")

    def update_startup(game_data):
        """
        Return the next scene to run after the startup.

        None is returned to signify program exit.

        :param game_data: a dictionary representing the data needed to run the game
        :precondition game_data: must be a well-formed dictionary of game data
        :postcondition: run the startup scene
        :postcondition: return the next scene to run, or None for game exit
        :return: a string representing the name of the next scene to run,
                 or None to signify game exit
        """
        while True:
            prompt_text_area["text"] = (
                f"Current size: {get_screen_size()} | Adjust to at least (100, 35) for the best experience.\n"
                "Enter 'y' to continue, 'n' to exit, and any key to reload screen size.\n"
                "> ")
            draw_text_box(text_area=prompt_text_area, overwrite=True)
            poll_key_press(game_data["key_input"])
            inputted = pull_input(game_data["key_input"], flush=True)[0]
            choice = update_confirm_prompt(inputted)
            if choice is None:
                continue
            choice = choice.lower()
            if choice == "y":
                return "main_menu"
            if choice == "n":
                return "quit"
            else:
                open_startup(game_data)

    return {
        "name": "startup",
        "open": open_startup,
        "update": update_startup,
        "exit": None}

