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
    page_title="Web Series – CineMatch",
    page_icon="📺", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("webseries")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:40px 0 28px;">
  <div style="font-size:11px;color:#7c3aed;font-weight:700;
              letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
    TV · Streaming · Series
  </div>
  <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
             letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
    Web Series &amp; TV Shows
  </h1>
  <p style="color:#8892a4;font-size:15px;max-width:580px;line-height:1.65;">
    Browse trending and popular web series. Posters and data are sourced from TMDB.
    The recommendation engine covers movies — series browsing is powered by TMDB directly.
  </p>
</div>
""", unsafe_allow_html=True)

# ── API key notice ────────────────────────────────────────────────────────────
if not has_api_key():
    st.markdown("""
    <div class="api-banner">
      <span style="font-size:22px;">🔑</span>
      <div>
        <strong>TMDB API key required for web series posters.</strong>
        Create <code>.streamlit/secrets.toml</code> with
        <code>TMDB_API_KEY = "your_key"</code>.
        Get a free key at
        <a href="https://www.themoviedb.org/settings/api" target="_blank"
           style="color:#e50914;">themoviedb.org</a>.
        Genre-coloured placeholders are shown until a key is added.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TRENDING THIS WEEK
# ═════════════════════════════════════════════════════════════════════════════
section_header("🔥 Trending This Week", "Top TV shows everyone is watching right now")

with st.spinner("Loading trending series…"):
    trending = get_trending_tv(10)

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
            # Watchlist
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            if item["title"] in wl_titles:
                if st.button("❤️", key=f"tv_tr_rem_{i}",
                             help=f"Remove '{item['title']}'"):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != item["title"]
                    ]
                    st.rerun()
            else:
                if st.button("🤍", key=f"tv_tr_add_{i}",
                             help=f"Save '{item['title']}'"):
                    st.session_state.watchlist.append({
                        "title":      item["title"],
                        "genres":     "TV Series",
                        "year":       item["year"],
                        "poster_url": item["poster_url"],
                    })
                    st.rerun()
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)
else:
    # Placeholder cards when no API key
    empty_state(
        "📺", "No Series Data",
        "Add a TMDB API key to load real web series posters. "
        "Without a key, placeholder artwork is shown below.",
    )
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
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)

# ═════════════════════════════════════════════════════════════════════════════
# POPULAR SERIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🌟 Popular Series", "Consistently high-rated shows")

with st.spinner("Loading popular series…"):
    popular_tv = get_popular_tv(10)

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
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            if item["title"] in wl_titles:
                if st.button("❤️", key=f"tv_pop_rem_{i}",
                             help=f"Remove '{item['title']}'"):
                    st.session_state.watchlist = [
                        m for m in st.session_state.watchlist
                        if m["title"] != item["title"]
                    ]
                    st.rerun()
            else:
                if st.button("🤍", key=f"tv_pop_add_{i}",
                             help=f"Save '{item['title']}'"):
                    st.session_state.watchlist.append({
                        "title":      item["title"],
                        "genres":     "TV Series",
                        "year":       item["year"],
                        "poster_url": item["poster_url"],
                    })
                    st.rerun()
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)
else:
    # Placeholder cards for popular
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
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)

# ═════════════════════════════════════════════════════════════════════════════
# SERIES DETAIL LOOKUP
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)
section_header("🔎 Series Details", "Look up details for any TV show")

KNOWN_SERIES = [
    "Breaking Bad","Stranger Things","The Crown","Money Heist","Dark",
    "Squid Game","The Witcher","Wednesday","The Last of Us","Succession",
    "Game of Thrones","The Office","Friends","Sherlock","Black Mirror",
    "Ozark","Peaky Blinders","The Mandalorian","Narcos","House of Cards",
    "Chernobyl","Fleabag","Atlanta","Barry","The Boys","Euphoria",
    "Mindhunter","Westworld","Fargo","True Detective",
]

dc1, dc2 = st.columns([3,1])
with dc1:
    series_pick = st.selectbox(
        "SELECT A SERIES",
        [""] + sorted(KNOWN_SERIES),
        format_func=lambda x: "— Choose a series —" if x == "" else x,
        key="tv_detail_pick",
    )
with dc2:
    st.markdown("<br>", unsafe_allow_html=True)
    lookup_btn = st.button("🔎 Show Details",
                           disabled=not series_pick,
                           use_container_width=True,
                           key="tv_detail_btn")

if lookup_btn and series_pick:
    with st.spinner(f"Looking up '{series_pick}'…"):
        details = get_tv_details(series_pick)

    poster_url   = details["poster_url"]
    vote         = details["vote_average"]
    overview     = details["overview"]
    year         = details.get("first_air_date","")[:4]
    seasons      = details.get("seasons",0)
    episodes     = details.get("episodes",0)
    genres_str   = details.get("genres","")

    year_pill    = f'<span class="detail-pill detail-pill-year">📅 {year}</span>' if year else ""
    rating_pill  = f'<span class="detail-pill detail-pill-rating">⭐ {vote}</span>' if vote > 0 else ""
    seasons_pill = f'<span class="detail-pill detail-pill-runtime">📺 {seasons} seasons</span>' if seasons > 0 else ""
    ep_pill      = f'<span class="detail-pill detail-pill-runtime">🎬 {episodes} episodes</span>' if episodes > 0 else ""
    genre_pills  = "".join(
        f'<span class="detail-pill detail-pill-genre">{g.strip()}</span>'
        for g in genres_str.split("|") if g.strip()
    )

    dp1, dp2 = st.columns([1, 3])
    with dp1:
        st.markdown(
            f'<img src="{poster_url}" style="width:100%;border-radius:12px;'
            f'border:2px solid #1e2a3a;box-shadow:0 8px 32px rgba(0,0,0,.6);" '
            f'alt="{series_pick}">',
            unsafe_allow_html=True,
        )
    with dp2:
        st.markdown(
            f"""
            <div style="padding:8px 0;">
              <div class="tv-badge" style="position:static;display:inline-block;margin-bottom:12px;">SERIES</div>
              <div style="font-size:26px;font-weight:900;color:#f1f1f1;
                          margin-bottom:12px;letter-spacing:-0.5px;">
                {series_pick}
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
                {year_pill}{rating_pill}{seasons_pill}{ep_pill}{genre_pills}
              </div>
              <div style="font-size:14px;color:#94a3b8;line-height:1.75;max-width:600px;">
                {overview if overview else
                 "No description available. Add a TMDB API key for full details."}
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
  CineMatch · Web Series powered by
  <a href="https://www.themoviedb.org/" target="_blank">TMDB</a>
</div></div>""", unsafe_allow_html=True)
