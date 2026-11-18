"""
pages/2_Explore_Movies.py
--------------------------
Browse, search, and filter the entire movie catalogue.

Features
--------
- Search by movie title.
- Filter by one or more genres.
- Sort alphabetically or by genre.
- Paginated results.
"""

import os
import sys

import streamlit as st
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.data_loader import load_movies
from utils.preprocessing import clean_movies, get_genre_list

# ------------------------------------------------------------------ #
# Page config
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Explore Movies – CineMatch",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# CSS
# ------------------------------------------------------------------ #
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #141414; color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #333; }
    [data-testid="stSidebar"] * { color: #e5e5e5 !important; }
    #MainMenu, footer, header { visibility: hidden; }
    h1 { color: #E50914 !important; font-weight: 800; }
    h2, h3 { color: #FFFFFF !important; }
    .stButton > button {
        background-color: #E50914; color: #FFFFFF; border: none;
        border-radius: 4px; padding: 8px 20px; font-size: 14px; font-weight: 600;
    }
    .stButton > button:hover { background-color: #F40612; }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
    }
    .explore-card {
        background: #1f1f1f;
        border-radius: 8px;
        padding: 16px 14px;
        margin-bottom: 8px;
        border: 1px solid #2a2a2a;
        transition: border-color 0.2s, transform 0.15s;
    }
    .explore-card:hover { border-color: #E50914; transform: translateX(4px); }
    .explore-title { color: #FFFFFF; font-size: 14px; font-weight: 700; margin-bottom: 6px; }
    .explore-genres { color: #888; font-size: 12px; }
    .genre-tag {
        display: inline-block; background: #2a2a2a; color: #E50914;
        padding: 2px 8px; border-radius: 10px; font-size: 11px;
        margin-right: 4px; margin-bottom: 2px; border: 1px solid #3a3a3a;
    }
    .result-count {
        background: #1f1f1f; border-left: 4px solid #E50914;
        border-radius: 4px; padding: 10px 16px; margin: 12px 0;
        color: #e5e5e5; font-size: 14px;
    }
    .section-header {
        font-size: 20px; font-weight: 700; color: #FFFFFF;
        margin-bottom: 20px; padding-bottom: 8px;
        border-bottom: 2px solid #E50914; display: inline-block;
    }
    .sidebar-logo { font-size: 28px; font-weight: 900; color: #E50914 !important; letter-spacing: -1px; margin-bottom: 4px; }
    .sidebar-tagline { font-size: 11px; color: #888 !important; letter-spacing: 1px; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Sidebar
# ------------------------------------------------------------------ #
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎬 CineMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">MOVIE RECOMMENDATION SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                          label="🏠  Home")
    st.page_link("pages/1_Recommend_Movies.py",     label="🎯  Recommend Movies")
    st.page_link("pages/2_Explore_Movies.py",       label="🔍  Explore Movies")
    st.page_link("pages/3_About_Project.py",        label="📖  About Project")
    st.markdown("---")
    st.markdown(
        '<div style="font-size:11px; color:#666;">Content-Based Filtering<br>TF-IDF + Cosine Similarity</div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ #
# Page header
# ------------------------------------------------------------------ #
st.markdown("# 🔍 Explore Movies")
st.markdown(
    '<p style="color:#b3b3b3; font-size:15px; margin-top:-10px;">Browse the full movie catalogue. Search, filter by genre, and sort results.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ------------------------------------------------------------------ #
# Load data
# ------------------------------------------------------------------ #
with st.spinner("Loading dataset…"):
    try:
        movies_raw = load_movies()
        movies_df  = clean_movies(movies_raw)
        genre_list = get_genre_list(movies_df)
        data_ok    = True
    except Exception as exc:
        st.error(f"⚠️ Failed to load data: {exc}")
        data_ok = False
        st.stop()

# ------------------------------------------------------------------ #
# Filter controls
# ------------------------------------------------------------------ #
fc1, fc2, fc3 = st.columns([3, 2, 1])

with fc1:
    search_query = st.text_input(
        "🔎 Search by Title",
        placeholder="e.g. Toy Story, Batman, Star Wars…",
    )

with fc2:
    selected_genres = st.multiselect(
        "🏷️ Filter by Genre",
        options=genre_list,
        placeholder="All genres",
    )

with fc3:
    sort_by = st.selectbox(
        "↕️ Sort By",
        options=["Title (A–Z)", "Title (Z–A)", "Genre"],
    )

# ------------------------------------------------------------------ #
# Apply filters
# ------------------------------------------------------------------ #
filtered = movies_df.copy()

# Title search
if search_query.strip():
    mask = filtered["title"].str.contains(search_query.strip(), case=False, na=False)
    filtered = filtered[mask]

# Genre filter
if selected_genres:
    def has_all_genres(genre_str: str) -> bool:
        movie_genres = {g.strip() for g in genre_str.split("|")}
        return any(g in movie_genres for g in selected_genres)
    filtered = filtered[filtered["genres"].apply(has_all_genres)]

# Sort
if sort_by == "Title (A–Z)":
    filtered = filtered.sort_values("title", ascending=True)
elif sort_by == "Title (Z–A)":
    filtered = filtered.sort_values("title", ascending=False)
elif sort_by == "Genre":
    filtered = filtered.sort_values(["genres", "title"])

filtered.reset_index(drop=True, inplace=True)

# ------------------------------------------------------------------ #
# Result count
# ------------------------------------------------------------------ #
filter_desc = []
if search_query.strip():
    filter_desc.append(f'title contains "<em>{search_query.strip()}</em>"')
if selected_genres:
    filter_desc.append(f'genres include <em>{", ".join(selected_genres)}</em>')

desc_str = " and ".join(filter_desc) if filter_desc else "all genres"

st.markdown(
    f'<div class="result-count">'
    f'Showing <strong>{len(filtered)}</strong> of <strong>{len(movies_df)}</strong> movies'
    f' — {desc_str}'
    f'</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Pagination
# ------------------------------------------------------------------ #
PAGE_SIZE = 30
total_pages = max(1, (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE)

if "explore_page" not in st.session_state:
    st.session_state.explore_page = 1

# Reset to page 1 when filters change
if (
    st.session_state.get("_last_search") != search_query
    or st.session_state.get("_last_genres") != selected_genres
):
    st.session_state.explore_page = 1
    st.session_state["_last_search"] = search_query
    st.session_state["_last_genres"] = selected_genres

page = st.session_state.explore_page
start_idx = (page - 1) * PAGE_SIZE
end_idx   = min(start_idx + PAGE_SIZE, len(filtered))
page_data = filtered.iloc[start_idx:end_idx]

# ------------------------------------------------------------------ #
# Display cards in 3 columns
# ------------------------------------------------------------------ #
COLS = 3
if len(page_data) == 0:
    st.markdown(
        """
        <div style="background:#1f1f1f; border-radius:12px; padding:60px; text-align:center; border:2px dashed #333;">
            <div style="font-size:48px; margin-bottom:12px;">🎬</div>
            <div style="font-size:18px; color:#FFFFFF; font-weight:700;">No Movies Found</div>
            <div style="font-size:13px; color:#888; margin-top:8px;">Try adjusting your search or filters.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for i in range(0, len(page_data), COLS):
        row_movies = page_data.iloc[i : i + COLS]
        cols = st.columns(COLS)
        for col, (_, movie) in zip(cols, row_movies.iterrows()):
            genre_tags = " ".join(
                f'<span class="genre-tag">{g.strip()}</span>'
                for g in movie["genres"].split("|")
                if g.strip()
            )
            with col:
                st.markdown(
                    f"""
                    <div class="explore-card">
                        <div class="explore-title">{movie['title']}</div>
                        <div>{genre_tags}</div>
                        <div style="font-size:10px; color:#555; margin-top:8px;">
                            ID: {movie['movieId']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ------------------------------------------------------------------ #
# Pagination controls
# ------------------------------------------------------------------ #
st.markdown("<br>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns([1, 2, 1])

with p_col1:
    if st.button("◀ Previous", disabled=(page <= 1), use_container_width=True):
        st.session_state.explore_page = max(1, page - 1)
        st.rerun()

with p_col2:
    st.markdown(
        f'<div style="text-align:center; color:#888; font-size:14px; padding:10px 0;">'
        f'Page <strong style="color:#E50914;">{page}</strong> of {total_pages} '
        f'({start_idx + 1}–{end_idx} of {len(filtered)})</div>',
        unsafe_allow_html=True,
    )

with p_col3:
    if st.button("Next ▶", disabled=(page >= total_pages), use_container_width=True):
        st.session_state.explore_page = min(total_pages, page + 1)
        st.rerun()

# ------------------------------------------------------------------ #
# Footer
# ------------------------------------------------------------------ #
st.markdown(
    """
    <hr style="border-color:#2a2a2a; margin-top:40px;">
    <div style="text-align:center; color:#666; font-size:12px; padding:16px 0 32px;">
        CineMatch · MovieLens Small Dataset · GroupLens Research
    </div>
    """,
    unsafe_allow_html=True,
)
