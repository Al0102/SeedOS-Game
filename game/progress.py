"""
Keep track of player progression
"""
from game.ansi_actions.style import style
from game.seedOS.console import send_messages, send_message, press_any_key_to_continue
from game.terminal.screen import clear_screen


def handle_progress(game_data: dict) -> None | str:
    """
    Handle game progress.

    Progress points include:
        just_loaded,
        new_user,
        autosave_enabled,
        read_welcome,
        read_aphid_tutorial,
        challenge_loss,
        challenge_win,
        max_privilege

    :param game_data: a dictionary representing the data needed to run the game
    :precondition: game_data must be a well-formed dictionary of game data with the key-value pair,
                       "progress": <set>
    :postcondition: handle what happens at each progress point
    :return: None or a string representing the scene to change to
    """
    progress = game_data["progress"]
    if "just_loaded" in progress:
        game_data["seed_system"]["message_history"].clear()
        welcome_message(game_data)
        if "new_user" in progress:
            new_user_welcome_instructions(game_data)
    if {"new_user", "read_Welcome"} <= progress:
        new_user_read_welcome(game_data)
    if "read_aphid_README" in progress and game_data["seed_system"]["aphid"]["privilege"] == 1:
        new_user_readme_aphid_tutorial(game_data)
    if "challenge_loss" in progress:
        return handle_loss(game_data)
    return None


def unlock_privilege(game_data: dict, level: int) -> None:
    """
    Unlock privilege for the APHID at <level>.

    :param game_data: a dictionary representing the data needed to run the game
    :param level: a positive integer greater than 0 representing the privilege level to give the aphid
    :precondition: game_data must be a well-formed dictionary of game data
    :precondition: level must be a positive integer greater than 0
    :postcondition: update user's privilege
    """
    new_privilege_level = max(level, game_data["seed_system"]["aphid"]["privilege"])
    game_data["seed_system"]["aphid"]["privilege"] = new_privilege_level
    send_messages(game_data["seed_system"], (
        "",
        style("Unlocking access...", 'yellow'),
        "...",
        style(f"APHID has unlocked privilege level {new_privilege_level}!", "black", "background_yellow")))


def welcome_message(game_data: dict) -> None:
    """
    Say welcome to user on startup.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition: game_data must be a well-formed dictionary of game data
    :postcondition: display welcome message and remove "just_loaded" progress point
    """
    game_data["progress"].remove("just_loaded")
    send_message(
        game_data["seed_system"],
        f"Welcome, {style(game_data['seed_system']['aphid']['name'], 'green')}")


def new_user_welcome_instructions(game_data: dict) -> None:
    """
    Say welcome instructions to new user on startup.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition: game_data must be a well-formed dictionary of game data
    :postcondition: display welcome instructions for new users
    """
    send_messages(game_data["seed_system"], (
        f"Hello {style('beta tester!', 'bold', 'yellow')}",
        "Welcome to SeedOS.",
        "To get setup with your new operating system,",
        f"enter '{style('help', 'bold', 'magenta')}' for information about commands.",
        f"When you're ready, take a '{style('look', 'bold', 'yellow')}' inside Welcome.txt",
        "for important information."))


def new_user_read_welcome(game_data: dict) -> None:
    """
    Unlock level 1 privileges after reading Welcome.txt.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition: game_data must be a well-formed dictionary of game data
    :postcondition: update user's privilege after reading the welcome message
    """
    game_data["progress"].remove("new_user")
    unlock_privilege(game_data, 1)
    send_messages(game_data["seed_system"], (
        "You now have access to changing directories!",
        f"Use \'{style('help', 'bold', 'magenta')} cd\' for more information",
        "When you're ready, head over to applications/tutorial to unlock more commands."))
    press_any_key_to_continue(game_data)


def new_user_readme_aphid_tutorial(game_data: dict) -> None:
    """
    Unlock level 2 privileges after reading aphid tutorial README.txt.

    :param game_data: a dictionary representing the data needed to run the game
    :precondition: game_data must be a well-formed dictionary of game data
    :postcondition: update user's privilege after reading the aphid tutorial message
    """
    unlock_privilege(game_data, 2)
    send_messages(game_data["seed_system"], (
        "You now have access to running commands with 'do'!",
        f"Use \'{style('help', 'bold', 'magenta')} do\' for more information",
        "When you're ready, 'do aphid_tutorial.sprout' to try it out!"))
    press_any_key_to_continue(game_data)


def handle_loss(game_data: dict) -> None | str:
    game_data["seed_system"]["aphid"]["stability"] -= 0.1
    send_messages(game_data["seed_system"], (
        style("APHID corrupted...", "red"),
        style("Stability lost: 10%", "red"),
        style(f"APHID stability: {game_data['seed_system']['aphid']['stability'] * 100}%", "red") ))
    if game_data["seed_system"]["aphid"]["stability"] <= 0:
        return handle_death(game_data)
    return None


def handle_death(game_data: dict) -> None | str:
    clear_screen()
    send_messages(game_data["seed_system"], (
        style("APHID stability: 0%", "red"),
        style("APHID corrupted...", "red"),
        style("Shutting down...", "red")))
    press_any_key_to_continue(game_data)
    return "main_menu"


def handle_win(game_data: dict) -> None:
    memory_gained = game_data["seed_system"]["active_file"]["data"]["difficulty"] * 10
    game_data["seed_system"]["aphid"]["memory"] += memory_gained
    send_messages(game_data["seed_system"], (
        "You beat the challenge!",
        f"+{memory_gained}kB of memory!"))
