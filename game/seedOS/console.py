"""
Main user interaction with the system via a console.
"""
from collections.abc import Callable
from time import sleep

from game.ansi_actions.style import style
from game.menu import create_menu, get_centered_menu_position
from game.sound.effects import get_effects
from game.terminal.draw import create_text_area, draw_text_box, draw_rectangle
from game.terminal.input import start_text_input, init_key_input, poll_key_press
from game.terminal.screen import get_screen_size, clear_screen


def get_console_dimensions():
    """
    Get the dimensions of the SeedOS simulation console parts within the actual terminal.

    Sizes are in form: (<columns AKA width>, <rows AKA height>)
    The dictionary's keys are as follows:
        "output":  message history (top left)
        "input": user input (bottom)
        "clippy": your virtual assistant (top right)

    :postcondition: get a dictionary of SeedOS simulation console parts and their sizes
    :postcondition: the dictionary will have key-value pairs of the form,
                        <string name>: <tuple of size 2>
    :postcondition: the dictionary's values are in the form (<columns AKA width>, <rows AKA height>)
    :postcondition: the dictionary will have tuples of form (<columns AKA width>, <rows AKA height>)
    :return: a dictionary of SeedOS simulation console part names as strings and their sizes as tuples
    """
    return {
        "output": (max(10, min(4 * get_screen_size()[0] // 4, get_screen_size()[0] - 20)),
                   max(1, get_screen_size()[1] - 4)),
        "input": (max(10, min(80, get_screen_size()[0] - 2)), 3),
        "clippy": (max(14, min(20, get_screen_size()[0] // 4)), max(20, get_screen_size()[1] - 4))
    }


def send_message(seed_system, message):
    """
    Write message(s) to the message history of <seed_system>.

    Split <message> into multiple lines if larger than console output width.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param message: a string representing the message to write to the message history
    :precondition: seed_system must be a dictionary with the key-value pair, "message_history": <list of strings>
    :precondition: message must be a string
    :postcondition: append <message> to the message history of <seed_system>
    :postcondition: the message may be split up if longer than the console output width
    """
    width = get_console_dimensions()["output"][0]
    if len(message) > width:
        seed_system["message_history"].append(message[:width])
        send_message(seed_system, message[width:])
    else:
        seed_system["message_history"].append(message)
    display_message_history(seed_system)


def send_messages(seed_system, messages, delay=0.5):
    """
    Send multiple messages to the console, <delay> seconds apart.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param messages: an iterable of strings representing the messages to write to the console
    :param delay: (default 0.5) a float greater than or equal to 0,
                  representing the seconds to wait between each message write
    :precondition: seed_system must be a dictionary with the key-value pair, "message_history": <list of strings>
    :precondition: message must be a string
    :precondition: delay must be a float greater than or equal to 0
    :postcondition: send and display each string in <messages>, <delay> seconds apart
    :postcondition: append the contents of each string in <messages> to the message history of <seed_system>
    """
    for message in messages:
        send_message(seed_system, message)
        display_message_history(seed_system)
        sleep(delay)


def display_message_history(seed_system, offset=0):
    """
    Display the message history of <seed_system> to the terminal.

    :param seed_system: a dictionary representing the currently active seedOS system
    :param offset: (default 0) an integer greater than or equal to 0,
                   representing the message offset from the latest to start displaying from
    :precondition: seed_system must be a dictionary with the key-value pair, "message_history": <list of strings>
    :precondition: offset must be an integer greater than or equal to 0
    :precondition: string in the history must not have newline characters (\n)
    :postcondition: display the message history of <seed_system> to the terminal
    :postcondition: the first message displayed is <offset> from the most recent message
    :postcondition: messages are displayed bottom to top
    """
    size = get_console_dimensions()["output"]
    message_count = min(
        len(seed_system["message_history"]),
        len(seed_system["message_history"]) - offset,
        size[1])
    # Get messages going back from offset to message_count inclusive
    messages = seed_system["message_history"][-offset - 1:- offset - message_count - 1:-1]
    messages.reverse()
    messages = ["" for _ in range(size[1] - message_count)] + messages
    text_area = create_text_area(
        column=4, row=2, width=size[0], height=size[1],
        text="\n".join(messages))
    draw_text_box(text_area=text_area, overwrite=True)


def draw_user_prompt():
    size = get_console_dimensions()["input"]
    draw_rectangle(
        column=0, row=get_screen_size()[1] - size[1] + 1, width=size[0], height=size[1] + 1,
        flush_output=False)
    draw_text_box(column=1, row=get_screen_size()[1] - 1, width=size[0] - 2, height=1, text="", overwrite=True)


def start_prompt_user():
    """
    Return a function for prompting the user for a command in the SeedOS console.

    :postcondition: start a new user prompt in the console
    :return: a function representing the update call for the prompt
    """
    text_input = start_text_input(
        column=3, row=get_screen_size()[1] - 1, max_width=get_console_dimensions()["input"][0] - 4)
    draw_user_prompt()
    get_effects()["mouse_click"].play(loop=True)
    get_effects()["mouse_click"].pause()

    def update_prompt(key_press):
        """
        Update the text_input for the prompt and draws it's border.

        :param key_press: a string representing the key code of the pressed key input
        :precondition: key_press must be a valid key code string
        :postcondition: update the text input prompt for the user
        :postcondition: the text_input will return a string of the user input or None
        :return: a string representing the result of the text input from the user,
                 or None if the input is unfinished
        """
        get_effects()["mouse_click"].resume()
        sleep(0.05)
        get_effects()["mouse_click"].pause()
        result = text_input(key_press)
        if not result is None:
            get_effects()["mouse_click"].stop()
            draw_user_prompt()
        return result

    return update_prompt


def do_validated_prompt(game_data: dict, is_valid: Callable) -> str:
    """
    Run a validated user prompt in the console.

    :param game_data: a dictionary representing the data needed to run the game
    :param is_valid: a callable function representing the acceptance condition
    :precondition: game_data must be a well-formed dictionary of game data that has "key_input"
    :precondition: is_valid must be a callable function that returns a boolean or Truthy/Falsy value
    :postcondition: get the result of the user prompt
    :return: a string representing the result of the prompt
    """
    prompt_user = start_prompt_user()
    prompt_user("escape")
    while True:
        output = prompt_user(poll_key_press(game_data["key_input"]))
        display_message_history(game_data["seed_system"])
        if output is None:
            continue
        if is_valid(output):
            return output
        else:
            send_message(game_data["seed_system"], "Invalid Input")


def do_menu_prompt(game_data: dict, *options: str, style_name="prompt") -> str:
    """
    Run a menu.

    Styles of menu include:
        "prompt": run inline with the console like a text prompt
        "centered": run centered on the terminal screen
        "position:<column>,<row>": run with a position at <column>, <row>

    :param game_data: a dictionary representing the data needed to run the game
    :param options: strings representing the menu's option names
    :param style_name: (default "prompt") a string representing the alignment style of the menu
    :precondition: game_data must be a well-formed dictionary of game data that has "key_input"
    :precondition: options must hold at least one string
    :precondition: style_name must be a string of name: "prompt" or "centered"
    :postcondition: get the result of the menu prompt
    :postcondition: add padding lines to console message history if <style_name> is "prompt"
    :raises ValueError: if style_nam ei snot a valid menu style
    :return: a string representing the result of the prompt
    """
    if style_name == "prompt":
        position = (4, get_console_dimensions()["output"][1] - len(options) + 1)
        send_messages(game_data["seed_system"], ["" for _ in range(len(options) + 2)], 0)
    elif style_name == "centered":
        position = get_centered_menu_position(*options)
    elif "position" in style_name:
        position = tuple(map(int, style_name.split(":")[1].split(',')))
    else:
        raise ValueError(style("Invalid menu style: {style}"), "red")
    menu = create_menu(*position, *options)
    menu["draw_menu"]()
    while True:
        result = menu["update_menu"](poll_key_press(game_data["key_input"]))
        if not result is None:
            if style_name == "prompt":
                send_message(game_data["seed_system"], result)
            return result


def main():
    """
    Drive the program.
    """
    clear_screen()
    mock_seed = {"message_history": ["Hello", "Welcome to SeedOS:", "Grow the system, Your way"]}
    display_message_history(mock_seed)
    # input()
    display_message_history(mock_seed, 1)
    # input()
    display_message_history(mock_seed, 2)

    key_input = init_key_input()
    update_console_prompt = start_prompt_user()
    while True:
        inputted = poll_key_press(key_input)
        if inputted == "tab":
            break
        result = update_console_prompt(inputted)
        print("", end="", flush=True)
        if result is None:
            continue
        draw_text_box(
            1, 1, get_console_dimensions()["output"][0], 5,
            text=f"\n\n{result}", overwrite=True)
        if result == "quit":
            break
        update_console_prompt = start_prompt_user()


if __name__ == '__main__':
    main()
