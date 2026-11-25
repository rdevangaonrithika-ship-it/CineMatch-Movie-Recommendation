"""
pages/4_Watchlist.py
--------------------
My Watchlist — session-state saved movies & series with poster cards.
"""

import os, sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, empty_state, extract_year,
)
from utils.tmdb import get_poster_url

st.set_page_config(
    page_title="My Watchlist – CineMatch",
    page_icon="❤️", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("watchlist")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
watchlist = st.session_state.watchlist

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

count = len(watchlist)
bc    = "#e50914" if count > 0 else "#64748b"
st.markdown(f"""
<div style="padding:36px 0 24px;">
  <div style="font-size:11px; color:#a78bfa; font-weight:800;
              letter-spacing:1.8px; text-transform:uppercase; margin-bottom:10px;">
    Personal Collection
  </div>
  <div style="display:flex; align-items:baseline; gap:16px; flex-wrap:wrap;">
    <h1 style="font-size:2.6rem; font-weight:900; color:#ffffff;
               letter-spacing:-1.2px; line-height:1.1; margin-bottom:0;">
      My Watchlist
    </h1>
    <div style="background:rgba(229,9,20,0.12); border:1px solid rgba(229,9,20,0.3);
                border-radius:20px; padding:4px 16px;">
      <span style="color:{bc}; font-size:14px; font-weight:800;">
        {count} saved title{'s' if count!=1 else ''}
      </span>
    </div>
  </div>
  <p style="color:#94a3b8; font-size:16px; max-width:600px; line-height:1.65; margin-top:12px;">
    Your personal library of movies and series to watch next. Tap 🤍 on any poster across CineMatch to save more.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="cm-divider" style="margin-top:0;">', unsafe_allow_html=True)

# ── Empty State ───────────────────────────────────────────────────────────────
if count == 0:
    empty_state(
        "❤️", "Your Watchlist is Empty",
        "Browse titles on the Discover page or generate recommendations, then tap 🤍 on any card to save it here.",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns([1.2, 1.2, 2])
    with bc1:
        if st.button("✨ Discover Movies", use_container_width=True):
            st.switch_page("pages/2_Explore_Movies.py")
    with bc2:
        if st.button("🎯 Get Recommendations", use_container_width=True):
            st.switch_page("pages/1_Recommend_Movies.py")
else:
    # ── Action Bar ────────────────────────────────────────────────────────────
    _a1, _a2 = st.columns([4, 1.2])
    with _a2:
        if st.button("🗑️ Clear Entire List", use_container_width=True):
            st.session_state.watchlist = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("❤️ Saved Titles", f"{count} title{'s' if count!=1 else ''} ready to watch")

    COLS = 5
    to_remove = []
    for row_start in range(0, len(watchlist), COLS):
        batch = watchlist[row_start: row_start + COLS]
        gcols = st.columns(COLS)
        for col, (i, item) in zip(gcols, enumerate(batch, start=row_start)):
            year   = item.get("year","") or extract_year(item["title"])
            poster = item.get("poster_url") or get_poster_url(
                item["title"], year, item.get("genres","")
            )
            is_tv = item.get("genres") == "TV Series"
            with col:
                st.markdown(
                    poster_card_html(
                        title      = item["title"],
                        poster_url = poster,
                        genres     = item.get("genres",""),
                        year       = year,
                        is_tv      = is_tv,
                    ),
                    unsafe_allow_html=True,
                )
                if st.button("❤️ Remove", key=f"wl_del_{i}", use_container_width=True):
                    to_remove.append(item["title"])
        st.markdown("<br>", unsafe_allow_html=True)

    if to_remove:
        st.session_state.watchlist = [
            m for m in st.session_state.watchlist
            if m["title"] not in to_remove
        ]
        st.rerun()

    # ── ML Recommendations Based on Last Saved Movie ──────────────────────────
    st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)
    
    last_movie_title = watchlist[-1]["title"]
    section_header(
        "🤖 Because You Saved This",
        f"Similar titles based on '{last_movie_title}'",
    )

    with st.spinner("Finding matches to your latest saved title…"):
        try:
            recommender = get_recommender()
            ml_ok       = True
        except Exception:
            ml_ok = False

    if ml_ok and watchlist:
        result = recommender.recommend_movies(last_movie_title, 5)

        if result["success"]:
            st.markdown(
                f'<div style="background:#111118; border:1px solid #1e2230;'
                f'border-radius:12px; padding:12px 18px; margin-bottom:20px;'
                f'font-size:13px; color:#94a3b8;">Based on: '
                f'<strong style="color:#ffffff;">{result["query_title"]}</strong>'
                f' &nbsp;·&nbsp; Processed in {result["recommendation_time_sec"]}s</div>',
                unsafe_allow_html=True,
            )
            rcols     = st.columns(5)
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            adds      = []
            for i, (col, rec) in enumerate(zip(rcols, result["recommendations"])):
                year   = extract_year(rec["title"])
                poster = get_poster_url(rec["title"], year, rec["genres"])
                with col:
                    st.markdown(
                        poster_card_html(
                            title          = rec["title"],
                            poster_url     = poster,
                            genres         = rec["genres"],
                            year           = year,
                            similarity_pct = rec["similarity_pct"],
                            rank           = i + 1,
                        ),
                        unsafe_allow_html=True,
                    )
                    if rec["title"] in wl_titles:
                        st.markdown(
                            '<div style="text-align:center; font-size:11px;'
                            'color:#e50914; font-weight:700; padding:6px 0;">❤️ In Watchlist</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        if st.button("🤍 Add", key=f"wlra_{i}", use_container_width=True):
                            adds.append({
                                "title": rec["title"], "genres": rec["genres"],
                                "year": year, "poster_url": poster,
                            })
            if adds:
                for a in adds:
                    if a["title"] not in [m["title"] for m in st.session_state.watchlist]:
                        st.session_state.watchlist.append(a)
                st.rerun()

st.markdown("""
<div class="cm-footer">CineMatch · Stream &amp; Discover</div>
</div>""", unsafe_allow_html=True)
