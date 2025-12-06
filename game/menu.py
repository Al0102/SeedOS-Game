"""
Option menus.
"""
from collections import deque

from game.sound.effects import get_effects
from game.terminal.draw import create_text_area, draw_text_box
from game.terminal.input import init_key_input, pull_input
from game.terminal.screen import clear_screen, get_screen_size
from game.utilities import longest_string, remove_escape_codes


def create_menu(column, row, *options, default=0):
    """
    Generate a menu and its control functions.

    Return a dictionary of form:
    {
        "next_option": <function>
        "previous_option": <function>
        "draw_menu": <function>
    }

    :param column: a positive integer greater than 0 representing
                          the horizontal position to draw the menu at
    :param row: a positive integer greater than 0 representing
                       the vertical position to draw the menu at
    :param options: strings representing the menu's option names
    :param default: (default 0) an integer representing the index of the default selected option
    :precondition: center_column must be a positive integer greater than 0
    :precondition: center_row must be a positive integer greater than 0
    :precondition: options must only hold strings
    :precondition: default must be an integer
    :precondition: options must hold at least one string
    :postcondition: generate a menu and its control functions
    :postcondition: generate a menu and its control functions
    :return: a dictionary representing a menu's control functions
    """
    selected_index = len(options) // 2
    longest_option = longest_string(options)[1]
    options = deque(options)
    options.rotate(selected_index - default)
    text_area = create_text_area(
        column=min(column, get_screen_size()[0] - longest_option - 4),
        row=min(row, get_screen_size()[1] - len(options)),
        width=longest_option + 4, height=len(options) + 1,
        text="")

    def update_menu(key_press):
        """
        Update the menu based on the input.

        :precondition: the menu must be well-formed
        :postcondition: update the menu
        :postcondition: draw the menu to the terminal
        """
        if key_press == "up":
            previous_option()
        elif key_press == "down":
            next_option()
        elif key_press in (" ", "enter"):
            return options[selected_index]
        else:
            get_effects()["honk"].play()
        draw_menu()
        return None

    def draw_menu():
        """
        Draw the menu.

        :precondition: the menu must be well-formed
        :postcondition: draw the menu to terminal
        :postcondition: menu is vertical
        """
        nonlocal text_area
        options_draw = options.copy()
        options_draw[selected_index] = f"< {options_draw[selected_index]} >"
        text_area["text"] = '\n'.join(map(lambda option: option.ljust(longest_option + 4), options_draw))
        draw_text_box(text_area=text_area, overwrite=True)

    def next_option():
        """
        Shift the selected menu option to one forward.

        :precondition: the menu must be well-formed
        :postcondition: shift the selected menu option to one forward
        :postcondition: the selected menu option cycles
        """
        nonlocal options
        options.rotate(-1)

    def previous_option():
        """
        Shift the selected menu option to one previous.

        :precondition: the menu must be well-formed
        :postcondition: shift the selected menu option to one previous
        :postcondition: the selected menu option cycles
        """
        nonlocal options
        options.rotate(1)

    return {
        "next_option": next_option,
        "previous_option": previous_option,
        "draw_menu": draw_menu,
        "update_menu": update_menu}


def get_centered_menu_position(*options):
    options = list(map(remove_escape_codes, options))
    menu_column = get_screen_size()[0] // 2 - longest_string(options)[1] - 4
    menu_row = (get_screen_size()[1] - len(options)) // 2
    return (menu_column, menu_row)


def main():
    """
    Drive the program.
    """
    key_input = init_key_input()
    test_menu = create_menu(
        5, 2,
        "Say Hi", "Say Bye", "Exit")
    clear_screen()
    test_menu["draw_menu"]()
    while True:
        if key_input["key_get"](key_input) in ("escape", "tab"):
            return
        inputted = pull_input(key_input, flush=True)[0]
        selected = test_menu["update_menu"](inputted)
        if selected == "Exit":
            return
        elif selected == "Say Hi":
            print("\033[6;1H Hi ", end="", flush=False)
        elif selected == "Say Bye":
            print("\033[6;1H Bye", end="", flush=False)
        else:
            print("\033[6;1H ...", end="", flush=False)
        print(end="", flush=True)


if __name__ == '__main__':
    main()