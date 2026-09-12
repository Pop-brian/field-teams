"""
team_generator.py

Responsible for turning a flat list of players into two randomized,
(as-close-to-)equal teams.
"""

import random
from typing import List, Tuple


def shuffle_players(players: List[str]) -> List[str]:
    """Return a new, randomly shuffled copy of the players list."""
    shuffled = players.copy()
    random.shuffle(shuffled)
    return shuffled


def handle_odd_players(shuffled: List[str], extra_to: str = "rotate",
                        rotation_state: int = 0) -> Tuple[List[str], List[str], int]:
    """
    Split a shuffled list into two teams, handling an odd number of players.

    extra_to: "team_a", "team_b", or "rotate"
    rotation_state: which team got the extra player last time (0 = Team A, 1 = Team B).
                    Only used/updated when extra_to == "rotate".

    Returns (team_a, team_b, new_rotation_state)
    """
    n = len(shuffled)
    midpoint = n // 2

    if n % 2 == 0:
        return shuffled[:midpoint], shuffled[midpoint:], rotation_state

    # Odd number of players - one team gets an extra player.
    if extra_to == "team_a":
        team_a = shuffled[: midpoint + 1]
        team_b = shuffled[midpoint + 1:]
        return team_a, team_b, rotation_state

    if extra_to == "team_b":
        team_a = shuffled[:midpoint]
        team_b = shuffled[midpoint:]
        return team_a, team_b, rotation_state

    # Rotate mode: alternate which team gets the extra player each time.
    if rotation_state == 0:
        team_a = shuffled[: midpoint + 1]
        team_b = shuffled[midpoint + 1:]
    else:
        team_a = shuffled[:midpoint]
        team_b = shuffled[midpoint:]

    new_rotation_state = 1 - rotation_state
    return team_a, team_b, new_rotation_state


def generate_teams(players: List[str], extra_to: str = "rotate",
                    rotation_state: int = 0) -> Tuple[List[str], List[str], int]:
    """
    Full pipeline: shuffle players, then split into two teams.

    Returns (team_a, team_b, new_rotation_state)
    """
    shuffled = shuffle_players(players)
    return handle_odd_players(shuffled, extra_to=extra_to, rotation_state=rotation_state)


def team_sizes_preview(num_players: int) -> str:
    """Human-readable 'X vs Y' preview of how teams would split."""
    if num_players == 0:
        return "0 vs 0"
    team_a_size = (num_players + 1) // 2
    team_b_size = num_players // 2
    return f"{team_a_size} vs {team_b_size}"
