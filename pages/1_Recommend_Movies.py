"""
pages/1_Recommend_Movies.py
----------------------------
Premium Recommendation Page.
All recommendations come 100% from the existing TF-IDF + Cosine Similarity model.
"""

import os
import sys
import time

import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    movie_card_html, empty_state, extract_year, toast,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Recommendations – CineMatch",
    page_icon  = "🎯",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)
inject_global_css()
sidebar_nav("recommend")

# ── Session state ─────────────────────────────────────────────────────────────
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Load model ────────────────────────────────────────────────────────────────
with st.spinner("Loading recommendation engine…"):
    try:
        recommender = get_recommender()
        model_ok    = True
    except Exception as exc:
        st.error(f"⚠️ Failed to load model: {exc}")
        model_ok = False
        st.stop()

all_titles = recommender.get_all_titles()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="cm-page">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="padding:40px 0 32px;">
      <div style="font-size:11px;color:#7c3aed;font-weight:700;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
        Content-Based Filtering · TF-IDF · Cosine Similarity
      </div>
      <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
                 letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
        Find Movies You'll Love
      </h1>
      <p style="color:#8892a4;font-size:15px;max-width:580px;line-height:1.65;">
        Select any movie below and our ML engine will instantly find the
        most similar films based on genre analysis.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
# CONTROLS PANEL
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="background:#12121a;border:1px solid #1e2a3a;border-radius:14px;
                padding:28px 28px 24px;margin-bottom:28px;">
    """,
    unsafe_allow_html=True,
)

ctrl1, ctrl2, ctrl3 = st.columns([4, 1, 1])

with ctrl1:
    selected_movie = st.selectbox(
        "SELECT A MOVIE",
        options=[""] + all_titles,
        format_func=lambda x: "— Search or choose a movie —" if x == "" else x,
        help="Start typing to search.",
        key="rec_movie_select",
    )

with ctrl2:
    n_recs = st.selectbox(
        "RESULTS",
        options=[5, 10],
        index=1,
        key="rec_n",
    )

with ctrl3:
    st.markdown("<br>", unsafe_allow_html=True)
    find_btn = st.button(
        "🎯 Find Similar",
        disabled=(not selected_movie),
        use_container_width=True,
        key="rec_find_btn",
    )

st.markdown("</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SELECTED MOVIE PANEL
# ═════════════════════════════════════════════════════════════════════════════
if selected_movie:
    info = recommender.get_movie_info(selected_movie)
    if info:
        year  = extract_year(info["title"])
        genre_parts = [g.strip() for g in info["genres"].split("|") if g.strip()]
        pills = "".join(
            f'<span style="background:rgba(124,58,237,0.15);color:#a78bfa;'
            f'border:1px solid rgba(124,58,237,0.3);padding:4px 12px;'
            f'border-radius:20px;font-size:12px;font-weight:600;margin-right:6px;">'
            f'{g}</span>'
            for g in genre_parts
        )
        year_html = (
            f'<span style="background:rgba(229,9,20,0.1);color:#e50914;'
            f'border:1px solid rgba(229,9,20,0.2);padding:4px 12px;'
            f'border-radius:20px;font-size:12px;font-weight:600;margin-right:6px;">'
            f'📅 {year}</span>'
            if year else ""
        )

        # Watchlist add
        wl_titles = [m["title"] for m in st.session_state.watchlist]
        in_wl     = info["title"] in wl_titles

        st.markdown(
            f"""
            <div class="selected-panel">
              <div class="selected-panel-eyebrow">▶ Now Selected</div>
              <div class="selected-panel-title">{info['title']}</div>
              <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;">
                {year_html}{pills}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Watchlist button for selected movie
        wl_col, _ = st.columns([1, 4])
        with wl_col:
            if in_wl:
                if st.button("❤️ Remove from Watchlist", key="sel_wl_remove"):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != info["title"]
                    ]
                    st.rerun()
            else:
                if st.button("🤍 Add to Watchlist", key="sel_wl_add"):
                    st.session_state.watchlist.append({
                        "title":  info["title"],
                        "genres": info["genres"],
                    })
                    st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS OUTPUT
