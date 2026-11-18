"""
pages/1_Recommend_Movies.py
----------------------------
Premium Recommendation Page — poster-first, ML-powered.
"""

import os, sys, time
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, empty_state, extract_year,
)
from utils.tmdb import get_poster_url, get_movie_details, has_api_key

st.set_page_config(
    page_title="Recommendations – CineMatch",
    page_icon="🎯", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("recommend")

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

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:40px 0 28px;">
  <div style="font-size:11px;color:#7c3aed;font-weight:700;
              letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
    Content-Based Filtering · TF-IDF · Cosine Similarity
  </div>
  <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
             letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
    Find Movies You'll Love
  </h1>
  <p style="color:#8892a4;font-size:15px;max-width:580px;line-height:1.65;">
    Select any movie and our ML engine instantly finds the most similar films
    based on genre analysis — displayed as beautiful poster cards.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#12121a;border:1px solid #1e2a3a;border-radius:14px;
            padding:28px 28px 24px;margin-bottom:28px;">
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([4, 1, 1])
with c1:
    selected_movie = st.selectbox(
        "SELECT A MOVIE",
        [""] + all_titles,
        format_func=lambda x: "— Search or choose a movie —" if x == "" else x,
        key="rec_movie_select",
    )
with c2:
    n_recs = st.selectbox("RESULTS", [5, 10], index=1, key="rec_n")
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    find_btn = st.button(
        "🎯 Find Similar",
        disabled=not selected_movie,
        use_container_width=True,
        key="rec_find_btn",
    )

st.markdown("</div>", unsafe_allow_html=True)

# ── Selected movie detail panel ───────────────────────────────────────────────
if selected_movie:
    info  = recommender.get_movie_info(selected_movie)
    if info:
        year  = extract_year(info["title"])

        # Fetch rich details + poster
        with st.spinner("Loading poster…"):
            details = get_movie_details(info["title"], year, info["genres"])

        poster_url   = details["poster_url"]
        backdrop_url = details["backdrop_url"]
        overview     = details["overview"]
        runtime      = details["runtime_min"]
        vote         = details["vote_average"]
        tagline      = details["tagline"]

        # Genre pills from original dataset genres (reliable)
        genre_parts = [g.strip() for g in info["genres"].split("|") if g.strip()]
        genre_pills = "".join(
            f'<span class="detail-pill detail-pill-genre">{g}</span>'
            for g in genre_parts
        )
        year_pill    = f'<span class="detail-pill detail-pill-year">📅 {year}</span>' if year else ""
        rating_pill  = f'<span class="detail-pill detail-pill-rating">⭐ {vote}</span>' if vote > 0 else ""
        runtime_pill = f'<span class="detail-pill detail-pill-runtime">⏱ {runtime} min</span>' if runtime > 0 else ""

        # Backdrop (top of panel)
        backdrop_html = (
            f'<img src="{backdrop_url}" class="detail-backdrop" alt="">'
            if backdrop_url and not backdrop_url.startswith("data:") else ""
        )

        wl_titles = [m["title"] for m in st.session_state.watchlist]
        in_wl     = info["title"] in wl_titles

        st.markdown(f"""
        <div class="detail-panel">
          {backdrop_html}
          <div class="detail-body">
            <div class="detail-poster-wrap">
              <img src="{poster_url}" alt="{info['title']}">
            </div>
            <div class="detail-info">
              <div class="detail-title">{info['title']}</div>
              {"<div class='detail-tagline'>"+tagline+"</div>" if tagline else ""}
              <div class="detail-meta-row">
                {year_pill}{rating_pill}{runtime_pill}{genre_pills}
              </div>
              {"<div class='detail-overview'>"+overview+"</div>" if overview else ""}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Watchlist toggle for selected movie
        wl_col, _ = st.columns([1, 5])
        with wl_col:
            if in_wl:
                if st.button("❤️ Remove from Watchlist", key="sel_wl_rem"):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != info["title"]
                    ]
                    st.rerun()
            else:
                if st.button("🤍 Add to Watchlist", key="sel_wl_add"):
                    st.session_state.watchlist.append({
                        "title": info["title"], "genres": info["genres"],
                        "year": year, "poster_url": poster_url,
                    })
                    st.rerun()

# ── Recommendation output ─────────────────────────────────────────────────────
if find_btn and selected_movie:
    with st.spinner("Calculating cosine similarity…"):
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

        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    flex-wrap:wrap;gap:12px;margin-bottom:24px;">
          <div>
            <div style="font-size:18px;font-weight:800;color:#f1f1f1;">
              Top {len(recs)} Movies Similar to "{result['query_title']}"
            </div>
            <div style="font-size:12px;color:#8892a4;margin-top:4px;">
              Computed in {result['recommendation_time_sec']}s &nbsp;·&nbsp;
              Genre match: <strong style="color:#a78bfa;">{result['query_genres']}</strong>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Fetch posters for all recs (cached after first call)
        COLS = 5
        wl_titles = [m["title"] for m in st.session_state.watchlist]
        wl_adds, wl_rems = [], []

        for row_start in range(0, len(recs), COLS):
            row_recs = recs[row_start: row_start + COLS]
            rcols    = st.columns(COLS)
            for col, rec in zip(rcols, row_recs):
                rank   = row_start + row_recs.index(rec) + 1
                year   = extract_year(rec["title"])
                poster = get_poster_url(rec["title"], year, rec["genres"])
                in_wl  = rec["title"] in wl_titles
                with col:
                    st.markdown(
                        poster_card_html(
                            title          = rec["title"],
                            poster_url     = poster,
                            genres         = rec["genres"],
                            year           = year,
                            similarity_pct = rec["similarity_pct"],
                            rank           = rank,
                        ),
                        unsafe_allow_html=True,
                    )
                    if in_wl:
                        if st.button("❤️", key=f"wr_{rank}",
                                     help=f"Remove '{rec['title']}'"):
                            wl_rems.append(rec["title"])
                    else:
                        if st.button("🤍", key=f"wa_{rank}",
                                     help=f"Add '{rec['title']}' to watchlist"):
                            wl_adds.append({
                                "title": rec["title"], "genres": rec["genres"],
                                "year": year, "poster_url": poster,
                            })
            st.markdown("<br>", unsafe_allow_html=True)

        if wl_adds or wl_rems:
            for item in wl_adds:
                if item["title"] not in [m["title"] for m in st.session_state.watchlist]:
                    st.session_state.watchlist.append(item)
            st.session_state.watchlist = [
                m for m in st.session_state.watchlist if m["title"] not in wl_rems
            ]
            st.rerun()

        # Disclaimer
        st.markdown("""
        <div style="background:#0d0d1a;border:1px solid #1e2a3a;border-radius:10px;
                    padding:14px 20px;display:flex;gap:12px;">
          <span style="flex-shrink:0;">ℹ️</span>
          <p style="font-size:12px;color:#4a5568;line-height:1.6;margin:0;">
            Recommendations use <strong style="color:#8892a4;">TF-IDF</strong> on genres
            and <strong style="color:#8892a4;">Cosine Similarity</strong>.
            A higher % means more genre overlap. Plots, cast and user history are not used.
          </p>
        </div>
        """, unsafe_allow_html=True)

elif not selected_movie:
    empty_state(
        "🎬", "Choose a Movie to Get Started",
        "Select any movie from the dropdown above, then click Find Similar.",
    )

st.markdown("""
<div class="cm-footer">CineMatch · Content-Based Filtering · TF-IDF + Cosine Similarity</div>
</div>""", unsafe_allow_html=True)
