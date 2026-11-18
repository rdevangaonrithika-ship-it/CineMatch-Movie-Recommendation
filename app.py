"""
app.py  –  CineMatch Home Page
-------------------------------
Entry point for the Streamlit multi-page application.
Run with:
    streamlit run app.py
"""

import os
import sys
import time

import streamlit as st

# ------------------------------------------------------------------ #
# Make project root importable from any working directory
# ------------------------------------------------------------------ #
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ------------------------------------------------------------------ #
# Ensure dataset files exist (download or generate sample)
# ------------------------------------------------------------------ #
def _bootstrap_data():
    data_dir = os.path.join(ROOT, "data")
    movies_path = os.path.join(data_dir, "movies.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")

    if not (os.path.exists(movies_path) and os.path.exists(ratings_path)):
        # Try real download first
        dl_script = os.path.join(data_dir, "download_data.py")
        gen_script = os.path.join(data_dir, "generate_sample_data.py")
        import subprocess
        if os.path.exists(dl_script):
            subprocess.run([sys.executable, dl_script], timeout=60, check=False)
        if not (os.path.exists(movies_path) and os.path.exists(ratings_path)):
            if os.path.exists(gen_script):
                subprocess.run([sys.executable, gen_script], timeout=30, check=False)

    # Ensure assets exist
    asset_script = os.path.join(ROOT, "assets", "create_assets.py")
    if os.path.exists(asset_script):
        import subprocess
        subprocess.run([sys.executable, asset_script], timeout=15, check=False)

_bootstrap_data()

# ------------------------------------------------------------------ #
# Imports (after bootstrap so data files exist)
# ------------------------------------------------------------------ #
from utils.data_loader import load_movies, load_ratings
from utils.preprocessing import clean_movies, get_popular_movies
from models.recommender import get_recommender

