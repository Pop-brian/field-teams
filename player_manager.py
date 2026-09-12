"""
player_manager.py

Handles everything related to the list of players:
- adding a single player
- bulk-adding players from a pasted block of text
- removing a player
- removing duplicates
- validating names
"""

from typing import List, Tuple


def validate_name(name: str) -> str:
    """Clean up a raw name string. Returns the cleaned name (may be empty)."""
    return name.strip()


def add_player(players: List[str], name: str) -> Tuple[List[str], str]:
    """
    Try to add a single player to the list.

    Returns (updated_players, message).
    message is empty on success, or explains why nothing was added.
    """
    clean_name = validate_name(name)

    if not clean_name:
        return players, "Player name can't be empty."

    if any(p.lower() == clean_name.lower() for p in players):
        return players, f'⚠️ "{clean_name}" has already been added.'

    return players + [clean_name], ""


def add_players_bulk(players: List[str], text_block: str) -> Tuple[List[str], List[str]]:
    """
    Parse a pasted block of text (one player per line) and add all new,
    non-duplicate names.

    Returns (updated_players, list_of_skipped_names) where skipped names
    were duplicates or blank lines.
    """
    updated = players.copy()
    skipped = []

    for raw_line in text_block.splitlines():
        name = validate_name(raw_line)
        if not name:
            continue
        if any(p.lower() == name.lower() for p in updated):
            skipped.append(name)
            continue
        updated.append(name)

    return updated, skipped


def remove_player(players: List[str], name: str) -> List[str]:
    """Remove a player by exact name match."""
    return [p for p in players if p != name]


def remove_duplicates(players: List[str]) -> List[str]:
    """
    Remove duplicate names (case-insensitive), keeping the first occurrence
    and preserving original order.
    """
    seen = set()
    result = []
    for p in players:
        key = p.lower()
        if key not in seen:
            seen.add(key)
            result.append(p)
    return result


def clear_players() -> List[str]:
    """Return a fresh, empty player list."""
    return []
