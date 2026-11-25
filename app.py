"""
app.py  –  CineMatch Home Page
Streamlit Entry Point
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
    lp, pp = os.path.join(ROOT, "assets", "logo.png"), os.path.join(ROOT, "assets", "placeholder.png")
    if not (os.path.exists(lp) and os.path.exists(pp)):
        asc = os.path.join(ROOT, "assets", "create_assets.py")
        if os.path.exists(asc):
            subprocess.run([sys.executable, asc], timeout=15, check=False)

_bootstrap()

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.data_loader   import load_movies, load_ratings
from utils.preprocessing import clean_movies, get_popular_movies, get_genre_list
from utils.styles        import (
    inject_global_css, sidebar_nav, section_header,
    poster_card_html, horizontal_scroll_row_html, empty_state, extract_year,
)
from utils.tmdb import (
    get_poster_url, get_trending_movies, get_top_rated_movies,
    get_trending_tv, has_api_key, placeholder_img_url,
)
from models.recommender import get_recommender

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Stream & Discover",
    page_icon="🎬", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("home")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading CineMatch catalogue…"):
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
# CINEMATIC HERO SECTION
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background: linear-gradient(180deg, rgba(14,14,24,0.4) 0%, rgba(8,8,12,0.92) 80%, #08080c 100%),
            radial-gradient(circle at 80% 20%, rgba(124,58,237,0.18) 0%, transparent 60%),
            radial-gradient(circle at 10% 80%, rgba(229,9,20,0.16) 0%, transparent 50%),
            #0b0c14;
            border-bottom: 1px solid #1a1b28; padding: 76px 48px 56px;
            position: relative; overflow: hidden; border-radius: 0 0 24px 24px;">
  
  <div style="display:inline-flex; align-items:center; gap:8px;
              background:rgba(229,9,20,0.12); border:1px solid rgba(229,9,20,0.3);
              border-radius:24px; padding:6px 16px; margin-bottom:24px;">
    <span style="width:8px; height:8px; border-radius:50%; background:#e50914;
                 box-shadow: 0 0 10px #e50914; display:inline-block;"></span>
    <span style="font-size:11px; font-weight:800; color:#ffffff; letter-spacing:1.5px;
                 text-transform:uppercase;">CineMatch Original Discovery</span>
  </div>

  <h1 style="font-size:clamp(2.4rem, 5.5vw, 4.2rem); font-weight:900; color:#ffffff;
             letter-spacing:-1.8px; line-height:1.08; max-width:820px; margin-bottom:20px;">
    Your Next Favourite Story<br>
    <span style="background:linear-gradient(135deg, #ffffff 30%, #e50914 70%, #a78bfa 100%);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                 background-clip:text;">Starts Here.</span>
  </h1>

  <p style="font-size:18px; color:#94a3b8; max-width:580px; line-height:1.65; margin-bottom:34px; font-weight:400;">
    Discover movies and series worth watching. ML-powered recommendations, stunning posters, and curated collections.
  </p>

  <div style="display:flex; gap:14px; flex-wrap:wrap; align-items:center;">
    <a href="/2_Explore_Movies" target="_self"
       style="display:inline-flex; align-items:center; gap:8px;
              background:linear-gradient(135deg, #e50914 0%, #c40812 100%); color:#ffffff;
              border-radius:10px; padding:13px 32px; font-size:15px; font-weight:700;
              text-decoration:none; box-shadow:0 6px 25px rgba(229,9,20,0.45); transition:transform 0.2s;">
      🍿 Explore Now
    </a>
    <a href="/1_Recommend_Movies" target="_self"
       style="display:inline-flex; align-items:center; gap:8px;
              background:rgba(255,255,255,0.06); color:#f1f1f1; border-radius:10px;
              padding:13px 28px; font-size:15px; font-weight:600; text-decoration:none;
              border:1px solid #2a2b3d; backdrop-filter:blur(10px);">
      🎯 Get Recommendations
    </a>
    <a href="/5_Web_Series" target="_self"
       style="display:inline-flex; align-items:center; gap:8px;
              background:rgba(124,58,237,0.12); color:#c4b5fd; border-radius:10px;
              padding:13px 28px; font-size:15px; font-weight:600; text-decoration:none;
              border:1px solid rgba(124,58,237,0.35);">
      📺 Web Series
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

# ── Hero Search Bar ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
hero_search_col1, hero_search_col2 = st.columns([5, 1])
with hero_search_col1:
    home_query = st.text_input(
        "Search catalogue",
        placeholder="🔍  Search across thousands of movies and series by title...",
        key="home_instant_search",
        label_visibility="collapsed",
    )
with hero_search_col2:
    search_nav_btn = st.button("Explore All", use_container_width=True, key="home_search_btn")
    if search_nav_btn:
        st.switch_page("pages/2_Explore_Movies.py")

if home_query.strip() and data_ok:
    matched = movies_clean[
        movies_clean["title"].str.contains(home_query.strip(), case=False, na=False)
    ].head(10)
    st.markdown("<br>", unsafe_allow_html=True)
    section_header(f'🔍 Search Results for "{home_query.strip()}"', f"Found {len(matched)} matching titles")
    if len(matched) == 0:
        empty_state("🔍", "No Movies Matched", "Try searching with a different keyword or browse our catalogue.")
    else:
        search_items = []
        for _, row in matched.iterrows():
            year = extract_year(row["title"])
            poster = get_poster_url(row["title"], year, row["genres"])
            search_items.append({
                "title": row["title"],
                "poster_url": poster,
                "year": year,
                "genres": row["genres"],
            })
        st.markdown(horizontal_scroll_row_html(search_items), unsafe_allow_html=True)

# ── API Key Notice Banner (if offline/unconfigured) ───────────────────────────
if not has_api_key():
    st.markdown("""
    <div class="api-banner">
      <span style="font-size:22px;">🔑</span>
      <div>
        <strong>TMDB API key optional for real streaming posters.</strong>
        Add <code>TMDB_API_KEY = "your_key"</code> in <code>.streamlit/secrets.toml</code> to stream official high-res studio posters.
        The platform operates smoothly offline with dynamic genre-themed artwork.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Stats Overview Bar ────────────────────────────────────────────────────────