# ------------------------------------------------------------------ #
# Page configuration
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="CineMatch – Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# Global CSS  – Netflix-inspired dark theme
# ------------------------------------------------------------------ #
st.markdown(
    """
    <style>
    /* ---- Global background & font ---- */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] * {
        color: #e5e5e5 !important;
    }

    /* ---- Hide default Streamlit elements ---- */
    #MainMenu, footer, header { visibility: hidden; }

    /* ---- Headings ---- */
    h1 { color: #E50914 !important; font-weight: 800; letter-spacing: -1px; }
    h2 { color: #FFFFFF !important; font-weight: 700; }
    h3 { color: #E50914 !important; font-weight: 600; }

    /* ---- Buttons ---- */
    .stButton > button {
        background-color: #E50914;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 10px 28px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #F40612;
        transform: scale(1.03);
    }

    /* ---- Select boxes & inputs ---- */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-radius: 4px;
    }

    /* ---- Movie cards ---- */
    .movie-card {
        background: linear-gradient(145deg, #1f1f1f, #2a2a2a);
        border-radius: 10px;
        padding: 18px 16px;
        margin-bottom: 16px;
        border-left: 4px solid #E50914;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .movie-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(229,9,20,0.25);
    }
    .movie-title {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .movie-genre {
        color: #b3b3b3;
        font-size: 12px;
        margin-bottom: 8px;
    }
    .similarity-badge {
        display: inline-block;
        background-color: #E50914;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    /* ---- Hero section ---- */
    .hero-section {
        background: linear-gradient(135deg, #1a0000 0%, #141414 50%, #0a0a0a 100%);
        border-radius: 16px;
        padding: 60px 48px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid #2a2a2a;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at center, rgba(229,9,20,0.07) 0%, transparent 60%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 72px;
        font-weight: 900;
        color: #E50914;
        letter-spacing: -3px;
        margin-bottom: 8px;
        line-height: 1;
    }
    .hero-tagline {
        font-size: 24px;
        color: #e5e5e5;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    .hero-desc {
        font-size: 16px;
        color: #b3b3b3;
        max-width: 680px;
        margin: 0 auto 32px auto;
        line-height: 1.7;
    }

    /* ---- Stat cards ---- */
    .stat-card {
        background: #1f1f1f;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #333;
    }
    .stat-number {
        font-size: 36px;
        font-weight: 800;
        color: #E50914;
    }
    .stat-label {
        font-size: 13px;
        color: #b3b3b3;
        margin-top: 4px;
    }

    /* ---- Section header ---- */
    .section-header {
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 20px;
        padding-bottom: 8px;
        border-bottom: 2px solid #E50914;
        display: inline-block;
    }

    /* ---- Popular movie row card ---- */
    .pop-card {
        background: #1f1f1f;
        border-radius: 8px;
        padding: 14px 12px;
        height: 120px;
        border: 1px solid #2a2a2a;
        overflow: hidden;
        transition: border-color 0.2s;
    }
    .pop-card:hover { border-color: #E50914; }
    .pop-title {
        color: #fff;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: 6px;
    }
    .pop-genre {
        color: #888;
        font-size: 11px;
        line-height: 1.4;
    }
    .pop-rating {
        color: #E50914;
        font-size: 12px;
        font-weight: 700;
        margin-top: 6px;
    }

    /* ---- Alert / info boxes ---- */
    .info-box {
        background: #1f1f1f;
        border-left: 4px solid #E50914;
        border-radius: 4px;
        padding: 14px 18px;
        margin: 16px 0;
        color: #e5e5e5;
        font-size: 14px;
    }

    /* ---- Sidebar nav ---- */
    .sidebar-logo {
        font-size: 28px;
        font-weight: 900;
        color: #E50914 !important;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }
    .sidebar-tagline {
        font-size: 11px;
        color: #888 !important;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }
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
    st.markdown("**Navigation**")
    st.page_link("app.py",                          label="🏠  Home",              )
    st.page_link("pages/1_Recommend_Movies.py",     label="🎯  Recommend Movies",  )
    st.page_link("pages/2_Explore_Movies.py",       label="🔍  Explore Movies",    )
    st.page_link("pages/3_About_Project.py",        label="📖  About Project",     )
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:11px; color:#666;">
        ML Mini Project · CSE<br>
        Content-Based Filtering<br>
        TF-IDF + Cosine Similarity
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ #
# Load data & build model (cached)
# ------------------------------------------------------------------ #
with st.spinner("Loading dataset and building model…"):
    try:
        movies_df_raw = load_movies()
        ratings_df    = load_ratings()
        recommender   = get_recommender()
        data_loaded   = True
    except Exception as exc:
        st.error(f"⚠️ Could not load dataset: {exc}")
        data_loaded = False

# ------------------------------------------------------------------ #
# Hero Section
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-title">CineMatch</div>
        <div class="hero-tagline">✦ Discover Movies You'll Love ✦</div>
        <div class="hero-desc">
            A content-based movie recommendation engine powered by
            <strong>TF-IDF Vectorization</strong> and <strong>Cosine Similarity</strong>.
            Select any movie and instantly get the most similar films based on genre analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTA button
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    if st.button("🎯  Explore Movies", use_container_width=True):
        st.switch_page("pages/1_Recommend_Movies.py")

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Stats Row
# ------------------------------------------------------------------ #
if data_loaded:
    cleaned_movies = clean_movies(movies_df_raw)
    n_movies  = len(cleaned_movies)
    n_genres  = len(set(
        g.strip()
        for row in cleaned_movies["genres"]
        for g in row.split("|")
        if g.strip() and g.strip() != "Unknown"
    ))
    n_ratings = len(ratings_df)
    model_stats = recommender.get_model_stats()

    st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-number">{n_movies:,}</div>'
            f'<div class="stat-label">Movies</div></div>',
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-number">{n_genres}</div>'
            f'<div class="stat-label">Unique Genres</div></div>',
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-number">{n_ratings:,}</div>'
            f'<div class="stat-label">Total Ratings</div></div>',
            unsafe_allow_html=True,
        )
    with s4:
        st.markdown(
            f'<div class="stat-card"><div class="stat-number">{model_stats["n_features"]}</div>'
            f'<div class="stat-label">TF-IDF Features</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# How It Works – 3-step visual
# ------------------------------------------------------------------ #
st.markdown('<div class="section-header">⚙️ How It Works</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
steps = [
    ("1️⃣", "Select a Movie",
     "Choose any movie from our dataset using the searchable dropdown on the Recommend Movies page."),
    ("2️⃣", "TF-IDF Analysis",
     "The system converts movie genres into numerical vectors using Term Frequency–Inverse Document Frequency."),
    ("3️⃣", "Cosine Similarity",
     "Similarity scores between all movie vectors are computed. The top similar movies are displayed instantly."),
]
for col, (icon, title, desc) in zip([c1, c2, c3], steps):
    with col:
        st.markdown(
            f"""
            <div class="stat-card" style="text-align:left; padding:24px;">
                <div style="font-size:32px; margin-bottom:10px;">{icon}</div>
                <div style="font-size:16px; font-weight:700; color:#E50914; margin-bottom:8px;">{title}</div>
                <div style="font-size:13px; color:#b3b3b3; line-height:1.6;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Popular Movies Section
# ------------------------------------------------------------------ #
if data_loaded:
    st.markdown('<div class="section-header">🔥 Popular Movies</div>', unsafe_allow_html=True)

    try:
        popular = get_popular_movies(cleaned_movies, ratings_df, n=20)
    except Exception:
        popular = cleaned_movies.head(20).copy()
        popular["avg_rating"] = 0.0
        popular["rating_count"] = 0

    # Show in rows of 5
    PER_ROW = 5
    for row_start in range(0, min(len(popular), 20), PER_ROW):
        row_movies = popular.iloc[row_start : row_start + PER_ROW]
        cols = st.columns(PER_ROW)
        for col, (_, movie) in zip(cols, row_movies.iterrows()):
            genre_short = " | ".join(movie["genres"].split("|")[:2])
            rating_str  = f"⭐ {movie['avg_rating']:.1f}" if movie.get("avg_rating", 0) > 0 else ""
            with col:
                st.markdown(
                    f"""
                    <div class="pop-card">
                        <div class="pop-title">{movie['title']}</div>
                        <div class="pop-genre">{genre_short}</div>
                        <div class="pop-rating">{rating_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Model Info box
# ------------------------------------------------------------------ #
if data_loaded:
    st.markdown(
        f"""
        <div class="info-box">
            <strong>Model Status:</strong>
            Built in <strong>{model_stats['build_time_sec']}s</strong> &nbsp;·&nbsp;
            <strong>{model_stats['n_movies']}</strong> movies indexed &nbsp;·&nbsp;
            <strong>{model_stats['n_features']}</strong> genre features &nbsp;·&nbsp;
            Algorithm: <strong>Content-Based Filtering (TF-IDF + Cosine Similarity)</strong>
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
        CineMatch · ML Mini Project · Content-Based Movie Recommendation System<br>
        Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank"
                   style="color:#E50914;">MovieLens Small</a> by GroupLens Research
    </div>
    """,
    unsafe_allow_html=True,
)
