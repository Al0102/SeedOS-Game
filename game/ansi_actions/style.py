"""
Helpers for visual customization like text colour and emphasis.
"""


def get_styles():
    """
    Return a dictionary of available styles and their ANSI escape sequences.

    :postcondition: get a dictionary of available styles and their ANSI escape sequences
    :postcondition: the key-value pairs have the form <name>: <sequence> and both are strings
    :return: a dictionary representing the available styles and their ANSI escape sequences.
    """
    return {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "slow_blink": "\033[5m",
        "rapid_blink": "\033[6m",
        "strike": "\033[9m",
        "normal_intensity": "\033[22m",
        "not_italic": "\033[23m",
        "not_underlined": "\033[24m",
        "not_blinking": "\033[25m",

        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",

        "background_black": "\033[40m",
        "background_red": "\033[41m",
        "background_green": "\033[42m",
        "background_yellow": "\033[43m",
        "background_blue": "\033[44m",
        "background_magenta": "\033[45m",
        "background_cyan": "\033[46m",
        "background_white": "\033[47m",
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
    """
    codes = [get_styles()[name] for name in styles]
    new_text = codes + text
    if reset:
        new_text += get_styles()["reset"]
    return codes + text


def main():
    """
    Drive the program.
    """
    print(style("This is RED", "RED", ""))

if __name__ == '__main__':
    main()
