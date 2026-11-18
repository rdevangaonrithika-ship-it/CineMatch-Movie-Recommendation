"""
pages/1_Recommend_Movies.py
----------------------------
The main recommendation page.

Users can:
  - Search and select a movie from the dataset.
  - Choose how many recommendations to display (5 or 10).
  - View recommended movies with genre and similarity percentage.
"""

import os
import sys
import time

import streamlit as st

# ------------------------------------------------------------------ #
# Make project root importable
# ------------------------------------------------------------------ #
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.data_loader import load_movies

# ------------------------------------------------------------------ #
# Page config
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Recommend Movies – CineMatch",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# Shared CSS (same theme as app.py)
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
    h2 { color: #FFFFFF !important; font-weight: 700; }
    h3 { color: #E50914 !important; }
    .stButton > button {
        background-color: #E50914; color: #FFFFFF; border: none;
        border-radius: 4px; padding: 10px 28px; font-size: 15px;
        font-weight: 600; transition: background-color 0.2s;
    }
    .stButton > button:hover { background-color: #F40612; transform: scale(1.03); }
    .stSelectbox > div > div {
        background-color: #2a2a2a !important; color: #FFFFFF !important;
        border: 1px solid #444 !important; border-radius: 4px;
    }
    .movie-card {
        background: linear-gradient(145deg, #1f1f1f, #2a2a2a);
        border-radius: 10px; padding: 18px 16px; margin-bottom: 10px;
        border-left: 4px solid #E50914;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .movie-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(229,9,20,0.25); }
    .movie-title { color: #FFFFFF; font-size: 15px; font-weight: 700; margin-bottom: 6px; }
    .movie-genre { color: #b3b3b3; font-size: 12px; margin-bottom: 8px; }
    .similarity-badge {
        display: inline-block; background-color: #E50914; color: white;
        padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 700;
    }
    .rank-badge {
        display: inline-block; background-color: #333; color: #E50914;
        padding: 2px 8px; border-radius: 4px; font-size: 11px;
        font-weight: 700; margin-right: 8px;
    }
    .selected-movie-box {
        background: linear-gradient(135deg, #1a0000, #1f1f1f);
        border: 1px solid #E50914; border-radius: 12px; padding: 24px 28px;
        margin-bottom: 28px;
    }
    .sim-bar-container {
        background: #333; border-radius: 8px; height: 8px;
        margin-top: 8px; overflow: hidden;
    }
    .sim-bar-fill {
        background: linear-gradient(90deg, #E50914, #FF6B6B);
        height: 8px; border-radius: 8px;
    }
    .info-box {
        background: #1f1f1f; border-left: 4px solid #E50914;
        border-radius: 4px; padding: 14px 18px; margin: 16px 0;
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
st.markdown("# 🎯 Movie Recommendations")
st.markdown(
    '<p style="color:#b3b3b3; font-size:15px; margin-top:-10px;">Select a movie to discover similar titles based on genre analysis.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ------------------------------------------------------------------ #
# Load model
# ------------------------------------------------------------------ #
with st.spinner("Loading recommendation model…"):
    try:
        recommender = get_recommender()
        model_ready = True
    except Exception as exc:
        st.error(f"⚠️ Failed to load model: {exc}")
        model_ready = False
        st.stop()

# ------------------------------------------------------------------ #
# Controls
# ------------------------------------------------------------------ #
all_titles = recommender.get_all_titles()

col_select, col_count = st.columns([3, 1])

with col_select:
    selected_movie = st.selectbox(
        "🎬 Select a Movie",
        options=[""] + all_titles,
        format_func=lambda x: "— Choose a movie —" if x == "" else x,
        help="Start typing to search for a movie.",
    )

with col_count:
    n_recommendations = st.selectbox(
        "📋 Recommendations",
        options=[5, 10],
        index=1,
        help="Choose how many recommendations to display.",
    )

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Display selected movie info
# ------------------------------------------------------------------ #
if selected_movie:
    movie_info = recommender.get_movie_info(selected_movie)

    if movie_info:
        genres_list = movie_info["genres"].split("|")
        genre_tags  = " ".join(
            f'<span style="background:#2a2a2a; color:#E50914; padding:3px 10px; '
            f'border-radius:12px; font-size:12px; margin-right:4px; border:1px solid #E50914;">{g.strip()}</span>'
            for g in genres_list if g.strip()
        )
        st.markdown(
            f"""
            <div class="selected-movie-box">
                <div style="font-size:11px; color:#888; letter-spacing:1px; margin-bottom:6px;">SELECTED MOVIE</div>
                <div style="font-size:22px; font-weight:800; color:#FFFFFF; margin-bottom:10px;">{movie_info['title']}</div>
                <div style="margin-bottom:10px;">{genre_tags}</div>
                <div style="font-size:12px; color:#666;">Movie ID: {movie_info['movieId']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------ #
# Recommend button
# ------------------------------------------------------------------ #
col_btn, col_clear = st.columns([2, 1])

with col_btn:
    get_recs = st.button(
        f"🚀 Get {n_recommendations} Recommendations",
        disabled=(not selected_movie),
        use_container_width=True,
    )

with col_clear:
    if st.button("🔄 Select Another Movie", use_container_width=True):
        st.rerun()

# ------------------------------------------------------------------ #
# Generate and display recommendations
# ------------------------------------------------------------------ #
if get_recs and selected_movie:
    with st.spinner(f"Finding the {n_recommendations} most similar movies…"):
        start_time = time.time()
        result = recommender.recommend_movies(selected_movie, n_recommendations)
        elapsed = round(time.time() - start_time, 4)

    if not result["success"]:
        st.error(f"⚠️ {result['error_message']}")
    else:
        recs = result["recommendations"]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-header">🎬 Top {len(recs)} Movies Similar to "{result["query_title"]}"</div>',
            unsafe_allow_html=True,
        )

        # Performance info
        st.markdown(
            f'<div class="info-box">'
            f'Found <strong>{len(recs)}</strong> recommendations in '
            f'<strong>{result["recommendation_time_sec"]}s</strong> &nbsp;·&nbsp; '
            f'Based on genre similarity to: <strong>{result["query_genres"]}</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Movie cards in 2 columns
        COLS = 2
        for i in range(0, len(recs), COLS):
            row_recs = recs[i : i + COLS]
            cols     = st.columns(COLS)
            for col, (j, rec) in zip(cols, enumerate(row_recs, start=i + 1)):
                genre_tags = " ".join(
                    f'<span style="background:#333; color:#aaa; padding:2px 8px; '
                    f'border-radius:10px; font-size:11px; margin-right:3px;">{g.strip()}</span>'
                    for g in rec["genres"].split("|")
                    if g.strip()
                )
                sim_pct    = rec["similarity_score"] * 100
                bar_width  = max(4, int(sim_pct))

                with col:
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <span class="rank-badge">#{j}</span>
                            <span class="similarity-badge">{rec['similarity_pct']} Match</span>
                            <div class="movie-title" style="margin-top:10px;">{rec['title']}</div>
                            <div class="movie-genre">{genre_tags}</div>
                            <div class="sim-bar-container">
                                <div class="sim-bar-fill" style="width:{bar_width}%;"></div>
                            </div>
                            <div style="font-size:11px; color:#666; margin-top:4px;">
                                Genre similarity score: {rec['similarity_score']:.4f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Explanation notice
        st.markdown(
            """
            <div style="background:#1a1a1a; border-radius:8px; padding:16px 20px; margin-top:24px;
                        border:1px solid #333; color:#888; font-size:13px; line-height:1.6;">
                <strong style="color:#E50914;">ℹ️ Note:</strong>
                Recommendations are based on <strong>genre similarity</strong> using TF-IDF vectors
                and cosine similarity scores. A higher percentage means the two movies share more
                genre characteristics. This model does not analyse plot descriptions or user preferences.
            </div>
            """,
            unsafe_allow_html=True,
        )

elif not selected_movie:
    # Prompt card
    st.markdown(
        """
        <div style="background:#1f1f1f; border-radius:12px; padding:60px 40px; text-align:center;
                    border:2px dashed #333; margin-top:20px;">
            <div style="font-size:56px; margin-bottom:16px;">🎬</div>
            <div style="font-size:20px; font-weight:700; color:#FFFFFF; margin-bottom:10px;">
                Choose a Movie to Get Started
            </div>
            <div style="font-size:14px; color:#888; max-width:460px; margin:0 auto; line-height:1.7;">
                Select any movie from the dropdown above and click
                <strong style="color:#E50914;">Get Recommendations</strong>
                to discover similar films.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ #
# Footer
# ------------------------------------------------------------------ #
st.markdown(
    """
    <hr style="border-color:#2a2a2a; margin-top:40px;">
    <div style="text-align:center; color:#666; font-size:12px; padding:16px 0 32px;">
        CineMatch · Content-Based Filtering · TF-IDF + Cosine Similarity
    </div>
    """,
    unsafe_allow_html=True,
)
