"""
Main user interaction with the system via a console.
"""
from game.terminal.draw import create_text_area, draw_text_box, draw_rectangle
from game.terminal.input import start_text_input, init_key_input, pull_input, poll_key_press
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
        "output": (max(10, min(60, get_screen_size()[0] - 20)), max(1, get_screen_size()[1] - 4)),
        "input": (max(10, min(80, get_screen_size()[0] - 2)), 3),
        "clippy": (max(14, min(20, get_screen_size()[0] // 4)), max(20, get_screen_size()[1] - 4))
    }


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
    # TODO move justify to draw.py
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

    :return:
    """
    text_input = start_text_input(
        column=3, row=get_screen_size()[1] - 1, max_width=get_console_dimensions()["input"][0] - 3)
    draw_user_prompt()

    def update_prompt(key_press):
        """
        Update the text_input for the prompt and draws it's border.

        :param key_press: a string representing the key code of the pressed key input
        :precondition: key_press must be a valid key code string
        :postcondition: update the text input prompt for the user
        :postcondition: the text_input will return a string of the user input or None
        :return: a string representing the result of teh text input from the user,
                 or None if the input is unfinished
        """
        draw_user_prompt()
        return text_input(key_press)

    return update_prompt


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
        draw_text_box(1, 1, get_console_dimensions()["output"][0], 5, text=f"\n\n{result}", overwrite=True)
        if result == "quit":
            break
        update_console_prompt = start_prompt_user()


if __name__ == '__main__':
    main()