# ═════════════════════════════════════════════════════════════════════════════
if find_btn and selected_movie:
    with st.spinner("Calculating cosine similarity across all movies…"):
        t0     = time.time()
        result = recommender.recommend_movies(selected_movie, n_recs)
        elapsed = round(time.time() - t0, 4)

    if not result["success"]:
        st.markdown(
            f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        recs = result["recommendations"]

        # ── Summary banner ──────────────────────────────────────────
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        flex-wrap:wrap;gap:12px;margin-bottom:24px;">
              <div>
                <div style="font-size:18px;font-weight:800;color:#f1f1f1;">
                  Top {len(recs)} Similar Movies
                </div>
                <div style="font-size:12px;color:#8892a4;margin-top:4px;">
                  Based on genre similarity to
                  <strong style="color:#f1f1f1;">{result['query_title']}</strong>
                  &nbsp;·&nbsp; Computed in {result['recommendation_time_sec']}s
                </div>
              </div>
              <div style="display:flex;align-items:center;gap:8px;
                          background:#12121a;border:1px solid #1e2a3a;
                          border-radius:8px;padding:8px 14px;">
                <span style="font-size:11px;color:#8892a4;">Query genres:</span>
                <span style="font-size:12px;color:#a78bfa;font-weight:600;">
                  {result['query_genres']}
                </span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Cards grid ──────────────────────────────────────────────
        COLS = 5
        for row_start in range(0, len(recs), COLS):
            row_recs = recs[row_start : row_start + COLS]
            rcols    = st.columns(COLS)
            for col, rec in zip(rcols, row_recs):
                rank = row_start + row_recs.index(rec) + 1
                year = extract_year(rec["title"])
                with col:
                    st.markdown(
                        movie_card_html(
                            title            = rec["title"],
                            genres           = rec["genres"],
                            year             = year,
                            similarity_pct   = rec["similarity_pct"],
                            similarity_score = rec["similarity_score"],
                            rank             = rank,
                        ),
                        unsafe_allow_html=True,
                    )
                    # Watchlist toggle per card
                    wl_titles = [m["title"] for m in st.session_state.watchlist]
                    if rec["title"] in wl_titles:
                        if st.button(
                            "❤️", key=f"wl_rem_{rank}",
                            help=f"Remove '{rec['title']}' from watchlist",
                        ):
                            st.session_state.watchlist = [
                                m for m in st.session_state.watchlist
                                if m["title"] != rec["title"]
                            ]
                            st.rerun()
                    else:
                        if st.button(
                            "🤍", key=f"wl_add_{rank}",
                            help=f"Add '{rec['title']}' to watchlist",
                        ):
                            st.session_state.watchlist.append({
                                "title":  rec["title"],
                                "genres": rec["genres"],
                            })
                            st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

        # ── Disclaimer ──────────────────────────────────────────────
        st.markdown(
            """
            <div style="background:#0d0d1a;border:1px solid #1e2a3a;border-radius:10px;
                        padding:14px 20px;margin-top:8px;display:flex;
                        align-items:flex-start;gap:12px;">
              <span style="font-size:16px;flex-shrink:0;">ℹ️</span>
              <p style="font-size:12px;color:#4a5568;line-height:1.6;margin:0;">
                Recommendations are computed using
                <strong style="color:#8892a4;">TF-IDF Vectorization</strong> on movie genres
                and <strong style="color:#8892a4;">Cosine Similarity</strong>.
                A higher match % means the two movies share more genre characteristics.
                This model does not analyse plots, cast, or personal user history.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif not selected_movie:
    empty_state(
        "🎬",
        "Choose a Movie to Get Started",
        "Select any movie from the dropdown above, then click Find Similar to discover "
        "recommendations powered by our ML model.",
    )

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="cm-footer">
      CineMatch &nbsp;·&nbsp; Content-Based Filtering &nbsp;·&nbsp;
      TF-IDF + Cosine Similarity
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
