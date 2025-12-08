"""
Drivers (actions to take during burrow).
"""
from typing import Callable

from game.seedOS.burrow.burrow import get_entities_at_position, remove_entity


def targeted_action(action_function: Callable) -> Callable:
    """
    Decorate an action function to have it be called on a target.

    :param action_function: a function representing an action to be done on a target
    :precondition: action_function must be a function
    :precondition: action_function must have the parameters: source_entity and target_entities
    :postcondition: create a targeted action wrapper for <action_function>
    :return: a wrapper to give <action_function> a target
    """

    def wrapper_action(board: dict, source_entity: dict, position: tuple, *args, **kwargs) -> None:
        targets = get_entities_at_position(board, position)
        action_function(*args, **kwargs, board=board, source_entity=source_entity, target_entities=targets)

    return wrapper_action


def get_drivers() -> dict:
    """
    Get a dictionary of action functions.

    :postcondition: get all driver names and their function
    :return: a dictionary representing of keys with driver names and values with the driver function
    """
    return {
        "move": move_entity
    }


@targeted_action
def move_entity(board: dict, source_entity, target_entities):
    """
    Move an entity on the map if no solids are in the way.
    """
    if any(map(lambda entity: entity["solid"] == True, target_entities)):
        return
    remove_entity(board, source_entity)
    target_position = target_entities[0]["position"]
    board[target_position].append(source_entity)
    source_entity["position"] = target_position