if data_ok:
    stats = recommender.get_model_stats()
    n_genres = len(get_genre_list(movies_clean))
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in [
        (s1, f"{stats['n_movies']:,}", "Movies Indexed"),
        (s2, str(n_genres),            "Unique Genres"),
        (s3, f"{len(ratings_df):,}",   "Audience Ratings"),
        (s4, str(stats['n_features']), "ML Feature Weights"),
    ]:
        with col:
            st.markdown(
                f'<div class="cm-stat-card">'
                f'<div class="cm-stat-num">{num}</div>'
                f'<div class="cm-stat-label">{lbl}</div>'
                f'</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# 1. TRENDING MOVIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🔥 Trending Movies", "Most watched and talked about this week")

trending_tmdb = get_trending_movies(10) if has_api_key() else []
trending_items = []

if trending_tmdb:
    for item in trending_tmdb[:10]:
        trending_items.append({
            "title": item["title"],
            "poster_url": item["poster_url"],
            "year": item["year"],
            "rating": str(item["vote_average"]) if item["vote_average"] > 0 else "",
            "genres": "",
        })
elif data_ok:
    try:
        popular = get_popular_movies(movies_clean, ratings_df, n=10)
    except Exception:
        popular = movies_clean.head(10).copy()
        popular["avg_rating"] = 0.0

    for _, row in popular.iterrows():
        year = extract_year(row["title"])
        rating = f"{row['avg_rating']:.1f}" if row.get("avg_rating", 0) > 0 else ""
        poster = get_poster_url(row["title"], year, row["genres"])
        trending_items.append({
            "title": row["title"],
            "poster_url": poster,
            "year": year,
            "rating": rating,
            "genres": row["genres"],
        })

if trending_items:
    st.markdown(horizontal_scroll_row_html(trending_items), unsafe_allow_html=True)
else:
    empty_state("🎬", "Trending Movies Unavailable", "Dataset could not be loaded.")

# ═════════════════════════════════════════════════════════════════════════════
# 2. POPULAR MOVIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🌟 Popular Movies", "All-time community favourites with highest audience engagement")

if data_ok:
    try:
        pop_df = get_popular_movies(movies_clean, ratings_df, n=10)
    except Exception:
        pop_df = movies_clean.sample(min(10, len(movies_clean)), random_state=42)
        pop_df["avg_rating"] = 0.0

    pop_items = []
    for _, row in pop_df.iterrows():
        year = extract_year(row["title"])
        rating = f"{row['avg_rating']:.1f}" if row.get("avg_rating", 0) > 0 else ""
        poster = get_poster_url(row["title"], year, row["genres"])
        pop_items.append({
            "title": row["title"],
            "poster_url": poster,
            "year": year,
            "rating": rating,
            "genres": row["genres"],
        })
    st.markdown(horizontal_scroll_row_html(pop_items), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# 3. TRENDING WEB SERIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("📺 Trending Web Series", "Top binge-worthy series from major streaming networks")

tv_items_raw = get_trending_tv(10) if has_api_key() else []
tv_items = []

if tv_items_raw:
    for item in tv_items_raw[:10]:
        tv_items.append({
            "title": item["title"],
            "poster_url": item["poster_url"],
            "year": item["year"],
            "rating": str(item["vote_average"]) if item["vote_average"] > 0 else "",
            "genres": "TV Series",
            "is_tv": True,
        })
else:
    # Curated top web series fallback
    SAMPLE_SERIES_HOME = [
        ("Breaking Bad",      "2008", "Crime | Drama | Thriller"),
        ("Stranger Things",   "2016", "Drama | Fantasy | Horror"),
        ("The Crown",         "2016", "Drama | History"),
        ("Money Heist",       "2017", "Action | Crime | Drama"),
        ("Dark",              "2017", "Drama | Mystery | Sci-Fi"),
        ("Squid Game",        "2021", "Action | Drama | Mystery"),
        ("The Witcher",       "2019", "Action | Adventure | Fantasy"),
        ("Wednesday",         "2022", "Comedy | Fantasy | Horror"),
        ("The Last of Us",    "2023", "Action | Adventure | Drama"),
        ("Succession",        "2018", "Drama"),
    ]
    for s_title, s_year, s_genres in SAMPLE_SERIES_HOME:
        poster = placeholder_img_url(s_genres, s_title)
        tv_items.append({
            "title": s_title,
            "poster_url": poster,
            "year": s_year,
            "genres": s_genres,
            "is_tv": True,
        })

st.markdown(horizontal_scroll_row_html(tv_items), unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:right; margin-top:8px;">'
    '<a href="/5_Web_Series" target="_self" '
    'style="color:#a78bfa; font-size:13px; font-weight:700; text-decoration:none;">'
    'Browse All Web Series →</a></div>',
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
# 4. RECOMMENDED FOR YOU (Interactive ML Recommender)
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🤖 Recommended For You", "Pick any title to unlock instant ML-powered matches")

if data_ok:
    all_titles = recommender.get_all_titles()
    pc, bc = st.columns([4, 1.2])
    with pc:
        chosen = st.selectbox(
            "Choose a movie:",
            [""] + all_titles,
            format_func=lambda x: "— Select a movie to discover similar films —" if x == "" else x,
            key="home_pick",
            label_visibility="collapsed",
        )
    with bc:
        find = st.button("🎯 Find Similar", disabled=not chosen, use_container_width=True)

    if find and chosen:
        with st.spinner("Calculating ML recommendations…"):
            result = recommender.recommend_movies(chosen, 5)
        if result["success"]:
            st.markdown(
                f'<p style="color:#94a3b8; font-size:14px; margin:12px 0 20px;">'
                f'Top matches similar to <strong style="color:#ffffff;">'
                f'{result["query_title"]}</strong> &nbsp;·&nbsp; '
                f'Processed in {result["recommendation_time_sec"]}s</p>',
                unsafe_allow_html=True,
            )
            rcols = st.columns(5)
            wl_titles = [m["title"] for m in st.session_state.watchlist]
            wl_adds = []
            wl_rems = []
            for i, rec in enumerate(result["recommendations"]):
                year = extract_year(rec["title"])
                poster = get_poster_url(rec["title"], year, rec["genres"])
                in_wl = rec["title"] in wl_titles
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
                    if in_wl:
                        if st.button("❤️ Saved", key=f"h_wr_{i}", use_container_width=True):
                            wl_rems.append(rec["title"])
                    else:
                        if st.button("🤍 Watchlist", key=f"h_wa_{i}", use_container_width=True):
                            wl_adds.append({
                                "title": rec["title"],
                                "genres": rec["genres"],
                                "year": year,
                                "poster_url": poster,
                            })

            if wl_adds or wl_rems:
                for item in wl_adds:
                    if item["title"] not in [m["title"] for m in st.session_state.watchlist]:
                        st.session_state.watchlist.append(item)
                st.session_state.watchlist = [
                    m for m in st.session_state.watchlist if m["title"] not in wl_rems
                ]
                st.rerun()

            st.markdown(
                '<div style="text-align:right; margin-top:14px;">'
                '<a href="/1_Recommend_Movies" target="_self" '
                'style="color:#e50914; font-size:13px; font-weight:700; text-decoration:none;">'
                'Go to Full Recommendations Studio →</a></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="cm-toast">⚠️ {result["error_message"]}</div>',
                unsafe_allow_html=True,
            )
    elif not chosen:
        st.markdown("""
        <div style="background:#111118; border:1px dashed #202232; border-radius:14px;
                    padding:44px 32px; text-align:center;">
          <div style="font-size:40px; margin-bottom:12px;">🎬</div>
          <div style="color:#ffffff; font-size:16px; font-weight:700; margin-bottom:6px;">
            Select a movie above to generate instant recommendations
          </div>
          <div style="color:#94a3b8; font-size:13px;">
            Our algorithm analyzes genre vectors and computes similarity scores instantly.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# 5. EXPLORE BY GENRE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
section_header("🎭 Explore By Genre", "Dive into your favourite genres")

GENRE_META = {
    "Action":    ("💥", "linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%)"),
    "Comedy":    ("😂", "linear-gradient(135deg, #78350f 0%, #451a03 100%)"),
    "Drama":     ("🎭", "linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%)"),
    "Thriller":  ("⚡", "linear-gradient(135deg, #1a0a0a 0%, #311010 100%)"),
    "Romance":   ("❤️", "linear-gradient(135deg, #831843 0%, #500724 100%)"),
    "Horror":    ("👻", "linear-gradient(135deg, #2a0808 0%, #150202 100%)"),
    "Sci-Fi":    ("🚀", "linear-gradient(135deg, #0c1a3e 0%, #060d20 100%)"),
    "Animation": ("🎨", "linear-gradient(135deg, #064e3b 0%, #022c22 100%)"),
    "Adventure": ("🗺️", "linear-gradient(135deg, #0f4c2a 0%, #042f1a 100%)"),
    "Fantasy":   ("🧙", "linear-gradient(135deg, #312e81 0%, #1e1b4b 100%)"),
    "Crime":     ("🔫", "linear-gradient(135deg, #181926 0%, #0d0e15 100%)"),
    "Mystery":   ("🔍", "linear-gradient(135deg, #172554 0%, #0b1329 100%)"),
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
# 6. TOP RATED MOVIES
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
section_header("⭐ Top Rated Movies", "Masterpieces celebrated by audiences and critics")

top_rated_tmdb = get_top_rated_movies(10) if has_api_key() else []
top_rated_items = []

if top_rated_tmdb:
    for item in top_rated_tmdb[:10]:
        top_rated_items.append({
            "title": item["title"],
            "poster_url": item["poster_url"],
            "year": item["year"],
            "rating": str(item["vote_average"]) if item["vote_average"] > 0 else "",
            "genres": "",
        })
elif data_ok:
    # Filter high rated movies
    try:
        top_df = movies_clean.merge(
            ratings_df.groupby("movieId")["rating"].agg(avg_rating="mean", count="count").reset_index(),
            on="movieId", how="inner"
        ).sort_values("avg_rating", ascending=False).head(10)
    except Exception:
        top_df = movies_clean.sample(min(10, len(movies_clean)), random_state=42)
        top_df["avg_rating"] = 4.5

    for _, row in top_df.iterrows():
        year = extract_year(row["title"])
        rating = f"{row.get('avg_rating', 4.5):.1f}"
        poster = get_poster_url(row["title"], year, row["genres"])
        top_rated_items.append({
            "title": row["title"],
            "poster_url": poster,
            "genres": row["genres"],
            "year": year,
            "rating": rating,
        })

if top_rated_items:
    st.markdown(horizontal_scroll_row_html(top_rated_items), unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cm-footer">
  <div style="font-size:16px; font-weight:800; color:#f1f1f1; margin-bottom:8px;">🎬 CineMatch</div>
  <div style="color:#8892a4; margin-bottom:12px;">Discover movies and web series worth watching. Powered by TF-IDF &amp; Cosine Similarity.</div>
  <div>Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens</a> by GroupLens Research &nbsp;·&nbsp;
  Media: <a href="https://www.themoviedb.org/" target="_blank">TMDB API</a></div>
</div>
</div>
""", unsafe_allow_html=True)
