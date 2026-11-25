"""
pages/2_Explore_Movies.py
--------------------------
Discover Movies — poster grid with search, genre, year & rating filters.
"""

import os, sys
import streamlit as st
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.data_loader   import load_movies, load_ratings
from utils.preprocessing import clean_movies, get_genre_list
from utils.styles import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, empty_state, extract_year,
)
from utils.tmdb import get_poster_url

st.set_page_config(
    page_title="Discover Movies – CineMatch",
    page_icon="🔍", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("discover")

if "watchlist"    not in st.session_state: st.session_state.watchlist    = []
if "explore_page" not in st.session_state: st.session_state.explore_page = 1

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading movie catalogue…"):
    try:
        movies_raw = load_movies()
        movies_df  = clean_movies(movies_raw)
        genre_list = get_genre_list(movies_df)
        ratings_df = load_ratings()
        data_ok    = True
    except Exception as exc:
        st.error(f"⚠️ {exc}")
        data_ok = False
        st.stop()

# Merge avg rating
try:
    avg_map = ratings_df.groupby("movieId")["rating"].mean().round(1).to_dict()
except Exception:
    avg_map = {}
movies_df = movies_df.copy()
movies_df["avg_rating"] = movies_df["movieId"].map(avg_map)

# Extract year column
movies_df["year"] = movies_df["title"].apply(extract_year)

st.markdown('<div class="cm-page">', unsafe_allow_html=True)
st.markdown("""
<div style="padding:36px 0 24px;">
  <div style="font-size:11px; color:#a78bfa; font-weight:800;
              letter-spacing:1.8px; text-transform:uppercase; margin-bottom:10px;">
    Catalogue Exploration · Real-Time Filters
  </div>
  <h1 style="font-size:2.6rem; font-weight:900; color:#ffffff;
             letter-spacing:-1.2px; line-height:1.1; margin-bottom:12px;">
    Discover Movies
  </h1>
  <p style="color:#94a3b8; font-size:16px; max-width:620px; line-height:1.65;">
    Explore our complete indexed film library. Filter by genre, release era, and critic ratings.
    Add titles directly to your watchlist or launch instant ML recommendations.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Filter Bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#111118; border:1px solid #1e2230; border-radius:16px;
            padding:24px 26px 20px; margin-bottom:28px;">
""", unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns([3, 2.2, 1.3, 1.4, 1.2])
with f1:
    search_q   = st.text_input("SEARCH BY TITLE",
                               placeholder="e.g. Toy Story, Batman, Pulp Fiction...",
                               key="disc_search")
with f2:
    sel_genres = st.multiselect("GENRES", genre_list,
                                placeholder="All Genres", key="disc_genres")
with f3:
    years_avail = sorted(
        {y for y in movies_df["year"] if y}, reverse=True
    )
    year_opts = ["Any Year"] + years_avail
    sel_year  = st.selectbox("RELEASE YEAR", year_opts, key="disc_year")
with f4:
    sort_by    = st.selectbox("SORT ORDER",
                              ["Title A–Z", "Title Z–A", "Rating ↓", "Genre"],
                              key="disc_sort")
with f5:
    min_rating = st.selectbox("MIN RATING",
                              ["Any Rating", "3.0+", "3.5+", "4.0+", "4.5+"],
                              key="disc_minrating")

st.markdown("</div>", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = movies_df.copy()

if search_q.strip():
    filtered = filtered[
        filtered["title"].str.contains(search_q.strip(), case=False, na=False)
    ]
if sel_genres:
    def _has(gs):
        return any(g in {x.strip() for x in gs.split("|")} for g in sel_genres)
    filtered = filtered[filtered["genres"].apply(_has)]
if sel_year != "Any Year":
    filtered = filtered[filtered["year"] == sel_year]
if min_rating != "Any Rating":
    thr = float(min_rating.replace("+",""))
    filtered = filtered[filtered["avg_rating"].fillna(0) >= thr]

if sort_by == "Title A–Z":
    filtered = filtered.sort_values("title")
elif sort_by == "Title Z–A":
    filtered = filtered.sort_values("title", ascending=False)
elif sort_by == "Rating ↓":
    filtered = filtered.sort_values("avg_rating", ascending=False)
elif sort_by == "Genre":
    filtered = filtered.sort_values(["genres","title"])

filtered.reset_index(drop=True, inplace=True)

# Reset page on filter change
fkey = (search_q, tuple(sel_genres), sel_year, sort_by, min_rating)
if st.session_state.get("_disc_fkey") != fkey:
    st.session_state.explore_page  = 1
    st.session_state["_disc_fkey"] = fkey

# ── Result Count Bar ──────────────────────────────────────────────────────────
parts = []
if search_q.strip():       parts.append(f'keyword "{search_q.strip()}"')
if sel_genres:             parts.append(f'genres: {", ".join(sel_genres)}')
if sel_year != "Any Year": parts.append(f'year: {sel_year}')
if min_rating != "Any Rating": parts.append(f'rating ≥ {min_rating}')
desc = " &amp; ".join(parts) if parts else "all indexed titles"

st.markdown(
    f'<div style="font-size:14px; color:#94a3b8; margin-bottom:22px; display:flex; justify-content:space-between; align-items:center;">'
    f'<div>Showing <strong style="color:#ffffff;">{len(filtered)}</strong>'
    f' of <strong style="color:#ffffff;">{len(movies_df)}</strong>'
    f' movies — {desc}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Pagination ────────────────────────────────────────────────────────────────
PAGE_SIZE   = 20
total_pages = max(1, (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE)
page        = min(st.session_state.explore_page, total_pages)
st.session_state.explore_page = page

start_idx = (page - 1) * PAGE_SIZE
end_idx   = min(start_idx + PAGE_SIZE, len(filtered))
page_data = filtered.iloc[start_idx:end_idx]

# ── Poster Grid ───────────────────────────────────────────────────────────────
COLS = 5
if len(page_data) == 0:
    empty_state("🔍", "No Movies Matched Your Filters", "Try clearing some filters or searching for another keyword.")
else:
    wl_titles = [m["title"] for m in st.session_state.watchlist]
    wl_adds, wl_rems = [], []

    for row_start in range(0, len(page_data), COLS):
        batch = page_data.iloc[row_start: row_start + COLS]
        gcols = st.columns(COLS)
        for col, (df_idx, movie) in zip(gcols, batch.iterrows()):
            year   = movie.get("year","")
            rating_val = movie.get("avg_rating")
            rating = f"{rating_val:.1f}" if pd.notna(rating_val) and rating_val > 0 else ""
            poster = get_poster_url(movie["title"], year, movie["genres"])
            in_wl  = movie["title"] in wl_titles
            with col:
                st.markdown(
                    poster_card_html(
                        title      = movie["title"],
                        poster_url = poster,
                        genres     = movie["genres"],
                        year       = year,
                        rating     = rating,
                    ),
                    unsafe_allow_html=True,
                )
                if in_wl:
                    if st.button("❤️ Saved", key=f"d_wl_{df_idx}",
                                 help=f"Remove '{movie['title']}'", use_container_width=True):
                        wl_rems.append(movie["title"])
                else:
                    if st.button("🤍 Watchlist", key=f"d_wl_{df_idx}",
                                 help=f"Add '{movie['title']}' to watchlist", use_container_width=True):
                        wl_adds.append({
                            "title": movie["title"], "genres": movie["genres"],
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

# ── Pagination Controls ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
pc1, pc2, pc3 = st.columns([1, 2, 1])
with pc1:
    if st.button("◀  Previous Page", disabled=(page <= 1),
                 use_container_width=True, key="disc_prev"):
        st.session_state.explore_page = max(1, page - 1)
        st.rerun()
with pc2:
    st.markdown(
        f'<div style="text-align:center; padding:10px 0; font-size:13px; color:#8892a4;">'
        f'Page <span style="color:#e50914; font-weight:800;">{page}</span>'
        f' of {total_pages} &nbsp;({start_idx+1}–{end_idx} of {len(filtered)} titles)</div>',
        unsafe_allow_html=True,
    )
with pc3:
    if st.button("Next Page  ▶", disabled=(page >= total_pages),
                 use_container_width=True, key="disc_next"):
        st.session_state.explore_page = min(total_pages, page + 1)
        st.rerun()

st.markdown("""
<div class="cm-footer">
  CineMatch Catalogue · Powered by MovieLens &amp; TMDB
</div></div>""", unsafe_allow_html=True)
