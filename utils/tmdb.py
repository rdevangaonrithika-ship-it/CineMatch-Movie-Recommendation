"""
utils/tmdb.py
-------------
TMDB API client for CineMatch.

Provides:
  - Poster URL fetching by movie title + year
  - Movie detail fetching (overview, runtime, rating, backdrop)
  - TV / Web-series search and detail fetching
  - In-process LRU cache (no disk writes needed)
  - Graceful fallback when API key is absent or request fails
  - API key read from st.secrets["TMDB_API_KEY"] or env var TMDB_API_KEY
  - NEVER hardcodes the key

Usage in Streamlit pages:
    from utils.tmdb import get_poster_url, get_movie_details, search_tv_series

Setup (optional — app works without it):
    1. Get a free API key from https://www.themoviedb.org/settings/api
    2. Create .streamlit/secrets.toml in the project root:
           TMDB_API_KEY = "your_key_here"
    3. OR set an environment variable:
           set TMDB_API_KEY=your_key_here    (Windows)
           export TMDB_API_KEY=your_key_here (Linux/macOS)
"""

import os
import re
import time
import functools
from typing import Optional

# ── Lazy imports so the module loads even without requests installed ──────────
try:
    import requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

try:
    import streamlit as st
    _ST_OK = True
except ImportError:
    _ST_OK = False

# ── TMDB base URLs ────────────────────────────────────────────────────────────
_BASE        = "https://api.themoviedb.org/3"
_IMG_BASE_W  = "https://image.tmdb.org/t/p/w500"   # poster  500 px wide
_IMG_BASE_B  = "https://image.tmdb.org/t/p/w1280"  # backdrop 1280 px wide
_IMG_BASE_O  = "https://image.tmdb.org/t/p/original"

# ── Placeholder SVGs embedded as data-URIs (no external dependency) ───────────
# Each genre family gets a distinct colour so the grid still looks varied.
_GENRE_PLACEHOLDER_COLORS = {
    "action":      ("#7f1d1d", "#ef4444", "💥"),
    "adventure":   ("#064e3b", "#10b981", "🗺️"),
    "animation":   ("#1e3a5f", "#3b82f6", "🎨"),
    "children":    ("#4c1d95", "#8b5cf6", "🧒"),
    "comedy":      ("#78350f", "#f59e0b", "😂"),
    "crime":       ("#111827", "#6b7280", "🔫"),
    "documentary": ("#1e3a5f", "#60a5fa", "🎥"),
    "drama":       ("#1a1a2e", "#818cf8", "🎭"),
    "fantasy":     ("#312e81", "#a78bfa", "🧙"),
    "horror":      ("#3b0000", "#f87171", "👻"),
    "musical":     ("#4a1d96", "#c084fc", "🎵"),
    "mystery":     ("#0f172a", "#94a3b8", "🔍"),
    "romance":     ("#831843", "#f472b6", "❤️"),
    "sci-fi":      ("#0c1a3e", "#38bdf8", "🚀"),
    "scifi":       ("#0c1a3e", "#38bdf8", "🚀"),
    "thriller":    ("#1a0a0a", "#fb923c", "⚡"),
    "war":         ("#1a1a0a", "#a3a300", "🎖️"),
    "western":     ("#2d1a0a", "#d97706", "🤠"),
    "tv movie":    ("#0f2a1a", "#34d399", "📺"),
}
_DEFAULT_PH = ("#12121a", "#e50914", "🎬")


def _placeholder_color(genres: str):
    """Return (bg_dark, accent, icon) for a genre string."""
    first = genres.split("|")[0].strip().lower().replace("-", "")
    return _GENRE_PLACEHOLDER_COLORS.get(first, _DEFAULT_PH)


