"""
pages/2_Explore_Movies.py
--------------------------
Discover Movies — browse, search, filter, sort the full catalogue.
Preserves all original session-state pagination logic.
"""

import os
import sys

import streamlit as st
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.data_loader   import load_movies
from utils.preprocessing import clean_movies, get_genre_list, get_popular_movies
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    movie_card_html, empty_state, extract_year,
)
from utils.data_loader import load_ratings

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Discover Movies – CineMatch",
    page_icon  = "🔍",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)
inject_global_css()
sidebar_nav("discover")

# ── Session state ─────────────────────────────────────────────────────────────
if "watchlist"    not in st.session_state: st.session_state.watchlist    = []
if "explore_page" not in st.session_state: st.session_state.explore_page = 1

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading movie catalogue…"):
    try:
        movies_raw   = load_movies()
        movies_df    = clean_movies(movies_raw)
        genre_list   = get_genre_list(movies_df)
        ratings_df   = load_ratings()
        data_ok      = True
    except Exception as exc:
        st.error(f"⚠️ Failed to load data: {exc}")
        data_ok = False
        st.stop()

# Build average rating lookup from ratings dataset (real values, no invention)
try:
    rating_avg = (
        ratings_df.groupby("movieId")["rating"]
        .mean()
        .round(1)
        .to_dict()
    )
except Exception:
    rating_avg = {}

# Merge avg rating into movies_df for filtering
movies_df = movies_df.copy()
movies_df["avg_rating"] = movies_df["movieId"].map(rating_avg)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="cm-page">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="padding:40px 0 32px;">
      <div style="font-size:11px;color:#7c3aed;font-weight:700;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
        Browse · Search · Filter
      </div>
      <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
                 letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
        Discover Movies
      </h1>
      <p style="color:#8892a4;font-size:15px;max-width:560px;line-height:1.65;">
        Explore the full movie catalogue. Filter by genre, sort by title, and add
        favourites to your watchlist.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
# FILTER BAR
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:#12121a;border:1px solid #1e2a3a;border-radius:14px;'
    'padding:24px 24px 20px;margin-bottom:28px;">',
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns([3, 2, 1.5, 1.5])

with f1:
    search_q = st.text_input(
        "SEARCH TITLE",
        placeholder="e.g. Toy Story, Batman, Star Wars…",
        key="disc_search",
    )
with f2:
    sel_genres = st.multiselect(
        "FILTER BY GENRE",
        options=genre_list,
        placeholder="All genres",
        key="disc_genres",
    )
with f3:
    sort_by = st.selectbox(
        "SORT BY",
        options=["Title A–Z", "Title Z–A", "Rating ↓", "Genre"],
        key="disc_sort",
    )
with f4:
    min_rating = st.selectbox(
        "MIN RATING",
        options=["Any", "3.0+", "3.5+", "4.0+", "4.5+"],
        key="disc_minrating",
    )

