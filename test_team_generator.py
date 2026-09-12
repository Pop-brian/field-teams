import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.team_generator import generate_teams, handle_odd_players, team_sizes_preview


def test_even_split():
    players = [f"Player{i}" for i in range(10)]
    team_a, team_b, _ = generate_teams(players)
    assert len(team_a) == 5
    assert len(team_b) == 5
    assert sorted(team_a + team_b) == sorted(players)


def test_odd_split_rotate():
    players = [f"Player{i}" for i in range(11)]
    team_a, team_b, rotation1 = generate_teams(players, extra_to="rotate", rotation_state=0)
    assert len(team_a) == 6
    assert len(team_b) == 5
    assert rotation1 == 1

    team_a2, team_b2, rotation2 = generate_teams(players, extra_to="rotate", rotation_state=rotation1)
    assert len(team_a2) == 5
    assert len(team_b2) == 6
    assert rotation2 == 0


def test_odd_split_forced_team():
    shuffled = [f"Player{i}" for i in range(7)]
    team_a, team_b, _ = handle_odd_players(shuffled, extra_to="team_b")
    assert len(team_a) == 3
    assert len(team_b) == 4


def test_no_duplicate_or_missing_players():
    players = [f"Player{i}" for i in range(9)]
    team_a, team_b, _ = generate_teams(players)
    combined = team_a + team_b
    assert len(combined) == len(players)
    assert set(combined) == set(players)


def test_team_sizes_preview():
    assert team_sizes_preview(0) == "0 vs 0"
    assert team_sizes_preview(10) == "5 vs 5"
    assert team_sizes_preview(11) == "6 vs 5"
