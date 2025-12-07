"""
Burrow board functions.
"""
import itertools
from io import StringIO
from sys import stderr
from typing import TextIO

from game.ansi_actions.cursor import cursor_set
from game.seedOS.burrow.entity import get_entity_types, create_entity
from game.terminal.screen import point_within_screen, clear_screen
from game.utilities import sum_vectors, remove_escape_codes


def spawn_entity(board: dict, position: tuple, name=None, entity=None) -> dict | None:
    """
    Spawn an entity on the board.

    :param board: a dictionary with position keys representing the board.
    :param position: a tuple of two positive integers larger than 0 representing the spawn position of the entity
    :param name: (default None) a string representing the name of the entity to spawn
    :param entity: (default None) a dictionary representing entity to spawn
    :precondition: board must be a dictionary of form <position tuple>: <entity dictionary>
    :precondition: position must be a tuple of 2 positive integers larger than 0
    :precondition: name must be a string or None
    :precondition: name must be a defined entity in get_entity_types()
    :precondition: entity must be a dictionary of entity data with at least these key-value-pairs:
                   "name": <string> and "icon": <string>
    :precondition: either <name> or <entity> must have a value
    :postcondition: create a new entity of type <name> or spawnat <position> in the board
    :return: a dictionary representing the created enemy if <name> is passed,
             a dictionary representing the passed entity if <entity> is passed,
             or None if the <name> is not a defined entity and <entity> is not passed

    >>> counter = itertools.count()
    >>> new_board = {"entity_id": counter}
    >>> spawn_entity(new_board, (1, 1), name="wall") == {
    ...     'name': 'wall', 'icon': '#', 'health': 5, 'position': (1, 1), 'id': 0}
    True
    >>> spawn_entity(new_board, (1, 1), entity={'name': 'player', 'position': (1, 1)}) == {
    ...     'name': 'player', 'position': (1, 1), 'id': 1}
    True
    >>> new_board == {
    ...     "entity_id": counter,
    ...     (1, 1): [{'name': 'wall', 'icon': '#', 'health': 5, 'position': (1, 1), 'id': 0},
    ...              {'name': 'player', 'position': (1, 1), 'id': 1}]}
    True
    """
    if not name is None:
        try:
            entity = get_entity_types()[name]
        except KeyError:
            print(f"Entity {name} not defined", file=stderr)
    try:
        entity["position"] = position
    except TypeError:
        print(f"Expected <name> or <entity> to be passed, but neither were found", file=stderr)
    else:
        entity["id"] = next(board["entity_id"])
        if not position in board:
            board[position] = []
        board[position].append(entity)
    return entity


def create_board():
    """
    Create an empty board.

    :postcondition: get a dictionary with one key-value pair: "entity_id": itertools.count()
    :postcondition: entity_id will be used to assign each added entity a unique id
    :return: a dictionary with key-value pair: "entity_id": itertools.count(),
             representing the new board
    """
    return {"entity_id": itertools.count()}


def load_board_from_file(board_file: TextIO):
    """
    Create a board with spawned entities based on a text file.

    :param board_file: a TextIO object representing the tilemap to create a board from
    :precondition: board_file must be a TextIO object
    :precondition: get_entity_types must be defined
    :postconditon: create a board from <board_file>
    :postconditon: whitespace ("void" entities) will be ignored
    :postconditon: if character is not the icon for an existing entity,
                   create an entity with a name and icon set to that character
    :return: a dictionary representing the board with entities loaded from <board_file>

    >>> tilemap = StringIO("    ")
    >>> load_board_from_file(tilemap) == {"entity_id": itertools.count()}
    True
    >>> tilemap = StringIO("#")
    >>> load_board_from_file(tilemap) == {
    ...     "entity_id": itertools.count(),
    ...     (1, 1): [{'name': 'wall', 'icon': '#', 'health': 5, 'position': (1, 1)}]}
    True
    >>> tilemap = StringIO(" * \\n   #")
    >>> load_board_from_file(tilemap) == {
    ...     "entity_id": itertools.count(),
    ...     (2, 1): [{'name': 'small_bug', 'icon': '\x1b[31m*\x1b[0m',
    ...              'health': 1, 'base_damage': 1, 'position': (2, 1)}],
    ...     (4, 2): [{'name': 'wall', 'icon': '#', 'health': 5, 'position': (4, 2)}]}
    True
    """
    board = create_board()
    entity_icons = dict(map(
        lambda entity: (remove_escape_codes(entity["icon"]), entity["name"]),
        get_entity_types().values()))
    row = 1
    while line := board_file.readline():
        first_character_index, last_character_index = len(line) - len(line.lstrip()), len(line.rstrip())
        for column, character in enumerate(line[first_character_index:last_character_index], first_character_index):
            try:
                spawn_entity(board, name=entity_icons[character], position=(column + 1, row))
            except KeyError:
                spawn_entity(board, entity=create_entity(name=character, icon=character), position=(column + 1, row))
        row += 1
    return board


