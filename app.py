"""
app.py  –  CineMatch Home Page
-------------------------------
Entry point for the Streamlit multi-page application.
Run with:
    python -m streamlit run app.py
"""

import os
import sys
import subprocess

import streamlit as st

# ── Project root on sys.path ──────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Bootstrap data + assets once ─────────────────────────────────────────────
def _bootstrap():
    data_dir     = os.path.join(ROOT, "data")
    movies_path  = os.path.join(data_dir, "movies.csv")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    if not (os.path.exists(movies_path) and os.path.exists(ratings_path)):
        for script in ("download_data.py", "generate_sample_data.py"):
            sp = os.path.join(data_dir, script)
            if os.path.exists(sp):
                subprocess.run([sys.executable, sp], timeout=60, check=False)
            if os.path.exists(movies_path) and os.path.exists(ratings_path):
                break
    asset_script = os.path.join(ROOT, "assets", "create_assets.py")
    if os.path.exists(asset_script):
        subprocess.run([sys.executable, asset_script], timeout=15, check=False)

_bootstrap()

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.data_loader   import load_movies, load_ratings
from utils.preprocessing import clean_movies, get_popular_movies, get_genre_list
from utils.styles        import (
    inject_global_css, sidebar_nav, section_header,
    movie_card_html, empty_state, extract_year, strip_year,
)
from models.recommender  import get_recommender

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "CineMatch – Discover Movies",
    page_icon  = "🎬",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

inject_global_css()
sidebar_nav("home")

# ── Session state ─────────────────────────────────────────────────────────────
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Load data (all cached) ────────────────────────────────────────────────────
with st.spinner("Loading CineMatch…"):
    try:
        movies_raw   = load_movies()
        ratings_df   = load_ratings()
        recommender  = get_recommender()
        movies_clean = clean_movies(movies_raw)
        data_ok      = True
    except Exception as exc:
        st.error(f"⚠️ Could not load dataset: {exc}")
        data_ok = False

