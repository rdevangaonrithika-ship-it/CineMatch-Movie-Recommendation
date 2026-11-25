"""
pages/1_Recommend_Movies.py
----------------------------
CineMatch Recommendations Studio – Visual ML-powered discovery.
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
    page_title="Recommendations Studio – CineMatch",
    page_icon="🎯", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("recommend")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Load model ────────────────────────────────────────────────────────────────
with st.spinner("Initializing recommendation engine…"):
    try:
        recommender = get_recommender()
        model_ok    = True
    except Exception as exc:
        st.error(f"⚠️ Failed to load recommendation model: {exc}")
        model_ok = False
        st.stop()

all_titles = recommender.get_all_titles()

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 36px 0 24px;">
  <div style="font-size: 11px; color: #a78bfa; font-weight: 800;
              letter-spacing: 1.8px; text-transform: uppercase; margin-bottom: 10px;">
    Similarity Engine · Visual Discovery
  </div>
  <h1 style="font-size: 2.6rem; font-weight: 900; color: #ffffff;
             letter-spacing: -1.2px; line-height: 1.1; margin-bottom: 12px;">
    Find Movies You'll Love
  </h1>
  <p style="color: #94a3b8; font-size: 16px; max-width: 620px; line-height: 1.65;">
    Select any title from our indexed library. CineMatch analyzes its full thematic profile
    and instantly generates the closest matching films as high-impact poster cards.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Selector & Controls ───────────────────────────────────────────────────────
st.markdown("""
<div style="background:#111118; border:1px solid #1e2230; border-radius:16px;
            padding:26px 28px 22px; margin-bottom:28px;">
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([4, 1.2, 1.4])
with c1:
    selected_movie = st.selectbox(
        "CHOOSE OR SEARCH A MOVIE",
        [""] + all_titles,
        format_func=lambda x: "— Type or select a movie to explore —" if x == "" else x,
        key="rec_movie_select",
    )
with c2:
    n_recs = st.selectbox("RESULTS", [5, 10], index=1, key="rec_n")
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    find_btn = st.button(
        "🎯 Find Similar Movies",
        disabled=not selected_movie,
        use_container_width=True,
        key="rec_find_btn",
    )

st.markdown("</div>", unsafe_allow_html=True)

# ── Selected Movie Rich Inspector ─────────────────────────────────────────────
if selected_movie:
    info = recommender.get_movie_info(selected_movie)
    if info:
        year = extract_year(info["title"])

        with st.spinner("Fetching studio media…"):
            details = get_movie_details(info["title"], year, info["genres"])

        poster_url   = details["poster_url"]
        backdrop_url = details["backdrop_url"]
        overview     = details["overview"]
        runtime      = details["runtime_min"]
        vote         = details["vote_average"]
        tagline      = details["tagline"]

        genre_parts = [g.strip() for g in info["genres"].split("|") if g.strip()]
        genre_pills = "".join(
            f'<span class="detail-pill detail-pill-genre">{g}</span>'
            for g in genre_parts
        )
        year_pill    = f'<span class="detail-pill detail-pill-year">📅 {year}</span>' if year else ""
        rating_pill  = f'<span class="detail-pill detail-pill-rating">⭐ {vote}</span>' if vote > 0 else ""
        runtime_pill = f'<span class="detail-pill detail-pill-runtime">⏱ {runtime} min</span>' if runtime > 0 else ""

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
              {"<div class='detail-overview'>"+overview+"</div>" if overview else "<div class='detail-overview' style='color:#64748b;'>Ready for similarity recommendation matching. Click 'Find Similar Movies' to explore.</div>"}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        wl_col, _ = st.columns([1.5, 4.5])
        with wl_col:
            if in_wl:
                if st.button("❤️ Remove from Watchlist", key="sel_wl_rem", use_container_width=True):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != info["title"]
                    ]
                    st.rerun()
            else:
                if st.button("🤍 Add to Watchlist", key="sel_wl_add", use_container_width=True):
                    st.session_state.watchlist.append({
                        "title": info["title"], "genres": info["genres"],
                        "year": year, "poster_url": poster_url,
                    })
                    st.rerun()

# ── Recommendation Output ─────────────────────────────────────────────────────
# Auto-generate recommendations when a movie is picked or Find button clicked
should_recommend = find_btn or (selected_movie and "last_recommended" in st.session_state and st.session_state.last_recommended == selected_movie)

if find_btn and selected_movie:
    st.session_state.last_recommended = selected_movie

if (find_btn or should_recommend) and selected_movie:
    with st.spinner("Computing cosine similarity across feature space…"):
        t0      = time.time()
        result  = recommender.recommend_movies(selected_movie, n_recs)
        elapsed = round(time.time() - t0, 4)

    if not result["success"]:
        st.markdown(
            f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        recs = result["recommendations"]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between;
                    flex-wrap:wrap; gap:12px; margin-bottom:24px;">
          <div>
            <div style="font-size:22px; font-weight:800; color:#ffffff;">
              Top {len(recs)} Matches for "{result['query_title']}"
            </div>
            <div style="font-size:13px; color:#94a3b8; margin-top:4px;">
              Computed in {result['recommendation_time_sec']}s &nbsp;·&nbsp;
              Feature Profile: <strong style="color:#a78bfa;">{result['query_genres']}</strong>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

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
                        if st.button("❤️ Saved", key=f"wr_{rank}", help=f"Remove '{rec['title']}'", use_container_width=True):
                            wl_rems.append(rec["title"])
                    else:
                        if st.button("🤍 Watchlist", key=f"wa_{rank}", help=f"Add '{rec['title']}' to watchlist", use_container_width=True):
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

elif not selected_movie:
    empty_state(
        "🎬", "Choose a Movie to Get Started",
        "Select any title from the search bar above, then tap 'Find Similar Movies'.",
    )

st.markdown("""
<div class="cm-footer">
  CineMatch Studio · Stream &amp; Discover
</div>
</div>""", unsafe_allow_html=True)
