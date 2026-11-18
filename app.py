"""
app.py  –  CineMatch Home Page
Run with:  python -m streamlit run app.py
"""

import os, sys, subprocess
import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Bootstrap ─────────────────────────────────────────────────────────────────
def _bootstrap():
    dd = os.path.join(ROOT, "data")
    mp, rp = os.path.join(dd, "movies.csv"), os.path.join(dd, "ratings.csv")
    if not (os.path.exists(mp) and os.path.exists(rp)):
        for sc in ("download_data.py", "generate_sample_data.py"):
            sp = os.path.join(dd, sc)
            if os.path.exists(sp):
                subprocess.run([sys.executable, sp], timeout=60, check=False)
            if os.path.exists(mp) and os.path.exists(rp):
                break
    asc = os.path.join(ROOT, "assets", "create_assets.py")
    if os.path.exists(asc):
        subprocess.run([sys.executable, asc], timeout=15, check=False)

_bootstrap()

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.data_loader   import load_movies, load_ratings
from utils.preprocessing import clean_movies, get_popular_movies, get_genre_list
from utils.styles        import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, empty_state, extract_year,
)
from utils.tmdb import (
    get_poster_url, get_trending_movies, get_top_rated_movies,
    has_api_key, placeholder_img_url,
)
from models.recommender import get_recommender

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Discover Movies",
    page_icon="🎬", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("home")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Load data ─────────────────────────────────────────────────────────────────
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
# HERO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:linear-gradient(135deg,#0d0014 0%,#0a0a0f 40%,#0a0a14 70%,#0d0014 100%);
            border-bottom:1px solid #1e2a3a;padding:72px 48px 60px;
            position:relative;overflow:hidden;">
  <div style="position:absolute;top:-80px;left:-80px;width:400px;height:400px;border-radius:50%;
              background:radial-gradient(circle,rgba(229,9,20,0.07) 0%,transparent 70%);
              pointer-events:none;"></div>
  <div style="position:absolute;bottom:-100px;right:-60px;width:500px;height:500px;border-radius:50%;
              background:radial-gradient(circle,rgba(124,58,237,0.07) 0%,transparent 70%);
              pointer-events:none;"></div>
  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(229,9,20,0.1);
              border:1px solid rgba(229,9,20,0.25);border-radius:20px;padding:5px 14px;
              margin-bottom:22px;">
    <span style="width:6px;height:6px;border-radius:50%;background:#e50914;
                 display:inline-block;"></span>
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
  <p style="font-size:17px;color:#8892a4;max-width:520px;line-height:1.7;margin-bottom:36px;">
    ML-powered recommendations · Beautiful posters · Browse movies &amp; web series
  </p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
    <a href="/1_Recommend_Movies" target="_self"
       style="display:inline-flex;align-items:center;gap:8px;
              background:linear-gradient(135deg,#e50914,#c40812);color:#fff;
              border-radius:8px;padding:12px 28px;font-size:14px;font-weight:700;
              text-decoration:none;box-shadow:0 4px 20px rgba(229,9,20,0.4);">
      🎯 Get Recommendations
    </a>
    <a href="/2_Explore_Movies" target="_self"
       style="display:inline-flex;align-items:center;gap:8px;background:transparent;
              color:#f1f1f1;border-radius:8px;padding:12px 28px;font-size:14px;
              font-weight:600;text-decoration:none;border:1px solid #2d3748;">
      🔍 Explore Movies
    </a>
    <a href="/5_Web_Series" target="_self"
       style="display:inline-flex;align-items:center;gap:8px;background:transparent;
              color:#a78bfa;border-radius:8px;padding:12px 28px;font-size:14px;
              font-weight:600;text-decoration:none;border:1px solid rgba(124,58,237,0.4);">
      📺 Web Series
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── API key notice ────────────────────────────────────────────────────────────
if not has_api_key():
    st.markdown("""
    <div class="api-banner">
      <span style="font-size:20px;">🔑</span>
      <div>
        <strong>Add a TMDB API key for real movie posters.</strong>
        Create <code>.streamlit/secrets.toml</code> and add
        <code>TMDB_API_KEY = "your_key"</code>.
        Get a free key at
        <a href="https://www.themoviedb.org/settings/api" target="_blank"
           style="color:#e50914;">themoviedb.org</a>.
        The app works without it — genre-coloured placeholders are shown instead.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if data_ok:
    stats    = recommender.get_model_stats()
    n_genres = len(get_genre_list(movies_clean))
    s1,s2,s3,s4 = st.columns(4)
    for col, num, lbl in [
        (s1, f"{stats['n_movies']:,}", "Movies Indexed"),
        (s2, str(n_genres),            "Unique Genres"),
        (s3, f"{len(ratings_df):,}",   "User Ratings"),
        (s4, str(stats['n_features']), "TF-IDF Features"),
    ]:
        with col:
            st.markdown(
                f'<div class="cm-stat-card">'
                f'<div class="cm-stat-num">{num}</div>'
                f'<div class="cm-stat-label">{lbl}</div>'
                f'</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TRENDING MOVIES  (TMDB if key present, else popular from dataset)
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🔥 Trending Movies", "What the world is watching this week")

trending_tmdb = get_trending_movies(10) if has_api_key() else []

if trending_tmdb:
    cols = st.columns(5)
    for i, item in enumerate(trending_tmdb[:10]):
        with cols[i % 5]:
            st.markdown(
                poster_card_html(
                    title      = item["title"],
                    poster_url = item["poster_url"],
                    year       = item["year"],
                    rating     = str(item["vote_average"]) if item["vote_average"] > 0 else "",
                ),
                unsafe_allow_html=True,
            )
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)
elif data_ok:
    # Fallback: popular from dataset with genre-coloured placeholders
    try:
        popular = get_popular_movies(movies_clean, ratings_df, n=10)
    except Exception:
        popular = movies_clean.head(10).copy()
        popular["avg_rating"] = 0.0

    cols = st.columns(5)
    for i, (_, row) in enumerate(popular.iterrows()):
        year   = extract_year(row["title"])
        rating = f"{row['avg_rating']:.1f}" if row.get("avg_rating", 0) > 0 else ""
        poster = get_poster_url(row["title"], year, row["genres"])
        with cols[i % 5]:
            st.markdown(
                poster_card_html(
                    title      = row["title"],
                    poster_url = poster,
                    genres     = row["genres"],
                    year       = year,
                    rating     = rating,
                ),
                unsafe_allow_html=True,
            )
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)
else:
    empty_state("🎬","Movies unavailable","Dataset could not be loaded.")

# ═════════════════════════════════════════════════════════════════════════════
# TOP RATED MOVIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("⭐ Top Rated Movies", "Critically acclaimed films you shouldn't miss")

top_rated_tmdb = get_top_rated_movies(10) if has_api_key() else []

if top_rated_tmdb:
    cols = st.columns(5)
    for i, item in enumerate(top_rated_tmdb[:10]):
        with cols[i % 5]:
            st.markdown(
                poster_card_html(
                    title      = item["title"],
                    poster_url = item["poster_url"],
                    year       = item["year"],
                    rating     = str(item["vote_average"]) if item["vote_average"] > 0 else "",
                ),
                unsafe_allow_html=True,
            )
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)
elif data_ok:
    top_df = movies_clean.sample(min(10, len(movies_clean)), random_state=42)
    cols   = st.columns(5)
    for i, (_, row) in enumerate(top_df.iterrows()):
        year   = extract_year(row["title"])
        poster = get_poster_url(row["title"], year, row["genres"])
        with cols[i % 5]:
            st.markdown(
                poster_card_html(
                    title=row["title"], poster_url=poster,
                    genres=row["genres"], year=year,
                ),
                unsafe_allow_html=True,
            )
        if i == 4:
            st.markdown("<br>", unsafe_allow_html=True)
            cols = st.columns(5)

# ═════════════════════════════════════════════════════════════════════════════
# RECOMMENDED FOR YOU  (ML teaser)
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🤖 Recommended For You", "Pick a movie — our ML engine finds similar ones instantly")

if data_ok:
    all_titles = recommender.get_all_titles()
    pc, bc     = st.columns([3, 1])
    with pc:
        chosen = st.selectbox(
            "Choose a movie:",
            [""] + all_titles,
            format_func=lambda x: "— Select a movie —" if x == "" else x,
            key="home_pick",
            label_visibility="collapsed",
        )
    with bc:
        find = st.button("🎯 Find Similar", disabled=not chosen, use_container_width=True)

    if find and chosen:
        with st.spinner("Calculating recommendations…"):
            result = recommender.recommend_movies(chosen, 5)
        if result["success"]:
            st.markdown(
                f'<p style="color:#8892a4;font-size:13px;margin:10px 0 18px;">'
                f'5 movies similar to <strong style="color:#f1f1f1;">'
                f'{result["query_title"]}</strong> · '
                f'{result["recommendation_time_sec"]}s</p>',
                unsafe_allow_html=True,
            )
            rcols = st.columns(5)
            for i, rec in enumerate(result["recommendations"]):
                year   = extract_year(rec["title"])
                poster = get_poster_url(rec["title"], year, rec["genres"])
                with rcols[i]:
                    st.markdown(
                        poster_card_html(
                            title          = rec["title"],
                            poster_url     = poster,
                            genres         = rec["genres"],
                            year           = year,
                            similarity_pct = rec["similarity_pct"],
                            rank           = i + 1,
                        ),
                        unsafe_allow_html=True,
                    )
            st.markdown(
                '<div style="text-align:right;margin-top:12px;">'
                '<a href="/1_Recommend_Movies" target="_self" '
                'style="color:#e50914;font-size:13px;font-weight:600;text-decoration:none;">'
                'Full recommendations page →</a></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
                unsafe_allow_html=True,
            )
    elif not chosen:
        st.markdown("""
        <div style="background:#12121a;border:1px dashed #1e2a3a;border-radius:12px;
                    padding:40px;text-align:center;">
          <div style="font-size:36px;margin-bottom:10px;">🎬</div>
          <div style="color:#8892a4;font-size:14px;">
            Select a movie above to see ML-powered recommendations.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# EXPLORE BY GENRE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🎭 Explore By Genre", "Browse movies by category")

GENRE_META = {
    "Action":    ("💥","linear-gradient(135deg,#7f1d1d,#991b1b)"),
    "Comedy":    ("😂","linear-gradient(135deg,#78350f,#92400e)"),
    "Drama":     ("🎭","linear-gradient(135deg,#1e3a5f,#1e40af)"),
    "Thriller":  ("⚡","linear-gradient(135deg,#1a0a0a,#450a0a)"),
    "Romance":   ("❤️","linear-gradient(135deg,#831843,#9d174d)"),
    "Horror":    ("👻","linear-gradient(135deg,#1a0000,#3b0000)"),
    "Sci-Fi":    ("🚀","linear-gradient(135deg,#0c1a3e,#1e3a8a)"),
    "Animation": ("🎨","linear-gradient(135deg,#064e3b,#065f46)"),
    "Adventure": ("🗺️","linear-gradient(135deg,#0f4c2a,#065f46)"),
    "Fantasy":   ("🧙","linear-gradient(135deg,#312e81,#4c1d95)"),
    "Crime":     ("🔫","linear-gradient(135deg,#111827,#1f2937)"),
    "Mystery":   ("🔍","linear-gradient(135deg,#0f172a,#1e293b)"),
}

if data_ok:
    gcounts = {}
    for gs in movies_clean["genres"]:
        for g in gs.split("|"):
            g = g.strip()
            if g and g != "Unknown":
                gcounts[g] = gcounts.get(g, 0) + 1

    gnames = list(GENRE_META.keys())
    for row_names in [gnames[:6], gnames[6:]]:
        gcols = st.columns(len(row_names))
        for col, gname in zip(gcols, row_names):
            icon, grad = GENRE_META[gname]
            cnt = gcounts.get(gname, 0)
            with col:
                st.markdown(
                    f'<div class="genre-card" style="background:{grad};">'
                    f'<div class="genre-card-icon">{icon}</div>'
                    f'<div class="genre-card-label">{gname}</div>'
                    f'<div class="genre-card-count">{cnt} movies</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# WEB SERIES TEASER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
section_header("📺 Trending Web Series", "Popular shows from TMDB")

from utils.tmdb import get_trending_tv
tv_items = get_trending_tv(5) if has_api_key() else []

if tv_items:
    tvcols = st.columns(5)
    for col, item in zip(tvcols, tv_items):
        with col:
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
    st.markdown(
        '<div style="text-align:right;margin-top:12px;">'
        '<a href="/5_Web_Series" target="_self" '
        'style="color:#a78bfa;font-size:13px;font-weight:600;text-decoration:none;">'
        'Browse all web series →</a></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown("""
    <div style="background:#12121a;border:1px dashed #1e2a3a;border-radius:12px;
                padding:32px;text-align:center;">
      <div style="font-size:32px;margin-bottom:8px;">📺</div>
      <div style="color:#8892a4;font-size:13px;">
        Add a TMDB API key to see trending web series posters.
        <a href="/5_Web_Series" target="_self"
           style="color:#a78bfa;font-weight:600;text-decoration:none;">
          Browse Web Series →</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cm-footer" style="margin-top:56px;">
  <strong style="color:#f1f1f1;">CineMatch</strong> &nbsp;·&nbsp;
  ML-Powered Movie Discovery &nbsp;·&nbsp;
  Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens</a>
  by GroupLens Research &nbsp;·&nbsp;
  Posters: <a href="https://www.themoviedb.org/" target="_blank">TMDB</a>
</div>
</div>
""", unsafe_allow_html=True)
