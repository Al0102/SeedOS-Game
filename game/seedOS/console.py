"""
Main user interaction with the system via a console.
"""
from game.terminal import draw
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
    text_area = draw.create_text_area(
        4, 2, size[0], size[1],
        "\n".join(messages))
    draw.draw_text_box(text_area=text_area, overwrite=True)


def draw_prompt():
    pass


def prompt_user():
    pass


def main():
    """
    Drive the program.
    """
    clear_screen()
    mock_seed = {"message_history": ["Hello", "Welcome to SeedOS:", "Grow the system, Your way"]}
    display_message_history(mock_seed)
    input()
    display_message_history(mock_seed, 1)
    input()
    display_message_history(mock_seed, 2)


if __name__ == '__main__':
    main()