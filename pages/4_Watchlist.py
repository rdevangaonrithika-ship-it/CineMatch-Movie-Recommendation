"""
pages/4_Watchlist.py
--------------------
My Watchlist — session-state based saved movies.
Users can add movies from the Recommendation and Discover pages,
then view, re-order and remove them here.
"""

import os
import sys

import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    movie_card_html, empty_state, extract_year,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "My Watchlist – CineMatch",
    page_icon  = "❤️",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)
inject_global_css()
sidebar_nav("watchlist")

# ── Session state ─────────────────────────────────────────────────────────────
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

watchlist = st.session_state.watchlist

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="cm-page">', unsafe_allow_html=True)

count = len(watchlist)
count_color = "#e50914" if count > 0 else "#4a5568"

st.markdown(
    f"""
    <div style="padding:40px 0 32px;">
      <div style="font-size:11px;color:#7c3aed;font-weight:700;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
        Your Saved Movies
      </div>
      <div style="display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;">
        <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
                   letter-spacing:-1px;line-height:1.1;margin-bottom:0;">
          My Watchlist
        </h1>
        <div style="background:rgba(229,9,20,0.12);border:1px solid rgba(229,9,20,0.25);
                    border-radius:20px;padding:4px 14px;">
          <span style="color:{count_color};font-size:14px;font-weight:700;">
            {count} movie{'s' if count != 1 else ''}
          </span>
        </div>
      </div>
      <p style="color:#8892a4;font-size:15px;max-width:560px;
                line-height:1.65;margin-top:12px;">
        Movies you've saved from recommendations and the discovery catalogue.
        Add more using the ❤️ / 🤍 buttons on any movie card.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="cm-divider" style="margin-top:0;">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# EMPTY STATE
# ═════════════════════════════════════════════════════════════════════════════
if count == 0:
    empty_state(
        "❤️",
        "Your Watchlist is Empty",
        "Browse movies on the Discover page or get recommendations, "
        "then tap the 🤍 button on any card to save it here.",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns([1, 1, 2])
    with bc1:
        if st.button("🔍 Discover Movies", use_container_width=True):
            st.switch_page("pages/2_Explore_Movies.py")
    with bc2:
        if st.button("🎯 Get Recommendations", use_container_width=True):
            st.switch_page("pages/1_Recommend_Movies.py")

else:
    # ── Action bar ──────────────────────────────────────────────────────────
    act1, act2, act3 = st.columns([2, 1, 1])
    with act3:
        if st.button("🗑️ Clear Watchlist", use_container_width=True):
            st.session_state.watchlist = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Watchlist cards (5-column grid) ─────────────────────────────────────
    section_header("❤️ Saved Movies", f"{count} movie{'s' if count != 1 else ''} in your list")

    COLS = 5
    to_remove = []

    for row_start in range(0, len(watchlist), COLS):
        row_items = watchlist[row_start : row_start + COLS]
        gcols     = st.columns(COLS)

        for col, (i, item) in zip(gcols, enumerate(row_items, start=row_start)):
            year = extract_year(item["title"])
            with col:
                st.markdown(
                    movie_card_html(
                        title  = item["title"],
                        genres = item["genres"],
                        year   = year,
                    ),
                    unsafe_allow_html=True,
                )
                if st.button("❤️ Remove", key=f"wl_del_{i}",
                             use_container_width=True):
                    to_remove.append(item["title"])

        st.markdown("<br>", unsafe_allow_html=True)

    if to_remove:
        st.session_state.watchlist = [
            m for m in st.session_state.watchlist
            if m["title"] not in to_remove
        ]
        st.rerun()

    # ── Divider ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

    # ── ML: Get recommendations based on watchlist ───────────────────────────
    section_header(
        "🤖 Recommendations Based on Your Watchlist",
        "Movies similar to what you've saved — powered by TF-IDF + Cosine Similarity",
    )

    with st.spinner("Building recommendations from your watchlist…"):
        try:
            recommender = get_recommender()
            ml_ok = True
        except Exception:
            ml_ok = False

    if ml_ok and watchlist:
        # Pick the most recently added movie as the seed
        seed_movie = watchlist[-1]["title"]
        result     = recommender.recommend_movies(seed_movie, 5)

        if result["success"]:
            st.markdown(
                f"""
                <div style="background:#12121a;border:1px solid #1e2a3a;border-radius:10px;
                            padding:12px 16px;margin-bottom:20px;font-size:13px;color:#8892a4;">
                  Showing movies similar to your last saved film:
                  <strong style="color:#f1f1f1;">{result['query_title']}</strong>
                  &nbsp;·&nbsp; Computed in {result['recommendation_time_sec']}s
                </div>
                """,
                unsafe_allow_html=True,
            )
            rcols = st.columns(5)
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            adds = []
            for i, (col, rec) in enumerate(zip(rcols, result["recommendations"])):
                year = extract_year(rec["title"])
                with col:
                    st.markdown(
                        movie_card_html(
                            title            = rec["title"],
                            genres           = rec["genres"],
                            year             = year,
                            similarity_pct   = rec["similarity_pct"],
                            similarity_score = rec["similarity_score"],
                            rank             = i + 1,
                        ),
                        unsafe_allow_html=True,
                    )
                    if rec["title"] not in wl_titles:
                        if st.button("🤍 Save", key=f"wl_rec_add_{i}",
                                     use_container_width=True):
                            adds.append({"title": rec["title"], "genres": rec["genres"]})
                    else:
                        st.markdown(
                            '<div style="text-align:center;font-size:11px;'
                            'color:#e50914;padding:4px 0;">❤️ Saved</div>',
                            unsafe_allow_html=True,
                        )
            if adds:
                for a in adds:
                    if a["title"] not in [m["title"] for m in st.session_state.watchlist]:
                        st.session_state.watchlist.append(a)
                st.rerun()
        else:
            st.markdown(
                f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="cm-footer">
      CineMatch &nbsp;·&nbsp; Watchlist powered by Streamlit Session State
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