def placeholder_img_url(genres: str = "", title: str = "") -> str:
    """
    Return a base-64-encoded SVG data-URI placeholder image.
    Each genre family has a distinct colour + icon so cards look varied.
    """
    bg, accent, icon = _placeholder_color(genres)
    # Truncate title for display
    display = (title[:20] + "…") if len(title) > 20 else title
    # Escape XML special chars
    display = (display.replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;")
                       .replace('"', "&quot;"))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="450">'
        f'<defs>'
        f'<linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" style="stop-color:{bg};stop-opacity:1"/>'
        f'<stop offset="100%" style="stop-color:#0a0a0f;stop-opacity:1"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<rect width="300" height="450" fill="url(#g)"/>'
        # border
        f'<rect x="1" y="1" width="298" height="448" fill="none" '
        f'stroke="{accent}" stroke-width="1" stroke-opacity="0.25" rx="8"/>'
        # film strip left
        f'<rect x="8" y="0" width="16" height="450" fill="{bg}" opacity="0.6"/>'
        + "".join(
            f'<rect x="11" y="{y}" width="10" height="18" fill="{accent}" opacity="0.3" rx="2"/>'
            for y in range(8, 450, 32)
        )
        # film strip right
        + f'<rect x="276" y="0" width="16" height="450" fill="{bg}" opacity="0.6"/>'
        + "".join(
            f'<rect x="279" y="{y}" width="10" height="18" fill="{accent}" opacity="0.3" rx="2"/>'
            for y in range(8, 450, 32)
        )
        # icon
        + f'<text x="150" y="210" font-size="64" text-anchor="middle" '
        f'dominant-baseline="middle" opacity="0.6">{icon}</text>'
        # title
        + f'<text x="150" y="310" font-size="13" font-family="Arial,sans-serif" '
        f'fill="#ffffff" text-anchor="middle" dominant-baseline="middle" '
        f'opacity="0.7">{display}</text>'
        # accent line
        + f'<rect x="100" y="338" width="100" height="2" fill="{accent}" opacity="0.5" rx="1"/>'
        # genre label
        + f'<text x="150" y="360" font-size="10" font-family="Arial,sans-serif" '
        f'fill="{accent}" text-anchor="middle" dominant-baseline="middle" '
        f'opacity="0.8">{genres.split("|")[0].strip().upper()}</text>'
        + f'</svg>'
    )
    import base64
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"


# ── API key resolution ────────────────────────────────────────────────────────
def _get_api_key() -> Optional[str]:
    """
    Read the TMDB API key from:
      1. st.secrets["TMDB_API_KEY"]
      2. Environment variable TMDB_API_KEY
    Returns None if neither is set.
    """
    if _ST_OK:
        try:
            key = st.secrets.get("TMDB_API_KEY", None)
            if key:
                return str(key).strip()
        except Exception:
            pass
    return os.environ.get("TMDB_API_KEY", "").strip() or None


def has_api_key() -> bool:
    """Return True if a TMDB API key is configured."""
    return bool(_get_api_key())


# ── Simple in-process cache (functools.lru_cache on the inner helpers) ────────
@functools.lru_cache(maxsize=2000)
def _tmdb_search_movie(title: str, year: str) -> Optional[dict]:
    """
    Call TMDB /search/movie and return the best matching result dict,
    or None on failure / no match.
    Cached: same (title, year) pair is never fetched twice per process.
    """
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return None
    params = {
        "api_key": key,
        "query":   title,
        "language": "en-US",
        "page": 1,
    }
    if year:
        params["year"] = year
    try:
        r = requests.get(
            f"{_BASE}/search/movie", params=params, timeout=5
        )
        if r.status_code != 200:
            return None
        results = r.json().get("results", [])
        if not results:
            # Retry without year constraint
            if year:
                params.pop("year", None)
                r2 = requests.get(
                    f"{_BASE}/search/movie", params=params, timeout=5
                )
                if r2.status_code == 200:
                    results = r2.json().get("results", [])
        return results[0] if results else None
    except Exception:
        return None