# ═════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg,
            #0d0014 0%, #0a0a0f 40%, #0a0a14 70%, #0d0014 100%);
        border-bottom: 1px solid #1e2a3a;
        padding: 72px 48px 60px;
        position: relative;
        overflow: hidden;
        margin-bottom: 0;
    ">
      <!-- glow blobs -->
      <div style="position:absolute;top:-80px;left:-80px;width:400px;height:400px;
                  border-radius:50%;
                  background:radial-gradient(circle,rgba(229,9,20,0.07) 0%,transparent 70%);
                  pointer-events:none;"></div>
      <div style="position:absolute;bottom:-100px;right:-60px;width:500px;height:500px;
                  border-radius:50%;
                  background:radial-gradient(circle,rgba(124,58,237,0.07) 0%,transparent 70%);
                  pointer-events:none;"></div>

      <!-- eyebrow -->
      <div style="display:inline-flex;align-items:center;gap:8px;
                  background:rgba(229,9,20,0.1);border:1px solid rgba(229,9,20,0.25);
                  border-radius:20px;padding:5px 14px;margin-bottom:22px;">
        <span style="width:6px;height:6px;border-radius:50%;background:#e50914;
                     animation:pulse 2s infinite;display:inline-block;"></span>
        <span style="font-size:11px;font-weight:700;color:#e50914;letter-spacing:1.5px;
                     text-transform:uppercase;">Now Discovering</span>
      </div>

      <h1 style="font-size:clamp(2.2rem,5vw,3.6rem);font-weight:900;color:#f1f1f1;
                 letter-spacing:-2px;line-height:1.1;max-width:700px;margin-bottom:18px;">
        Discover Your Next<br>
        <span style="background:linear-gradient(135deg,#e50914,#7c3aed);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                     background-clip:text;">Favourite Movie.</span>
      </h1>

      <p style="font-size:17px;color:#8892a4;max-width:520px;line-height:1.7;
                margin-bottom:36px;">
        Powered by Machine Learning. Find movies that match your taste in seconds
        using genre-based content filtering.
      </p>

      <!-- CTA row -->
      <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
        <a href="/1_Recommend_Movies" target="_self"
           style="display:inline-flex;align-items:center;gap:8px;
                  background:linear-gradient(135deg,#e50914,#c40812);
                  color:#fff;border-radius:8px;padding:12px 28px;
                  font-size:14px;font-weight:700;text-decoration:none;
                  box-shadow:0 4px 20px rgba(229,9,20,0.4);
                  transition:all 0.2s;">
          🎯 Get Recommendations
        </a>
        <a href="/2_Explore_Movies" target="_self"
           style="display:inline-flex;align-items:center;gap:8px;
                  background:transparent;color:#f1f1f1;border-radius:8px;
                  padding:12px 28px;font-size:14px;font-weight:600;
                  text-decoration:none;border:1px solid #2d3748;
                  transition:all 0.2s;">
          🔍 Explore Movies
        </a>
      </div>
    </div>

    <style>
    @keyframes pulse {
      0%,100%{opacity:1;transform:scale(1);}
      50%{opacity:.5;transform:scale(1.4);}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Page content wrapper ──────────────────────────────────────────────────────
st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# STATS ROW
# ═════════════════════════════════════════════════════════════════════════════
if data_ok:
    stats = recommender.get_model_stats()
    n_genres = len(get_genre_list(movies_clean))

    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, label in [
        (s1, f"{stats['n_movies']:,}",    "Movies Indexed"),
        (s2, str(n_genres),               "Unique Genres"),
        (s3, f"{len(ratings_df):,}",      "User Ratings"),
        (s4, f"{stats['n_features']}",    "TF-IDF Features"),
    ]:
        with col:
            st.markdown(
                f'<div class="cm-stat-card">'
                f'<div class="cm-stat-num">{num}</div>'
                f'<div class="cm-stat-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ═════════════════════════════════════════════════════════════════════════════
# TRENDING / POPULAR MOVIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🔥 Trending Movies", "Most-rated films in the dataset")

if data_ok:
    try:
        popular = get_popular_movies(movies_clean, ratings_df, n=20)
    except Exception:
        popular = movies_clean.head(20).copy()
        popular["avg_rating"]   = 0.0
        popular["rating_count"] = 0

    cols = st.columns(5)
    for i, (_, row) in enumerate(popular.head(10).iterrows()):
        year   = extract_year(row["title"])
        rating = f"{row['avg_rating']:.1f}" if row.get("avg_rating", 0) > 0 else ""
        with cols[i % 5]:
            st.markdown(
                movie_card_html(
                    title   = row["title"],
                    genres  = row["genres"],
                    year    = year,
                    rating  = rating,
                ),
                unsafe_allow_html=True,
            )

    # second row
    st.markdown("<br>", unsafe_allow_html=True)
    cols2 = st.columns(5)
    for i, (_, row) in enumerate(popular.iloc[10:20].iterrows()):
        year   = extract_year(row["title"])
        rating = f"{row['avg_rating']:.1f}" if row.get("avg_rating", 0) > 0 else ""
        with cols2[i % 5]:
            st.markdown(
                movie_card_html(
                    title  = row["title"],
                    genres = row["genres"],
                    year   = year,
                    rating = rating,
                ),
                unsafe_allow_html=True,
            )
else:
    empty_state("🎬", "Movies unavailable", "Dataset could not be loaded.")

# ═════════════════════════════════════════════════════════════════════════════
# ML-POWERED RECOMMENDATIONS TEASER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🤖 Recommended For You", "Pick a movie — our ML engine finds similar ones instantly")

if data_ok:
    all_titles = recommender.get_all_titles()
    with st.container():
        pick_col, btn_col = st.columns([3, 1])
        with pick_col:
            chosen = st.selectbox(
                "Choose a movie to get recommendations:",
                options=[""] + all_titles,
                format_func=lambda x: "— Select a movie —" if x == "" else x,
                key="home_movie_pick",
                label_visibility="collapsed",
            )
        with btn_col:
            find_btn = st.button(
                "🎯 Find Similar",
                use_container_width=True,
                disabled=(not chosen),
            )

    if find_btn and chosen:
        with st.spinner("Analysing with TF-IDF + Cosine Similarity…"):
            result = recommender.recommend_movies(chosen, 5)

        if result["success"]:
            st.markdown(
                f'<p style="color:#8892a4;font-size:13px;margin:12px 0 20px;">'
                f'Showing 5 movies similar to <strong style="color:#f1f1f1;">'
                f'{result["query_title"]}</strong> · '
                f'Found in {result["recommendation_time_sec"]}s</p>',
                unsafe_allow_html=True,
            )
            rcols = st.columns(5)
            for i, rec in enumerate(result["recommendations"]):
                year = extract_year(rec["title"])
                with rcols[i]:
                    st.markdown(
                        movie_card_html(
                            title           = rec["title"],
                            genres          = rec["genres"],
                            year            = year,
                            similarity_pct  = rec["similarity_pct"],
                            similarity_score= rec["similarity_score"],
                            rank            = i + 1,
                        ),
                        unsafe_allow_html=True,
                    )
            st.markdown(
                '<div style="text-align:right;margin-top:12px;">'
                '<a href="/1_Recommend_Movies" target="_self" '
                'style="color:#e50914;font-size:13px;font-weight:600;text-decoration:none;">'
                'View full recommendations →</a></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
                unsafe_allow_html=True,
            )
    elif not chosen:
        st.markdown(
            """
            <div style="background:#12121a;border:1px dashed #1e2a3a;border-radius:12px;
                        padding:40px;text-align:center;">
              <div style="font-size:36px;margin-bottom:10px;">🎬</div>
              <div style="color:#8892a4;font-size:14px;">
                Select a movie above to see ML-powered recommendations.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ═════════════════════════════════════════════════════════════════════════════
# EXPLORE BY GENRE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🎭 Explore By Genre", "Browse movies by category")

GENRE_META = {
    "Action":      ("💥", "linear-gradient(135deg,#7f1d1d,#991b1b)"),
    "Comedy":      ("😂", "linear-gradient(135deg,#78350f,#92400e)"),
    "Drama":       ("🎭", "linear-gradient(135deg,#1e3a5f,#1e40af)"),
    "Thriller":    ("⚡", "linear-gradient(135deg,#1a0a0a,#450a0a)"),
    "Romance":     ("❤️", "linear-gradient(135deg,#831843,#9d174d)"),
    "Horror":      ("👻", "linear-gradient(135deg,#1a0000,#3b0000)"),
    "Sci-Fi":      ("🚀", "linear-gradient(135deg,#0c1a3e,#1e3a8a)"),
    "Animation":   ("🎨", "linear-gradient(135deg,#064e3b,#065f46)"),
    "Adventure":   ("🗺️", "linear-gradient(135deg,#0f4c2a,#065f46)"),
    "Fantasy":     ("🧙", "linear-gradient(135deg,#312e81,#4c1d95)"),
    "Crime":       ("🔫", "linear-gradient(135deg,#111827,#1f2937)"),
    "Mystery":     ("🔍", "linear-gradient(135deg,#0f172a,#1e293b)"),
}

if data_ok:
    # count movies per genre
    genre_counts: dict = {}
    for genre_str in movies_clean["genres"]:
        for g in genre_str.split("|"):
            g = g.strip()
            if g and g != "Unknown":
                genre_counts[g] = genre_counts.get(g, 0) + 1

    genre_names = list(GENRE_META.keys())
    rows_g = [genre_names[:6], genre_names[6:]]
    for row_g in rows_g:
        gcols = st.columns(len(row_g))
        for col, gname in zip(gcols, row_g):
            icon, grad = GENRE_META[gname]
            cnt = genre_counts.get(gname, 0)
            with col:
                st.markdown(
                    f"""
                    <div class="genre-card" style="background:{grad};">
                      <div class="genre-card-icon">{icon}</div>
                      <div class="genre-card-label">{gname}</div>
                      <div class="genre-card-count">{cnt} movies</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# HOW IT WORKS – 3-STEP
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
section_header("⚙️ How CineMatch Works")

hw_cols = st.columns(3)
steps = [
    ("01", "🗂️", "Pick a Movie",
     "Choose any title from our library of movies spanning every genre."),
    ("02", "🧮", "TF-IDF Analysis",
     "Genres are converted into numerical vectors using Term Frequency–Inverse Document Frequency."),
    ("03", "🎯", "Cosine Similarity",
     "Similarity scores are computed instantly. The closest matches are returned as recommendations."),
]
for col, (num, icon, title, desc) in zip(hw_cols, steps):
    with col:
        st.markdown(
            f"""
            <div style="background:#12121a;border:1px solid #1e2a3a;border-radius:14px;
                        padding:28px 24px;height:100%;transition:border-color 0.2s;"
                 onmouseover="this.style.borderColor='rgba(229,9,20,0.3)'"
                 onmouseout="this.style.borderColor='#1e2a3a'">
              <div style="font-size:11px;color:#e50914;font-weight:800;
                          letter-spacing:2px;margin-bottom:12px;">{num}</div>
              <div style="font-size:30px;margin-bottom:12px;">{icon}</div>
              <div style="font-size:15px;font-weight:700;color:#f1f1f1;
                          margin-bottom:10px;">{title}</div>
              <div style="font-size:13px;color:#8892a4;line-height:1.65;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <div class="cm-footer" style="margin-top:56px;">
      <strong style="color:#f1f1f1;">CineMatch</strong> &nbsp;·&nbsp;
      ML-Powered Movie Discovery &nbsp;·&nbsp;
      Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens</a>
      by GroupLens Research
    </div>
    </div>
    """,  # closes .cm-page
    unsafe_allow_html=True,
)
