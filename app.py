import os
import sys

# Forces Python to look in both the current directory and its parent folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Your imports (Line 8)
from .src.player_manager import add_player, add_players_bulk, remove_player

"""
⚽ Field Teams — Random Team Picker
Randomize. Divide. Play.

Run with:
    streamlit run app.py
"""

import streamlit as st

from src.player_manager import add_player, add_players_bulk, remove_player, clear_players
from src.team_generator import generate_teams, team_sizes_preview
from src.sharing import generate_share_text, generate_all_players_text


# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(page_title="Field Teams", page_icon="⚽", layout="centered")

# ----------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------
if "players" not in st.session_state:
    st.session_state.players = []

if "team_a" not in st.session_state:
    st.session_state.team_a = []

if "team_b" not in st.session_state:
    st.session_state.team_b = []

if "rotation_state" not in st.session_state:
    st.session_state.rotation_state = 0

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "By Team"

if "extra_player_rule" not in st.session_state:
    st.session_state.extra_player_rule = "rotate"

if "duplicate_warning" not in st.session_state:
    st.session_state.duplicate_warning = ""

if "skipped_bulk" not in st.session_state:
    st.session_state.skipped_bulk = []


def do_shuffle():
    if len(st.session_state.players) < 2:
        st.session_state.duplicate_warning = "Add at least 2 players before shuffling."
        return
    team_a, team_b, new_rotation = generate_teams(
        st.session_state.players,
        extra_to=st.session_state.extra_player_rule,
        rotation_state=st.session_state.rotation_state,
    )
    st.session_state.team_a = team_a
    st.session_state.team_b = team_b
    st.session_state.rotation_state = new_rotation


# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 0;'>⚽ FIELD TEAMS</h1>"
    "<p style='text-align: center; color: gray; margin-top: 0;'>Randomize. Divide. Play.</p>",
    unsafe_allow_html=True,
)
st.divider()

# ----------------------------------------------------------------------
# Player input section
# ----------------------------------------------------------------------
st.subheader("👤 Add Players")

input_tab, paste_tab = st.tabs(["One at a time", "Paste a list"])

with input_tab:
    with st.form(key="add_player_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            new_name = st.text_input("Player name", label_visibility="collapsed",
                                      placeholder="Enter player name")
        with col2:
            submitted = st.form_submit_button("+ Add", use_container_width=True)

        if submitted:
            updated, msg = add_player(st.session_state.players, new_name)
            st.session_state.players = updated
            st.session_state.duplicate_warning = msg

with paste_tab:
    with st.form(key="bulk_add_form", clear_on_submit=True):
        bulk_text = st.text_area(
            "Paste names, one per line",
            placeholder="Brian\nKevin\nJohn\nMike\nDavid\nSamuel",
            height=150,
        )
        bulk_submitted = st.form_submit_button("+ Add All", use_container_width=True)

        if bulk_submitted:
            updated, skipped = add_players_bulk(st.session_state.players, bulk_text)
            st.session_state.players = updated
            st.session_state.skipped_bulk = skipped
            st.session_state.duplicate_warning = ""

# Warnings / feedback
if st.session_state.duplicate_warning:
    st.warning(st.session_state.duplicate_warning)
    st.session_state.duplicate_warning = ""

if st.session_state.skipped_bulk:
    skipped_list = ", ".join(st.session_state.skipped_bulk)
    st.warning(f"⚠️ Skipped duplicate(s): {skipped_list}")
    st.session_state.skipped_bulk = []

# ----------------------------------------------------------------------
# Player list + count
# ----------------------------------------------------------------------
num_players = len(st.session_state.players)
st.markdown(f"**Players: {num_players}**  ·  {team_sizes_preview(num_players)}")

if st.session_state.players:
    for name in st.session_state.players:
        col_name, col_remove = st.columns([5, 1])
        with col_name:
            st.write(f"• {name}")
        with col_remove:
            if st.button("✕", key=f"remove_{name}", help=f"Remove {name}"):
                st.session_state.players = remove_player(st.session_state.players, name)
                st.rerun()

    if st.button("🗑️ Clear all players"):
        st.session_state.players = clear_players()
        st.session_state.team_a = []
        st.session_state.team_b = []
        st.rerun()
else:
    st.info("No players yet. Add some above to get started.")

st.divider()

# ----------------------------------------------------------------------
# Settings (kept minimal for v1, per the "don't overbuild" recommendation)
# ----------------------------------------------------------------------
with st.expander("⚙️ Game Settings"):
    st.session_state.extra_player_rule = st.radio(
        "Extra player (when the number of players is odd) goes to:",
        options=["rotate", "team_a", "team_b"],
        format_func=lambda x: {"rotate": "Rotate", "team_a": "Team A", "team_b": "Team B"}[x],
        index=["rotate", "team_a", "team_b"].index(st.session_state.extra_player_rule),
        horizontal=True,
    )

# ----------------------------------------------------------------------
# Shuffle button
# ----------------------------------------------------------------------
shuffle_label = "🔀 SHUFFLE TEAMS" if not st.session_state.team_a else "🔀 SHUFFLE AGAIN"
if st.button(shuffle_label, use_container_width=True, type="primary"):
    do_shuffle()

# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
if st.session_state.team_a or st.session_state.team_b:
    st.divider()
    st.subheader("⚽ Teams Ready!")

    if len(st.session_state.team_a) != len(st.session_state.team_b):
        larger = "Team A" if len(st.session_state.team_a) > len(st.session_state.team_b) else "Team B"
        st.caption(f"⚠️ {larger} has one extra player.")

    st.session_state.view_mode = st.radio(
        "View",
        options=["By Team", "All Players"],
        index=["By Team", "All Players"].index(st.session_state.view_mode),
        horizontal=True,
        label_visibility="collapsed",
    )

    if st.session_state.view_mode == "By Team":
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 🟦 Team A")
            for p in st.session_state.team_a:
                st.write(p)
        with col_b:
            st.markdown("### 🟥 Team B")
            for p in st.session_state.team_b:
                st.write(p)
    else:
        all_players_text = generate_all_players_text(st.session_state.team_a, st.session_state.team_b)
        for line in all_players_text.splitlines():
            st.write(line)

    st.divider()

    # Copy / Share
    share_text = generate_share_text(st.session_state.team_a, st.session_state.team_b)

    st.markdown("**📋 Copy / 📲 Share**")
    st.text_area("Shareable text", value=share_text, height=260, label_visibility="collapsed")
    st.caption("Tap inside the box above and copy (Ctrl/Cmd+A, then Ctrl/Cmd+C) to share on WhatsApp or anywhere else.")

st.divider()
st.caption("Field Teams v1 · Built with Python + Streamlit")
