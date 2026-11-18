"""
tests/test_poster_integration.py
---------------------------------
Verifies the TMDB module, poster helpers and all new page files.
Run:  python tests/test_poster_integration.py
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# ── 1. TMDB module imports ────────────────────────────────────────────────────
print("--- 1. TMDB module imports ---")
from utils.tmdb import (
    get_poster_url, get_movie_details, get_tv_poster_url, get_tv_details,
    get_trending_movies, get_trending_tv, get_popular_tv,
    get_top_rated_movies, has_api_key, placeholder_img_url, clear_cache
)
print("  imports: OK")
print(f"  has_api_key: {has_api_key()}")

# ── 2. Placeholder SVG (no API key needed) ────────────────────────────────────
print("--- 2. Placeholder SVG ---")
ph = placeholder_img_url("Action|Adventure", "Test Movie (2024)")
assert ph.startswith("data:image/svg+xml;base64,"), "Bad placeholder URI"
assert len(ph) > 200, "Placeholder too short"
print(f"  placeholder_img_url: OK  ({len(ph)} chars)")

# Each genre gives a DIFFERENT placeholder
ph2 = placeholder_img_url("Horror", "Scary Movie")
ph3 = placeholder_img_url("Comedy", "Funny Film")
assert ph != ph2 != ph3, "Placeholders should differ by genre"
print("  genre-distinct placeholders: OK")

# ── 3. get_poster_url without API key ─────────────────────────────────────────
print("--- 3. get_poster_url (no API key) ---")
url = get_poster_url("Toy Story (1995)", "1995", "Animation|Children|Comedy")
assert url.startswith("data:"), "Should fall back to placeholder without key"
assert len(url) > 100
print(f"  returns placeholder: OK  ({url[:50]}...)")

# ── 4. get_movie_details without API key ──────────────────────────────────────
print("--- 4. get_movie_details (no API key) ---")
det = get_movie_details("The Dark Knight (2008)", "2008", "Action|Crime|Drama")
required_keys = ["title","year","genres","overview","runtime_min","vote_average",
                 "poster_url","backdrop_url","tmdb_id","release_date","tagline"]
for k in required_keys:
    assert k in det, f"Missing key: {k}"
assert det["poster_url"].startswith("data:")
print(f"  all {len(required_keys)} keys present: OK")

# ── 5. TV / Series functions ──────────────────────────────────────────────────
print("--- 5. TV series functions ---")
tv_url = get_tv_poster_url("Breaking Bad", "2008", "Crime|Drama")
assert tv_url.startswith("data:") or tv_url.startswith("https://")
print(f"  get_tv_poster_url: OK")

tv_det = get_tv_details("Stranger Things")
for k in ["title","year","genres","overview","poster_url","vote_average"]:
    assert k in tv_det, f"Missing TV key: {k}"
print(f"  get_tv_details: all keys present OK")

# ── 6. Trending / popular lists return lists ──────────────────────────────────
print("--- 6. List functions ---")
for fn_name, fn in [
    ("get_trending_movies", get_trending_movies),
    ("get_trending_tv",     get_trending_tv),
    ("get_popular_tv",      get_popular_tv),
    ("get_top_rated_movies",get_top_rated_movies),
]:
    result = fn(5)
    assert isinstance(result, list), f"{fn_name} did not return list"
    print(f"  {fn_name}: returns list len={len(result)}  OK")

# ── 7. poster_card_html ───────────────────────────────────────────────────────
print("--- 7. poster_card_html ---")
from utils.styles import poster_card_html, movie_card_html
html = poster_card_html(
    title="Toy Story (1995)", poster_url=ph,
    genres="Animation|Children|Comedy",
    year="1995", rating="4.2",
    similarity_pct="87.5%", rank=1, is_tv=False,
)
assert "poster-card"  in html
assert "Toy Story"    in html
assert "87.5%"        in html
assert "poster-img"   in html
assert "#1"           in html
print(f"  poster_card_html: OK  ({len(html)} chars)")

# TV variant
html_tv = poster_card_html("Breaking Bad","data:x","Crime",year="2008",is_tv=True)
assert "tv-badge" in html_tv or "SERIES" in html_tv
print(f"  poster_card_html (TV): OK")

# backward-compat movie_card_html
old_html = movie_card_html("Toy Story (1995)","Animation|Children|Comedy",
                            year="1995", rating="4.2", rank=1)
assert len(old_html) > 100
print("  movie_card_html (compat): OK")

# ── 8. New files exist on disk ────────────────────────────────────────────────
print("--- 8. File existence ---")
expected = [
    "utils/tmdb.py",
    "utils/styles.py",
    "pages/5_Web_Series.py",
    ".streamlit/secrets.toml",
    "app.py",
    "pages/1_Recommend_Movies.py",
    "pages/2_Explore_Movies.py",
    "pages/3_About_Project.py",
    "pages/4_Watchlist.py",
]
for rel in expected:
    full = os.path.join(ROOT, rel)
    assert os.path.exists(full), f"MISSING: {rel}"
    print(f"  [OK] {rel}")

# ── 9. Original ML tests still pass ──────────────────────────────────────────
print("--- 9. ML recommender sanity ---")
import pandas as pd
from utils.data_loader   import load_movies
from models.recommender  import MovieRecommender
movies = load_movies()
rec    = MovieRecommender()
rec.build(movies)
titles = rec.get_all_titles()
result = rec.recommend_movies(titles[0], 10)
assert result["success"]
assert len(result["recommendations"]) == min(10, rec.n_movies - 1)
scores = [r["similarity_score"] for r in result["recommendations"]]
assert scores == sorted(scores, reverse=True)
print(f"  ML build: {rec.n_movies} movies, {rec.n_features} features")
print(f"  recommend_movies: {len(result['recommendations'])} results, sorted: OK")

print()
print("=" * 55)
print("  ALL POSTER INTEGRATION CHECKS PASSED")
print("=" * 55)
