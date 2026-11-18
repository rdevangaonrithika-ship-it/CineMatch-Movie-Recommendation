"""
tests/test_ui_integration.py
-----------------------------
Smoke-tests every module that the redesigned UI pages import.
Run with:  python tests/test_ui_integration.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── 1. Data loading ──────────────────────────────────────────────────────────
print("--- 1. Data loading ---")
from utils.data_loader import load_movies, load_ratings
movies  = load_movies()
ratings = load_ratings()
assert len(movies)  > 0, "movies empty"
assert len(ratings) > 0, "ratings empty"
print(f"  movies : {len(movies)} rows  cols={list(movies.columns)}")
print(f"  ratings: {len(ratings)} rows")

# ── 2. Preprocessing ─────────────────────────────────────────────────────────
print("--- 2. Preprocessing ---")
from utils.preprocessing import (
    clean_movies, prepare_genre_features,
    get_genre_list, get_popular_movies,
)
cleaned = clean_movies(movies)
assert len(cleaned) > 0
genres  = get_genre_list(cleaned)
assert len(genres) > 0
pop     = get_popular_movies(cleaned, ratings, 10)
assert "avg_rating"   in pop.columns
assert "rating_count" in pop.columns
print(f"  cleaned: {len(cleaned)} rows")
print(f"  genres : {genres[:6]}")
print(f"  popular: {len(pop)} rows  cols={list(pop.columns)}")

# ── 3. Styles module ─────────────────────────────────────────────────────────
print("--- 3. Styles module ---")
from utils.styles import (
    extract_year, strip_year, movie_card_html,
    GLOBAL_CSS,
)
assert extract_year("Toy Story (1995)")    == "1995"
assert extract_year("Batman")             == ""
assert strip_year("Toy Story (1995)")     == "Toy Story"
assert strip_year("Batman")              == "Batman"
html = movie_card_html(
    title="Toy Story (1995)", genres="Animation|Children|Comedy",
    year="1995", rating="4.1", rank=1,
    similarity_pct="92.0%", similarity_score=0.92,
)
assert len(html) > 100
assert "Toy Story" in html
assert "92.0%" in html
assert len(GLOBAL_CSS) > 500
print(f"  extract_year  : OK")
print(f"  strip_year    : OK")
print(f"  movie_card_html: {len(html)} chars")
print(f"  GLOBAL_CSS    : {len(GLOBAL_CSS)} chars")

# ── 4. Recommender ───────────────────────────────────────────────────────────
print("--- 4. Recommender ---")
from models.recommender import MovieRecommender
rec = MovieRecommender()
rec.build(movies)
assert rec.n_movies  > 0
assert rec.n_features > 0
print(f"  n_movies  : {rec.n_movies}")
print(f"  n_features: {rec.n_features}")
print(f"  build_time: {rec.build_time_sec}s")

titles = rec.get_all_titles()
assert len(titles) > 0
seed   = titles[0]

result = rec.recommend_movies(seed, 10)
assert result["success"],        f"FAIL: {result['error_message']}"
assert len(result["recommendations"]) == min(10, rec.n_movies - 1)
recs   = result["recommendations"]
# query movie must not appear in its own recommendations
rec_titles_lc = [r["title"].lower() for r in recs]
assert seed.lower() not in rec_titles_lc, "Query movie in its own recs!"
# scores must be descending
scores = [r["similarity_score"] for r in recs]
assert scores == sorted(scores, reverse=True), "Recs not sorted!"
# similarity_pct format
for r in recs:
    assert r["similarity_pct"].endswith("%"), f"Bad pct: {r['similarity_pct']}"
print(f"  recommend_movies('{seed}', 10): {len(recs)} recs  OK")
print(f"  first rec: {recs[0]['title']}  ({recs[0]['similarity_pct']})")

# bad title
bad = rec.recommend_movies("XYZZY_NONEXISTENT_99999", 5)
assert not bad["success"]
assert bad["error_message"]
print(f"  bad title handled: '{bad['error_message'][:60]}'")

# get_movie_info
info = rec.get_movie_info(seed)
assert info is not None
assert "title" in info and "genres" in info and "movieId" in info
print(f"  get_movie_info('{seed}'): {info}")

# stats
stats = rec.get_model_stats()
assert stats["n_movies"]  > 0
assert stats["n_features"] > 0
assert stats["build_time_sec"] > 0
print(f"  get_model_stats: {stats}")

# ── 5. avg_rating merge (Discover page logic) ────────────────────────────────
print("--- 5. avg_rating merge (Discover page) ---")
import pandas as pd
rating_avg = (
    ratings.groupby("movieId")["rating"]
    .mean()
    .round(1)
    .to_dict()
)
df = cleaned.copy()
df["avg_rating"] = df["movieId"].map(rating_avg)
rated_count = df["avg_rating"].notna().sum()
print(f"  movies with avg_rating: {rated_count} / {len(df)}")
# min rating filter simulation
threshold = 3.5
filtered = df[df["avg_rating"].fillna(0) >= threshold]
print(f"  movies rated >= {threshold}: {len(filtered)}")

# ── 6. Watchlist session-state keys (structural) ─────────────────────────────
print("--- 6. Watchlist structure ---")
# Simulate the session_state dict operations used by 4_Watchlist.py
fake_wl = []
item1   = {"title": "Toy Story (1995)",   "genres": "Animation|Children|Comedy"}
item2   = {"title": "Jumanji (1995)",     "genres": "Adventure|Children|Fantasy"}
fake_wl.append(item1)
fake_wl.append(item2)
assert len(fake_wl) == 2
# Remove
fake_wl = [m for m in fake_wl if m["title"] != "Toy Story (1995)"]
assert len(fake_wl) == 1
assert fake_wl[0]["title"] == "Jumanji (1995)"
# Duplicate guard
titles_in = [m["title"] for m in fake_wl]
if item2["title"] not in titles_in:
    fake_wl.append(item2)
assert len(fake_wl) == 1          # no duplicate added
print(f"  add/remove/dedup: OK")

# ── 7. Page file existence ───────────────────────────────────────────────────
print("--- 7. Page file existence ---")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
expected = [
    "app.py",
    os.path.join("pages", "1_Recommend_Movies.py"),
    os.path.join("pages", "2_Explore_Movies.py"),
    os.path.join("pages", "3_About_Project.py"),
    os.path.join("pages", "4_Watchlist.py"),
    os.path.join("utils", "styles.py"),
    os.path.join("utils", "data_loader.py"),
    os.path.join("utils", "preprocessing.py"),
    os.path.join("models", "recommender.py"),
    os.path.join("data",   "movies.csv"),
    os.path.join("data",   "ratings.csv"),
]
all_ok = True
for rel in expected:
    full = os.path.join(ROOT, rel)
    exists = os.path.exists(full)
    status = "OK" if exists else "MISSING"
    if not exists:
        all_ok = False
    print(f"  [{status}] {rel}")
assert all_ok, "Some files are missing!"

print()
print("=" * 55)
print("  ALL INTEGRATION CHECKS PASSED")
print("=" * 55)
