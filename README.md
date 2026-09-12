# ⚽ Field Teams

**Random Team Picker** — Randomize. Divide. Play.

Enter players, shuffle, and instantly get two balanced-size, randomized teams.
Built for standing on the field: add players in under 30 seconds, shuffle, and share.

## Features (v1)

- Add players one at a time, or paste a whole list (one name per line)
- Duplicate name detection
- Live player count and team-size preview (e.g. "6 vs 5")
- Random shuffle with equal (or as-equal-as-possible) team split
- Odd-player handling: send the extra player to Team A, Team B, or rotate each shuffle
- "By Team" and "All Players" views
- "Shuffle Again" for instant re-randomization
- Copy/share-ready team text, formatted for WhatsApp and similar apps

## Project structure

```
field-teams/
├── app.py                     # Streamlit UI
├── requirements.txt
├── README.md
├── src/
│   ├── team_generator.py      # shuffle_players, handle_odd_players, generate_teams
│   ├── player_manager.py      # add_player, add_players_bulk, remove_player, remove_duplicates
│   └── sharing.py             # format_teams, generate_share_text, generate_all_players_text
└── tests/
    └── test_team_generator.py
```

## Running the app

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Open the local URL Streamlit prints (usually `http://localhost:8501`).

## Running tests

```bash
pip install pytest
pytest tests/
```

## Roadmap (v2 ideas)

- Player positions (goalkeeper, defender, midfielder, forward) with position-balanced teams
- Player skill ratings and a "Balanced" shuffle mode
- Saved player lists across sessions
- Custom team names/colors
- Match history
- Native mobile share sheet (via a future mobile wrapper)
