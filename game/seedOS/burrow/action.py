"""
Moves that can be taken during a burrow session.
"""
import itertools
import random
from collections.abc import Callable

from game.ansi_actions.cursor import cursor_set
from game.seedOS.burrow.board import get_entities_at_position, spawn_entity
from game.terminal.screen import clear_screen
from game.utilities import sum_vectors, targets_have_key


def targeted_action(action_function: Callable) -> Callable:
    """
    Decorate an action function to have it be called on a target.

    :param action_function: a function representing an action to be done on a target
    :precondition: action_function must be a function
    :precondition: action_function must have the parameters: source_entity and target_entities
    :postcondition: create a targeted action wrapper for <action_function>
    :return: a wrapper to give <action_function> a target
    """

    def wrapper_action(source_entity: dict, board: dict, position: tuple, *args, **kwargs) -> None:
        targets = get_entities_at_position(board, position)
        action_function(*args, **kwargs, board=board, source_entity=source_entity, target_entities=targets)

    return wrapper_action


@targeted_action
def move_entity(board, source_entity, target_entities):
    if not all(targets_have_key("on_occupy", *target_entities)):
        return
    for target_entity in target_entities:
        if not target_entity["on_occupy"] is None:
            target_entity["on_occupy"](board, source_entity, target_entity)
    board[source_entity["position"]].remove(source_entity)
    target_position = target_entities[0]["position"]
    board[target_position].append(source_entity)
    source_entity["position"] = target_position

@targeted_action
def attack_entity(board, source_entity, target_entities):
    targets = tuple(filter(lambda target: target[0] == True, zip(targets_have_key("hurt"), target_entities)))
    random.choice(targets)[1]["hurt"]()


def main():
    """
    Drive the program.
    """
    clear_screen()
    board = {"entity_id": itertools.count()}
    spawn_entity(board, (1, 1), "floor")
    spawn_entity(board, (1, 2), "floor")
    spawn_entity(board, (1, 3), "floor")
    player = spawn_entity(board, (1, 1), "player")
    spawn_entity(board, (2, 1), "wall")
    spawn_entity(board, (1, 3), "small_bug")
    print(board)
    input()
    move(player, board, sum_vectors(player["position"], (1, 0)))
    print(board)
    input()
    move(player, board, sum_vectors(player["position"], (0, 1)))
    print(board)
    cursor_set(1, 100)



if __name__ == '__main__':
    main()