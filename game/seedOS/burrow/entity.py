"""
Entities in a burrow session.
"""
from game.ansi_actions.style import style
from game.seedOS.burrow.action import move_entity


def get_entity_types():
    """
    Get a dictionary of new entities.

    Defined entities:
        "floor",
        "void",
        "wall",
        "small_bug",
        "large_bug",
        "nectar",
        "player"

    :postcondition: a dictionary representing the defined entities
    :return: a dictionary representing the defined entities
    """
    entities = (
        create_entity("floor", style(".", "dim"), on_occupy=None),
        create_entity("void", ""),
        create_entity("wall", "#", health=5),
        create_entity(
            "small_bug", style("*", "red"),
            health=1, base_damage=1, moves=(move_entity, spread_self)),
        create_entity("large_bug", style("@", "red"), health=5, base_damage=3),
        create_entity("nectar", style("n", "yellow"), heal=2),
        create_entity("player", style("n", "green"), health=100))
    return {entity["name"]: entity for entity in entities}


def create_entity(name: str, icon: str, **kwargs) -> dict:
    """
    Create an entity.

    Every entity has a name and icon.

    :param name: a string representing the name of the entity
    :param icon: a string representing the icon to display on the board for the entity
    :param kwargs: a dictionary of entity properties
    :precondition: name must be a string
    :precondition: icon must be a string
    :precondition: position must be a tuple of 2 integers larger than or equal to 1
    :precondition: kwargs must be a dictionary
    :postcondition: create an entity dictionary
    :return: a dictionary representing an entity on a board

    >>> create_entity("wall", "#") == {
    ... "name":  "wall",
    ... "icon": "#"}
    True
    >>> create_entity("small bug", "*", position=(10, 13), health=1, base_damage=1) == {
    ... "name":  "small bug",
    ... "icon": "*",
    ... "position": (10, 13),
    ... "health": 1,
    ... "base_damage": 1}
    True
    """
    return {"name": name, "icon": icon, **kwargs}
