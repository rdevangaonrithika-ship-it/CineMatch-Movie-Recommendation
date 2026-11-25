"""
pages/5_Web_Series.py
----------------------
Web Series — browse trending and popular TV shows via TMDB.
Completely separate from the movie recommendation model.
"""

import os, sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, empty_state, extract_year,
)
from utils.tmdb import (
    get_trending_tv, get_popular_tv, get_tv_details,
    has_api_key, placeholder_img_url,
)

st.set_page_config(
    page_title="Web Series & Shows – CineMatch",
    page_icon="📺", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("webseries")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:36px 0 24px;">
  <div style="font-size:11px; color:#a78bfa; font-weight:800;
              letter-spacing:1.8px; text-transform:uppercase; margin-bottom:10px;">
    Television &amp; Streaming Originals
  </div>
  <h1 style="font-size:2.6rem; font-weight:900; color:#ffffff;
             letter-spacing:-1.2px; line-height:1.1; margin-bottom:12px;">
    Web Series &amp; TV Shows
  </h1>
  <p style="color:#94a3b8; font-size:16px; max-width:620px; line-height:1.65;">
    Browse trending releases and critically acclaimed web series.
    Inspect season counts, episodes, and plot overviews, and save your favourite shows directly to your watchlist.
  </p>
</div>
""", unsafe_allow_html=True)

# ── API Key Notice Banner ─────────────────────────────────────────────────────
if not has_api_key():
    st.markdown("""
    <div class="api-banner">
      <span style="font-size:22px;">🔑</span>
      <div>
        <strong>TMDB API key optional for live streaming posters.</strong>
        Add <code>TMDB_API_KEY = "your_key"</code> in <code>.streamlit/secrets.toml</code> to load real-time TV network posters and metadata.
        Curated series artworks are displayed below in offline mode.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Section Tabs ──────────────────────────────────────────────────────────────
tab_trending, tab_popular, tab_inspector = st.tabs([
    "🔥 Trending This Week",
    "🌟 All-Time Popular Hits",
    "🔎 Series Detail Inspector",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: TRENDING THIS WEEK
# ═════════════════════════════════════════════════════════════════════════════
with tab_trending:
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🔥 Trending Shows", "The most-watched web series across streaming platforms right now")

    with st.spinner("Fetching trending series…"):
        trending = get_trending_tv(10)

    wl_titles = [m["title"] for m in st.session_state.watchlist]
    wl_adds = []
    wl_rems = []

    if trending:
        cols = st.columns(5)
        for i, item in enumerate(trending[:10]):
            with cols[i % 5]:
                st.markdown(
                    poster_card_html(
                        title      = item["title"],
                        poster_url = item["poster_url"],
                        year       = item["year"],
                        rating     = str(item["vote_average"]) if item["vote_average"] > 0 else "",
                        is_tv      = True,
                    ),
                    unsafe_allow_html=True,
                )
                if item["title"] in wl_titles:
                    if st.button("❤️ Saved", key=f"tv_tr_rem_{i}", use_container_width=True):
                        wl_rems.append(item["title"])
                else:
                    if st.button("🤍 Watchlist", key=f"tv_tr_add_{i}", use_container_width=True):
                        wl_adds.append({
                            "title":      item["title"],
                            "genres":     "TV Series",
                            "year":       item["year"],
                            "poster_url": item["poster_url"],
                        })
            if i == 4:
                st.markdown("<br>", unsafe_allow_html=True)
                cols = st.columns(5)
    else:
        # High quality offline fallback list
        SAMPLE_SERIES = [
            ("Breaking Bad",         "2008", "Crime | Drama | Thriller"),
            ("Stranger Things",      "2016", "Drama | Fantasy | Horror"),
            ("The Crown",            "2016", "Drama | History"),
            ("Money Heist",          "2017", "Action | Crime | Drama"),
            ("Dark",                 "2017", "Drama | Mystery | Sci-Fi"),
            ("Squid Game",           "2021", "Action | Drama | Mystery"),
            ("The Witcher",          "2019", "Action | Adventure | Fantasy"),
            ("Wednesday",            "2022", "Comedy | Fantasy | Horror"),
            ("The Last of Us",       "2023", "Action | Adventure | Drama"),
            ("Succession",           "2018", "Drama"),
        ]
        cols = st.columns(5)
        for i, (title, year, genres) in enumerate(SAMPLE_SERIES):
            poster = placeholder_img_url(genres, title)
            with cols[i % 5]:
                st.markdown(
                    poster_card_html(
                        title      = title,
                        poster_url = poster,
                        genres     = genres,
                        year       = year,
                        is_tv      = True,
                    ),
                    unsafe_allow_html=True,
                )
                if title in wl_titles:
                    if st.button("❤️ Saved", key=f"s_tv_rem_{i}", use_container_width=True):
                        wl_rems.append(title)
                else:
                    if st.button("🤍 Watchlist", key=f"s_tv_add_{i}", use_container_width=True):
                        wl_adds.append({
                            "title":      title,
                            "genres":     "TV Series",
                            "year":       year,
                            "poster_url": poster,
                        })
            if i == 4:
                st.markdown("<br>", unsafe_allow_html=True)
                cols = st.columns(5)

    if wl_adds or wl_rems:
        for item in wl_adds:
            if item["title"] not in [m["title"] for m in st.session_state.watchlist]:
                st.session_state.watchlist.append(item)
        st.session_state.watchlist = [
            m for m in st.session_state.watchlist if m["title"] not in wl_rems
        ]
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: POPULAR ALL-TIME HITS
# ═════════════════════════════════════════════════════════════════════════════
with tab_popular:
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🌟 Popular Hits", "Top rated series with dedicated global fanbases")

    with st.spinner("Fetching popular series…"):
        popular_tv = get_popular_tv(10)

    wl_titles = [m["title"] for m in st.session_state.watchlist]
    wl_adds = []
    wl_rems = []

    if popular_tv:
        cols = st.columns(5)
        for i, item in enumerate(popular_tv[:10]):
            with cols[i % 5]:
                st.markdown(
                    poster_card_html(
                        title      = item["title"],
                        poster_url = item["poster_url"],
                        year       = item["year"],
                        rating     = str(item["vote_average"]) if item["vote_average"] > 0 else "",
                        is_tv      = True,
                    ),
                    unsafe_allow_html=True,
                )
                if item["title"] in wl_titles:
                    if st.button("❤️ Saved", key=f"tv_pop_rem_{i}", use_container_width=True):
                        wl_rems.append(item["title"])
                else:
                    if st.button("🤍 Watchlist", key=f"tv_pop_add_{i}", use_container_width=True):
                        wl_adds.append({
                            "title":      item["title"],
                            "genres":     "TV Series",
                            "year":       item["year"],
                            "poster_url": item["poster_url"],
                        })
            if i == 4:
                st.markdown("<br>", unsafe_allow_html=True)
                cols = st.columns(5)
    else:
        SAMPLE_POPULAR = [
            ("Game of Thrones",   "2011", "Action | Adventure | Drama"),
            ("The Office",        "2005", "Comedy"),
            ("Friends",           "1994", "Comedy | Romance"),
            ("Sherlock",          "2010", "Crime | Drama | Mystery"),
            ("Black Mirror",      "2011", "Drama | Sci-Fi | Thriller"),
            ("Ozark",             "2017", "Crime | Drama | Thriller"),
            ("Peaky Blinders",    "2013", "Crime | Drama"),
            ("The Mandalorian",   "2019", "Action | Adventure | Sci-Fi"),
            ("Narcos",            "2015", "Biography | Crime | Drama"),
            ("House of Cards",    "2013", "Drama"),
        ]
        cols = st.columns(5)
        for i, (title, year, genres) in enumerate(SAMPLE_POPULAR):
            poster = placeholder_img_url(genres, title)
            with cols[i % 5]:
                st.markdown(
                    poster_card_html(
                        title=title, poster_url=poster,
                        genres=genres, year=year, is_tv=True,
                    ),
                    unsafe_allow_html=True,
                )
                if title in wl_titles:
                    if st.button("❤️ Saved", key=f"s_pop_rem_{i}", use_container_width=True):
                        wl_rems.append(title)
                else:
                    if st.button("🤍 Watchlist", key=f"s_pop_add_{i}", use_container_width=True):
                        wl_adds.append({
                            "title":      title,
                            "genres":     "TV Series",
                            "year":       year,
                            "poster_url": poster,
                        })
            if i == 4:
                st.markdown("<br>", unsafe_allow_html=True)
                cols = st.columns(5)

    if wl_adds or wl_rems:
        for item in wl_adds:
            if item["title"] not in [m["title"] for m in st.session_state.watchlist]:
                st.session_state.watchlist.append(item)
        st.session_state.watchlist = [
            m for m in st.session_state.watchlist if m["title"] not in wl_rems
        ]
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: SERIES DETAIL INSPECTOR
# ═════════════════════════════════════════════════════════════════════════════
with tab_inspector:
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("🔎 Series Details", "Inspect complete metadata, seasons, and plot overviews")

    KNOWN_SERIES = [
        "Breaking Bad", "Stranger Things", "The Crown", "Money Heist", "Dark",
        "Squid Game", "The Witcher", "Wednesday", "The Last of Us", "Succession",
        "Game of Thrones", "The Office", "Friends", "Sherlock", "Black Mirror",
        "Ozark", "Peaky Blinders", "The Mandalorian", "Narcos", "House of Cards",
        "Chernobyl", "Fleabag", "Atlanta", "Barry", "The Boys", "Euphoria",
        "Mindhunter", "Westworld", "Fargo", "True Detective",
    ]

    dc1, dc2 = st.columns([3, 1])
    with dc1:
        series_pick = st.selectbox(
            "SELECT A SERIES TO INSPECT",
            [""] + sorted(KNOWN_SERIES),
            format_func=lambda x: "— Choose a web series to view details —" if x == "" else x,
            key="tv_detail_pick",
        )
    with dc2:
        st.markdown("<br>", unsafe_allow_html=True)
        lookup_btn = st.button("🔎 Show Details", disabled=not series_pick, use_container_width=True, key="tv_detail_btn")

    if (lookup_btn or series_pick) and series_pick:
        with st.spinner(f"Looking up '{series_pick}'…"):
            details = get_tv_details(series_pick)

        poster_url   = details["poster_url"]
        vote         = details["vote_average"]
        overview     = details["overview"]
        year         = details.get("first_air_date", "")[:4]
        seasons      = details.get("seasons", 0)
        episodes     = details.get("episodes", 0)
        genres_str   = details.get("genres", "")

        year_pill    = f'<span class="detail-pill detail-pill-year">📅 {year}</span>' if year else ""
        rating_pill  = f'<span class="detail-pill detail-pill-rating">⭐ {vote}</span>' if vote > 0 else ""
        seasons_pill = f'<span class="detail-pill detail-pill-runtime">📺 {seasons} seasons</span>' if seasons > 0 else ""
        ep_pill      = f'<span class="detail-pill detail-pill-runtime">🎬 {episodes} episodes</span>' if episodes > 0 else ""
        genre_pills  = "".join(
            f'<span class="detail-pill detail-pill-genre">{g.strip()}</span>'
            for g in genres_str.split("|") if g.strip()
        )

        st.markdown("<br>", unsafe_allow_html=True)
        dp1, dp2 = st.columns([1, 3])
        with dp1:
            st.markdown(
                f'<img src="{poster_url}" style="width:100%; border-radius:14px;'
                f'border:2px solid #1e2230; box-shadow:0 12px 36px rgba(0,0,0,.7);" '
                f'alt="{series_pick}">',
                unsafe_allow_html=True,
            )
        with dp2:
            st.markdown(
                f"""
                <div style="padding:4px 0;">
                  <div class="tv-badge" style="position:static; display:inline-block; margin-bottom:12px;">SERIES</div>
                  <div style="font-size:28px; font-weight:900; color:#ffffff;
                              margin-bottom:12px; letter-spacing:-0.5px;">
                    {series_pick}
                  </div>
                  <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:18px;">
                    {year_pill}{rating_pill}{seasons_pill}{ep_pill}{genre_pills}
                  </div>
                  <div style="font-size:14px; color:#94a3b8; line-height:1.75; max-width:680px; margin-bottom:20px;">
                    {overview if overview else
                     "Critically acclaimed streaming series available on major international platforms."}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            if series_pick in wl_titles:
                if st.button("❤️ Remove from Watchlist", key="tv_det_rem"):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != series_pick
                    ]
                    st.rerun()
            else:
                if st.button("🤍 Add to Watchlist", key="tv_det_add"):
                    st.session_state.watchlist.append({
                        "title": series_pick, "genres": genres_str or "TV Series",
                        "year": year, "poster_url": poster_url,
                    })
                    st.rerun()

st.markdown("""
<div class="cm-footer">
  CineMatch Web Series · Powered by TMDB API
</div></div>""", unsafe_allow_html=True)