@functools.lru_cache(maxsize=2000)
def _tmdb_movie_details(tmdb_id: int) -> Optional[dict]:
    """Fetch full movie details from TMDB /movie/{id}. Cached by TMDB id."""
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return None
    try:
        r = requests.get(
            f"{_BASE}/movie/{tmdb_id}",
            params={"api_key": key, "language": "en-US"},
            timeout=5,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


@functools.lru_cache(maxsize=500)
def _tmdb_search_tv(title: str, year: str) -> Optional[dict]:
    """Search TMDB /search/tv and return best match."""
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return None
    params = {"api_key": key, "query": title, "language": "en-US", "page": 1}
    if year:
        params["first_air_date_year"] = year
    try:
        r = requests.get(f"{_BASE}/search/tv", params=params, timeout=5)
        if r.status_code != 200:
            return None
        results = r.json().get("results", [])
        return results[0] if results else None
    except Exception:
        return None


@functools.lru_cache(maxsize=500)
def _tmdb_tv_details(tmdb_id: int) -> Optional[dict]:
    """Fetch full TV series details."""
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return None
    try:
        r = requests.get(
            f"{_BASE}/tv/{tmdb_id}",
            params={"api_key": key, "language": "en-US"},
            timeout=5,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


@functools.lru_cache(maxsize=200)
def _tmdb_trending(media_type: str = "movie", time_window: str = "week") -> list:
    """
    Fetch trending movies or TV shows.
    media_type: 'movie' | 'tv'
    time_window: 'day' | 'week'
    """
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return []
    try:
        r = requests.get(
            f"{_BASE}/trending/{media_type}/{time_window}",
            params={"api_key": key, "language": "en-US"},
            timeout=5,
        )
        return r.json().get("results", []) if r.status_code == 200 else []
    except Exception:
        return []


@functools.lru_cache(maxsize=200)
def _tmdb_popular(media_type: str = "movie") -> list:
    """Fetch popular movies or TV shows."""
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return []
    try:
        r = requests.get(
            f"{_BASE}/{media_type}/popular",
            params={"api_key": key, "language": "en-US", "page": 1},
            timeout=5,
        )
        return r.json().get("results", []) if r.status_code == 200 else []
    except Exception:
        return []


@functools.lru_cache(maxsize=200)
def _tmdb_top_rated(media_type: str = "movie") -> list:
    """Fetch top-rated movies or TV shows."""
    key = _get_api_key()
    if not key or not _REQUESTS_OK:
        return []
    try:
        r = requests.get(
            f"{_BASE}/{media_type}/top_rated",
            params={"api_key": key, "language": "en-US", "page": 1},
            timeout=5,
        )
        return r.json().get("results", []) if r.status_code == 200 else []
    except Exception:
        return []


# ── Public API ────────────────────────────────────────────────────────────────

def get_poster_url(title: str, year: str = "", genres: str = "") -> str:
    """
    Return a poster image URL for the given movie title.

    Priority:
      1. TMDB poster path  →  full URL via _IMG_BASE_W
      2. Genre-coloured SVG placeholder (always available, never random)

    Parameters
    ----------
    title  : Movie title (with or without year suffix like "(1995)")
    year   : Release year string, e.g. "1995". Extracted from title if blank.
    genres : Pipe-separated genre string used for placeholder colour.
    """
    # Extract year from title if not given separately
    if not year:
        m = re.search(r"\((\d{4})\)\s*$", title)
        year = m.group(1) if m else ""

    # Clean title (remove year suffix for search)
    clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
    # Remove common "The, A, An" article moves (e.g. "President, The" → "The President")
    if clean_title.endswith(", The"):
        clean_title = "The " + clean_title[:-5]
    elif clean_title.endswith(", A"):
        clean_title = "A " + clean_title[:-3]
    elif clean_title.endswith(", An"):
        clean_title = "An " + clean_title[:-4]

    result = _tmdb_search_movie(clean_title, year)
    if result and result.get("poster_path"):
        return f"{_IMG_BASE_W}{result['poster_path']}"

    return placeholder_img_url(genres, title)


def get_backdrop_url(title: str, year: str = "", genres: str = "") -> str:
    """Return a backdrop (wide) image URL, falls back to poster, then placeholder."""
    if not year:
        m = re.search(r"\((\d{4})\)\s*$", title)
        year = m.group(1) if m else ""
    clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
    result = _tmdb_search_movie(clean_title, year)
    if result:
        if result.get("backdrop_path"):
            return f"{_IMG_BASE_B}{result['backdrop_path']}"
        if result.get("poster_path"):
            return f"{_IMG_BASE_W}{result['poster_path']}"
    return placeholder_img_url(genres, title)


def get_movie_details(title: str, year: str = "", genres: str = "") -> dict:
    """
    Return a rich detail dict for a movie.

    Always returns a dict — never raises. Falls back gracefully.

    Keys returned:
      title, year, genres, overview, runtime_min, vote_average,
      vote_count, poster_url, backdrop_url, tmdb_id,
      release_date, original_language, tagline
    """
    if not year:
        m = re.search(r"\((\d{4})\)\s*$", title)
        year = m.group(1) if m else ""
    clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    base = {
        "title":             title,
        "year":              year,
        "genres":            genres,
        "overview":          "",
        "runtime_min":       0,
        "vote_average":      0.0,
        "vote_count":        0,
        "poster_url":        placeholder_img_url(genres, title),
        "backdrop_url":      placeholder_img_url(genres, title),
        "tmdb_id":           0,
        "release_date":      year,
        "original_language": "",
        "tagline":           "",
    }

    search = _tmdb_search_movie(clean_title, year)
    if not search:
        return base

    base["tmdb_id"]    = search.get("id", 0)
    base["vote_average"] = round(search.get("vote_average", 0.0), 1)
    base["vote_count"]   = search.get("vote_count", 0)
    base["overview"]     = search.get("overview", "")
    base["release_date"] = search.get("release_date", year)

    if search.get("poster_path"):
        base["poster_url"]   = f"{_IMG_BASE_W}{search['poster_path']}"
    if search.get("backdrop_path"):
        base["backdrop_url"] = f"{_IMG_BASE_B}{search['backdrop_path']}"

    # Fetch full details for runtime & tagline
    if base["tmdb_id"]:
        details = _tmdb_movie_details(base["tmdb_id"])
        if details:
            base["runtime_min"]       = details.get("runtime", 0) or 0
            base["tagline"]           = details.get("tagline", "") or ""
            base["original_language"] = details.get("original_language", "") or ""
            if details.get("genres"):
                base["genres"] = " | ".join(g["name"] for g in details["genres"])

    return base


def get_tv_poster_url(title: str, year: str = "", genres: str = "") -> str:
    """Return a poster URL for a TV series."""
    clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
    result = _tmdb_search_tv(clean_title, year)
    if result and result.get("poster_path"):
        return f"{_IMG_BASE_W}{result['poster_path']}"
    return placeholder_img_url(genres or "Drama", title)


def get_tv_details(title: str, year: str = "", genres: str = "") -> dict:
    """Return a rich detail dict for a TV series."""
    if not year:
        m = re.search(r"\((\d{4})\)\s*$", title)
        year = m.group(1) if m else ""
    clean_title = re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    base = {
        "title":        title,
        "year":         year,
        "genres":       genres,
        "overview":     "",
        "vote_average": 0.0,
        "poster_url":   placeholder_img_url(genres or "Drama", title),
        "backdrop_url": placeholder_img_url(genres or "Drama", title),
        "tmdb_id":      0,
        "first_air_date": year,
        "seasons":      0,
        "episodes":     0,
    }

    search = _tmdb_search_tv(clean_title, year)
    if not search:
        return base

    base["tmdb_id"]       = search.get("id", 0)
    base["vote_average"]  = round(search.get("vote_average", 0.0), 1)
    base["overview"]      = search.get("overview", "")
    base["first_air_date"]= search.get("first_air_date", year)

    if search.get("poster_path"):
        base["poster_url"]   = f"{_IMG_BASE_W}{search['poster_path']}"
    if search.get("backdrop_path"):
        base["backdrop_url"] = f"{_IMG_BASE_B}{search['backdrop_path']}"

    if base["tmdb_id"]:
        details = _tmdb_tv_details(base["tmdb_id"])
        if details:
            base["seasons"]  = details.get("number_of_seasons", 0) or 0
            base["episodes"] = details.get("number_of_episodes", 0) or 0
            if details.get("genres"):
                base["genres"] = " | ".join(g["name"] for g in details["genres"])

    return base


def get_trending_movies(n: int = 20) -> list[dict]:
    """
    Return up to n trending movies from TMDB (this week).
    Each dict has: title, year, overview, poster_url, vote_average, tmdb_id, genres
    Falls back to empty list if no API key.
    """
    results = _tmdb_trending("movie", "week")
    out = []
    for r in results[:n]:
        poster = (f"{_IMG_BASE_W}{r['poster_path']}"
                  if r.get("poster_path") else
                  placeholder_img_url("", r.get("title", "")))
        year = (r.get("release_date", "") or "")[:4]
        out.append({
            "title":        r.get("title", ""),
            "year":         year,
            "overview":     r.get("overview", ""),
            "poster_url":   poster,
            "vote_average": round(r.get("vote_average", 0.0), 1),
            "tmdb_id":      r.get("id", 0),
            "genres":       "",
        })
    return out


def get_trending_tv(n: int = 20) -> list[dict]:
    """Return up to n trending TV series from TMDB."""
    results = _tmdb_trending("tv", "week")
    out = []
    for r in results[:n]:
        poster = (f"{_IMG_BASE_W}{r['poster_path']}"
                  if r.get("poster_path") else
                  placeholder_img_url("Drama", r.get("name", "")))
        year = (r.get("first_air_date", "") or "")[:4]
        out.append({
            "title":        r.get("name", ""),
            "year":         year,
            "overview":     r.get("overview", ""),
            "poster_url":   poster,
            "vote_average": round(r.get("vote_average", 0.0), 1),
            "tmdb_id":      r.get("id", 0),
            "genres":       "",
        })
    return out


def get_popular_tv(n: int = 20) -> list[dict]:
    """Return up to n popular TV series from TMDB."""
    results = _tmdb_popular("tv")
    out = []
    for r in results[:n]:
        poster = (f"{_IMG_BASE_W}{r['poster_path']}"
                  if r.get("poster_path") else
                  placeholder_img_url("Drama", r.get("name", "")))
        year = (r.get("first_air_date", "") or "")[:4]
        out.append({
            "title":        r.get("name", ""),
            "year":         year,
            "overview":     r.get("overview", ""),
            "poster_url":   poster,
            "vote_average": round(r.get("vote_average", 0.0), 1),
            "tmdb_id":      r.get("id", 0),
            "genres":       "",
        })
    return out


def get_top_rated_movies(n: int = 20) -> list[dict]:
    """Return up to n top-rated movies from TMDB."""
    results = _tmdb_top_rated("movie")
    out = []
    for r in results[:n]:
        poster = (f"{_IMG_BASE_W}{r['poster_path']}"
                  if r.get("poster_path") else
                  placeholder_img_url("", r.get("title", "")))
        year = (r.get("release_date", "") or "")[:4]
        out.append({
            "title":        r.get("title", ""),
            "year":         year,
            "overview":     r.get("overview", ""),
            "poster_url":   poster,
            "vote_average": round(r.get("vote_average", 0.0), 1),
            "tmdb_id":      r.get("id", 0),
            "genres":       "",
        })
    return out


def clear_cache():
    """Clear all in-process TMDB caches (useful after API key change)."""
    _tmdb_search_movie.cache_clear()
    _tmdb_movie_details.cache_clear()
    _tmdb_search_tv.cache_clear()
    _tmdb_tv_details.cache_clear()
    _tmdb_trending.cache_clear()
    _tmdb_popular.cache_clear()
    _tmdb_top_rated.cache_clear()