st.markdown("</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ═════════════════════════════════════════════════════════════════════════════
filtered = movies_df.copy()

if search_q.strip():
    filtered = filtered[
        filtered["title"].str.contains(search_q.strip(), case=False, na=False)
    ]

if sel_genres:
    def _has_genre(gs: str) -> bool:
        movie_genres = {g.strip() for g in gs.split("|")}
        return any(g in movie_genres for g in sel_genres)
    filtered = filtered[filtered["genres"].apply(_has_genre)]

if min_rating != "Any":
    threshold = float(min_rating.replace("+", ""))
    filtered = filtered[filtered["avg_rating"].fillna(0) >= threshold]

if sort_by == "Title A–Z":
    filtered = filtered.sort_values("title", ascending=True)
elif sort_by == "Title Z–A":
    filtered = filtered.sort_values("title", ascending=False)
elif sort_by == "Rating ↓":
    filtered = filtered.sort_values("avg_rating", ascending=False)
elif sort_by == "Genre":
    filtered = filtered.sort_values(["genres", "title"])

filtered.reset_index(drop=True, inplace=True)

# ── Reset page on filter change ───────────────────────────────────────────────
filter_key = (search_q, tuple(sel_genres), sort_by, min_rating)
if st.session_state.get("_disc_filter_key") != filter_key:
    st.session_state.explore_page = 1
    st.session_state["_disc_filter_key"] = filter_key

# ═════════════════════════════════════════════════════════════════════════════
# RESULT COUNT BAR
# ═════════════════════════════════════════════════════════════════════════════
active_filters = []
if search_q.strip():     active_filters.append(f'title contains "<em>{search_q.strip()}</em>"')
if sel_genres:           active_filters.append(f'genre: <em>{", ".join(sel_genres)}</em>')
if min_rating != "Any":  active_filters.append(f'rating ≥ {min_rating}')

desc = " &amp; ".join(active_filters) if active_filters else "all movies"

st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:24px;flex-wrap:wrap;gap:10px;">
      <div style="font-size:14px;color:#8892a4;">
        Showing <strong style="color:#f1f1f1;">{len(filtered)}</strong>
        of <strong style="color:#f1f1f1;">{len(movies_df)}</strong> movies
        &nbsp;—&nbsp; {desc}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
# PAGINATION
# ═════════════════════════════════════════════════════════════════════════════
PAGE_SIZE   = 20
total_pages = max(1, (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE)
page        = min(st.session_state.explore_page, total_pages)
st.session_state.explore_page = page

start_idx = (page - 1) * PAGE_SIZE
end_idx   = min(start_idx + PAGE_SIZE, len(filtered))
page_data = filtered.iloc[start_idx:end_idx]

# ═════════════════════════════════════════════════════════════════════════════
# MOVIE GRID  (5 columns)
# ═════════════════════════════════════════════════════════════════════════════
COLS = 5

if len(page_data) == 0:
    empty_state(
        "🔍",
        "No Movies Found",
        "Try adjusting your search terms or removing some filters.",
    )
else:
    wl_titles = [m["title"] for m in st.session_state.watchlist]
    # track which movies user clicks "add to watchlist" on this render
    wl_adds    = []
    wl_removes = []

    for row_start in range(0, len(page_data), COLS):
        row_movies = page_data.iloc[row_start : row_start + COLS]
        gcols      = st.columns(COLS)

        for col, (df_idx, movie) in zip(gcols, row_movies.iterrows()):
            year   = extract_year(movie["title"])
            rating_val = movie.get("avg_rating")
            rating = f"{rating_val:.1f}" if pd.notna(rating_val) and rating_val > 0 else ""

            with col:
                st.markdown(
                    movie_card_html(
                        title  = movie["title"],
                        genres = movie["genres"],
                        year   = year,
                        rating = rating,
                    ),
                    unsafe_allow_html=True,
                )
                btn_key = f"disc_wl_{df_idx}"
                in_wl   = movie["title"] in wl_titles
                if in_wl:
                    if st.button("❤️", key=btn_key,
                                 help=f"Remove '{movie['title']}' from watchlist"):
                        wl_removes.append(movie["title"])
                else:
                    if st.button("🤍", key=btn_key,
                                 help=f"Add '{movie['title']}' to watchlist"):
                        wl_adds.append({
                            "title":  movie["title"],
                            "genres": movie["genres"],
                        })

        st.markdown("<br>", unsafe_allow_html=True)

    # Apply watchlist mutations after the render loop
    if wl_adds or wl_removes:
        for item in wl_adds:
            if item["title"] not in [m["title"] for m in st.session_state.watchlist]:
                st.session_state.watchlist.append(item)
        st.session_state.watchlist = [
            m for m in st.session_state.watchlist
            if m["title"] not in wl_removes
        ]
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# PAGINATION CONTROLS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
pc1, pc2, pc3 = st.columns([1, 2, 1])

with pc1:
    if st.button("◀  Previous", disabled=(page <= 1),
                 use_container_width=True, key="disc_prev"):
        st.session_state.explore_page = max(1, page - 1)
        st.rerun()

with pc2:
    st.markdown(
        f"""
        <div style="text-align:center;padding:10px 0;">
          <span style="color:#8892a4;font-size:13px;">Page </span>
          <span style="color:#e50914;font-weight:700;font-size:15px;">{page}</span>
          <span style="color:#8892a4;font-size:13px;"> of {total_pages}
          &nbsp;({start_idx+1}–{end_idx} of {len(filtered)})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with pc3:
    if st.button("Next  ▶", disabled=(page >= total_pages),
                 use_container_width=True, key="disc_next"):
        st.session_state.explore_page = min(total_pages, page + 1)
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="cm-footer">
      CineMatch &nbsp;·&nbsp; MovieLens Small Dataset &nbsp;·&nbsp;
      <a href="https://grouplens.org/datasets/movielens/" target="_blank">GroupLens Research</a>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
