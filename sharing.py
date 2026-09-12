"""
sharing.py

Formats generated teams into human-friendly text for copying or sharing
(e.g. pasting into WhatsApp).
"""

from typing import List


def format_teams(team_a: List[str], team_b: List[str],
                  team_a_name: str = "Team A", team_b_name: str = "Team B") -> str:
    """Simple two-column-style plain text listing of both teams."""
    lines = [f"🟦 {team_a_name}"]
    lines += [f"- {p}" for p in team_a]
    lines.append("")
    lines.append(f"🟥 {team_b_name}")
    lines += [f"- {p}" for p in team_b]
    return "\n".join(lines)


def generate_share_text(team_a: List[str], team_b: List[str],
                         team_a_name: str = "Team A", team_b_name: str = "Team B") -> str:
    """
    Produce the shareable message, styled like the mockup:

    ⚽ TODAY'S TEAMS

    🟦 TEAM A
    1. Brian
    2. John
    ...

    🟥 TEAM B
    1. Kevin
    ...

    Good game! ⚽🔥
    """
    lines = ["⚽ TODAY'S TEAMS", ""]

    lines.append(f"🟦 {team_a_name.upper()}")
    lines += [f"{i}. {p}" for i, p in enumerate(team_a, start=1)]
    lines.append("")

    lines.append(f"🟥 {team_b_name.upper()}")
    lines += [f"{i}. {p}" for i, p in enumerate(team_b, start=1)]
    lines.append("")

    lines.append("Good game! ⚽🔥")

    return "\n".join(lines)


def generate_all_players_text(team_a: List[str], team_b: List[str],
                               team_a_name: str = "Team A", team_b_name: str = "Team B") -> str:
    """
    Interleaved 'All Players' view, in the original shuffle order
    (alternating team_a / team_b entries as they were drawn).
    """
    combined = []
    max_len = max(len(team_a), len(team_b))
    for i in range(max_len):
        if i < len(team_a):
            combined.append((team_a[i], team_a_name))
        if i < len(team_b):
            combined.append((team_b[i], team_b_name))

    lines = [f"{i}. {name} — {team}" for i, (name, team) in enumerate(combined, start=1)]
    return "\n".join(lines)
