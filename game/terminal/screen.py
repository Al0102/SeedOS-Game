"""
Terminal information and manipulation.
"""
import os


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def get_screen_size():
    """
    Get the dimensions of the terminal as a tuple.

    :postcondition: get a tuple representing the width and height of the terminal
    :return: a tuple of two integers representing the width and height of the terminal
    """
    try:
        dimensions = os.get_terminal_size()
    except OSError:
        print("get_screen_size: Invalid terminal, cannot get size.")
        return None
    else:
        return (dimensions.columns, dimensions.lines)


def main():
    """
    Drive the program.
    """
    print("Terminal columns (width) and rows (height)")
    print(get_screen_size())
    print("Clear screen after input...")
    input()
    clear_screen()


if __name__ == '__main__':
    main()