def draw_board(board: dict, position_offset=(0, 0), flush=True):
    """
    Draw the values of board to the screen, offset by <position_offset>.

    :param board: a dictionary of entity dictionaries representing the board to draw
    :param position_offset: a tuple of 2 integers larger than or equal to 0,
           representing the position to offset drawing <board> by
    :param flush: (default True) a boolean representing whether to flush the output to stdout
    :precondition: board must be a dictionary of dictionaries with key-value pair: "icon": <string>
    :precondition: position_offset must be a tuple of 2 integers larger than or equal to 0
    :precondition: flush_output must be a boolean
    :postcondition: draw <board> to the screen, offset by <position_offset>
    :postcondition: the entity most recently added to the tile is drawn
    """
    for entities_position, entities in board.items():
        if entities_position == "entity_id":
            continue
        terminal_position = sum_vectors(entities_position, position_offset)
        if all(point_within_screen(terminal_position)):
            cursor_set(*terminal_position)
            print(entities[-1]["icon"], end="")
    print(end="", flush=flush)


def get_entities_at_position(board, position):
    """
    Get the entity data dictionaries at <position> in board.

    Spawn a "void" entity if board has no key: <position>

    :param board: a dictionary of entity dictionaries representing the board to search
    :param position: a tuple of 2 positive integers larger than 0 representing the position to search
    :precondition: board must be a dictionary of dictionaries with key-value pair: "icon": <string>
    :precondition: position must be a tuple of 2 positive integers larger than 0
    :postcondition: get the entities at <position> in <board>,
    :postcondition: spawn a new "void" entity if <position> does not exist yet
    :return: a list of dictionaries representing the data of the entities at <position> in <board>,

    >>> new_board = {(1, 1): [{"name": "floor", "icon": "▯"}]}
    >>> get_entities_at_position(new_board, (1, 1)) == [{"name": "floor", "icon": "▯"}]
    True
    >>> new_board = {(1, 1): [{"name": "floor", "icon": "▯"}, {"name": "small bug", "icon": "*"}]}
    >>> get_entities_at_position(new_board, (1, 1)) == [
    ...     {"name": "floor", "icon": "▯"}, {"name": "small bug", "icon": "*"}]
    True
    >>> new_board = {(1, 1): [{"name": "floor", "icon": "▯"}]}
    >>> get_entities_at_position(new_board, (1, 5)) == [{"name": "void", "icon": ""}]
    False
    """
    try:
        entity = board[position]
    except KeyError:
        entity = spawn_entity(board, position, name="void")
    return entity


def main():
    """
    Drive the program.
    """
    clear_screen()
    draw_board({(1, 1): [{"icon": "a"}]})
    input()
    clear_screen()
    board = load_board_from_file(StringIO(" 1 1 \n  *\n-._.-"))
    draw_board(board)
    input()
    clear_screen()
    board = {}
    spawn_entity(board, name="wall", position=(1, 1))
    spawn_entity(board, name="wall", position=(1, 2))
    draw_board(board)


if __name__ == '__main__':
    main()
