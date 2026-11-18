"""
pages/4_Watchlist.py
--------------------
My Watchlist — session-state saved movies with poster cards.
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
bc    = "#e50914" if count > 0 else "#4a5568"
st.markdown(f"""
<div style="padding:40px 0 28px;">
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
      <span style="color:{bc};font-size:14px;font-weight:700;">
        {count} movie{'s' if count!=1 else ''}
      </span>
    </div>
  </div>
  <p style="color:#8892a4;font-size:15px;max-width:560px;line-height:1.65;margin-top:12px;">
    Movies you've saved. Tap 🤍 on any poster card to add more.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="cm-divider" style="margin-top:0;">', unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
if count == 0:
    empty_state(
        "❤️", "Your Watchlist is Empty",
        "Browse movies on the Discover page or get recommendations, "
        "then tap 🤍 on any card to save it here.",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns([1,1,2])
    with bc1:
        if st.button("🔍 Discover Movies", use_container_width=True):
            st.switch_page("pages/2_Explore_Movies.py")
    with bc2:
        if st.button("🎯 Get Recommendations", use_container_width=True):
            st.switch_page("pages/1_Recommend_Movies.py")
else:
    # ── Action bar ────────────────────────────────────────────────────────────
    _a1, _a2, _a3 = st.columns([3,1,1])
    with _a3:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.watchlist = []; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("❤️ Saved Movies", f"{count} movie{'s' if count!=1 else ''} in your list")

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
            with col:
                st.markdown(
                    poster_card_html(
                        title      = item["title"],
                        poster_url = poster,
                        genres     = item.get("genres",""),
                        year       = year,
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

    # ── ML recs from last saved movie ─────────────────────────────────────────
    st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)
    section_header(
        "🤖 Because You Saved This",
        f"Movies similar to your last saved film — TF-IDF + Cosine Similarity",
    )

    with st.spinner("Building recommendations…"):
        try:
            recommender = get_recommender()
            ml_ok       = True
        except Exception:
            ml_ok = False

    if ml_ok and watchlist:
        seed   = watchlist[-1]["title"]
        result = recommender.recommend_movies(seed, 5)

        if result["success"]:
            st.markdown(
                f'<div style="background:#12121a;border:1px solid #1e2a3a;'
                f'border-radius:10px;padding:12px 16px;margin-bottom:20px;'
                f'font-size:13px;color:#8892a4;">Based on: '
                f'<strong style="color:#f1f1f1;">{result["query_title"]}</strong>'
                f' · {result["recommendation_time_sec"]}s</div>',
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
                            '<div style="text-align:center;font-size:11px;'
                            'color:#e50914;padding:4px 0;">❤️ Saved</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        if st.button("🤍 Save", key=f"wlra_{i}",
                                     use_container_width=True):
                            adds.append({
                                "title":rec["title"],"genres":rec["genres"],
                                "year":year,"poster_url":poster,
                            })
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

st.markdown("""
<div class="cm-footer">CineMatch · Watchlist powered by Streamlit Session State</div>
</div>""", unsafe_allow_html=True)
