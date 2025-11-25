"""
Helpers for visual customization like text colour and emphasis.
"""


def get_styles():
    """
    Return a dictionary of available styles and their ANSI escape sequences.

    :postcondition: get a dictionary of available styles and their ANSI escape sequences
    :postcondition: the key-value pairs have the form <name>: <sequence> and both are strings
    :return: a dictionary representing the available styles and their ANSI escape sequences.

    >>> get_styles() == {
    ...     "reset": "\\033[0m",
    ...     "bold": "\\033[1m",
    ...     "dim": "\\033[2m",
    ...     "italic": "\\033[3m",
    ...     "underline": "\\033[4m",
    ...     "slow_blink": "\\033[5m",
    ...     "rapid_blink": "\\033[6m",
    ...     "strike": "\\033[9m",
    ...     "normal_intensity": "\\033[22m",
    ...     "not_italic": "\\033[23m",
    ...     "not_underlined": "\\033[24m",
    ...     "not_blinking": "\\033[25m",
    ...     "black": "\\033[30m",
    ...     "red": "\\033[31m",
    ...     "green": "\\033[32m",
    ...     "yellow": "\\033[33m",
    ...     "blue": "\\033[34m",
    ...     "magenta": "\\033[35m",
    ...     "cyan": "\\033[36m",
    ...     "white": "\\033[37m",
    ...     "background_black": "\\033[40m",
    ...     "background_red": "\\033[41m",
    ...     "background_green": "\\033[42m",
    ...     "background_yellow": "\\033[43m",
    ...     "background_blue": "\\033[44m",
    ...     "background_magenta": "\\033[45m",
    ...     "background_cyan": "\\033[46m",
    ...     "background_white": "\\033[47m"}
    True
    """
    return {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        # <-Usually only for Windows Powershell->
        "slow_blink": "\033[5m",
        "rapid_blink": "\033[6m",
        "strike": "\033[9m",
        # <------------------------------------->
        "normal_intensity": "\033[22m",
        "not_italic": "\033[23m",
        "not_underlined": "\033[24m",
        "not_blinking": "\033[25m",
        # Foreground Colours
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        # Background Colours
        "background_black": "\033[40m",
        "background_red": "\033[41m",
        "background_green": "\033[42m",
        "background_yellow": "\033[43m",
        "background_blue": "\033[44m",
        "background_magenta": "\033[45m",
        "background_cyan": "\033[46m",
        "background_white": "\033[47m"
    }


def style(text, *styles, reset=True):
    """
    Return <text> with the style <type> prepended to it.

    The optional <reset> will append the ANSI reset code to <text>

    :param text: a string representing the text to style
    :param reset: a boolean representing whether to reset the styling after <text>
    :param styles: strings representing the styles to apply to <text>
    :precondition: text must be a string representing the text to style
    :precondition: reset a boolean representing whether to reset the styling after <text>
    :precondition: types must be made up of strings found in get_styles()
    :postcondition: prepend and/or append ANSI codes to style the text when printing
    :return: a string representing the styled <text> with appropriate ANSI codes prepended/appended to it

    >>> style("This is red", "red")
    '\\x1b[31mThis is red\\x1b[0m'
    >>> style("This is bold and blue", "bold", "blue")
    '\\x1b[1m\\x1b[34mThis is bold and blue\\x1b[0m'
    >>> style("This is bold and blue and not reset", "bold", "blue", reset=False)
    '\\x1b[1m\\x1b[34mThis is bold and blue and not reset'
    """
    codes = "".join(map(lambda name: get_styles()[name], styles))
    new_text = codes + text
    if reset:
        new_text += get_styles()["reset"]
    return new_text


def reset_style():
    """
    Reset the text style being printed.

    :postcondition: print the reset escape code
    :postcondition: no newline will be printed

    >>> reset_style()
    \\x1b[0m
    """
    print(get_styles()["reset"], end="", flush=True)


def main():
    """
    Drive the program.
    """
    print(style("This is RED", "red"), " --> but not this.")
    print(style("Unless...", "bold", "italic"))
    print(style("This is GREEN", "green", reset=False), " --> reset is False.")

    print("RESET")
    reset_style()

    print(style("Under where?", "underline"))
    print(style("BACKGROUND AND TEXT", "background_yellow", "black"))

    input(style("Remember to blink", "rapid_blink"))
    input(style("But not too fast", "slow_blink"))
    print(style("My eyes hurt and it's hard to see...", "dim"))

    print(style("I have one last secret...", "strike"))


if __name__ == '__main__':
    main()
