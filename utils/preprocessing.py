"""
utils/preprocessing.py
-----------------------
All data-cleaning and feature-preparation steps live here.

Functions
---------
clean_movies(df)            – Clean the movies DataFrame.
prepare_genre_features(df)  – Prepare the genre text for TF-IDF.
get_genre_list(df)          – Return a sorted list of unique genres.
get_popular_movies(movies, ratings, n) – Top-N movies by rating count.
"""

import re
import pandas as pd
import streamlit as st


# ------------------------------------------------------------------ #
# Constants
# ------------------------------------------------------------------ #
UNKNOWN_GENRE_PLACEHOLDER = "Unknown"


def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw movies DataFrame.

    Steps
    -----
    1. Drop rows with missing movieId or title.
    2. Remove exact duplicate rows.
    3. Replace '(no genres listed)' with a placeholder.
    4. Strip leading/trailing whitespace from titles and genres.
    5. Reset the index.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame loaded from movies.csv.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    df = df.copy()

    # 1. Drop rows missing essential fields
    df.dropna(subset=["movieId", "title"], inplace=True)

    # 2. Remove fully duplicate rows
    df.drop_duplicates(inplace=True)

    # 3. Handle missing/unknown genres
    df["genres"] = df["genres"].fillna(UNKNOWN_GENRE_PLACEHOLDER)
    df["genres"] = df["genres"].replace("(no genres listed)", UNKNOWN_GENRE_PLACEHOLDER)

    # 4. Strip whitespace
    df["title"] = df["title"].str.strip()
    df["genres"] = df["genres"].str.strip()

    # 5. Ensure movieId is integer
    df["movieId"] = pd.to_numeric(df["movieId"], errors="coerce").astype("Int64")
    df.dropna(subset=["movieId"], inplace=True)

    df.reset_index(drop=True, inplace=True)
    return df


def prepare_genre_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the genre text so TF-IDF can process it correctly.

    MovieLens genres are separated by '|'.
    We replace '|' with a space so each genre becomes a separate
    token for TF-IDF, e.g.:
        "Action|Adventure|Sci-Fi"  →  "Action Adventure SciFi"

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned movies DataFrame with a 'genres' column.

    Returns
    -------
    pd.DataFrame
        DataFrame with an added 'genre_features' column.
    """
    df = df.copy()

    def _clean_genre_string(genre_str: str) -> str:
        # Replace pipe separator with space
        text = genre_str.replace("|", " ")
        # Remove hyphens inside genre names (e.g. Sci-Fi → SciFi)
        # so they are treated as single tokens by TF-IDF
        text = text.replace("-", "")
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    df["genre_features"] = df["genres"].apply(_clean_genre_string)

    return df


@st.cache_data(show_spinner=False)
def get_genre_list(df: pd.DataFrame) -> list[str]:
    """
    Extract all unique individual genres from the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned movies DataFrame.

    Returns
    -------
    list[str]
        Sorted list of genre strings.
    """
    all_genres = set()
    for genre_str in df["genres"]:
        for g in genre_str.split("|"):
            g = g.strip()
            if g and g != UNKNOWN_GENRE_PLACEHOLDER:
                all_genres.add(g)
    return sorted(all_genres)


@st.cache_data(show_spinner=False)
def get_popular_movies(
    movies_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    n: int = 20,
) -> pd.DataFrame:
    """
    Return the top-N most-rated movies joined with their genre info.

    Parameters
    ----------
    movies_df  : cleaned movies DataFrame
    ratings_df : ratings DataFrame
    n          : number of movies to return

    Returns
    -------
    pd.DataFrame with columns: movieId, title, genres, rating_count, avg_rating
    """
    # Count how many ratings each movie has
    rating_stats = (
        ratings_df.groupby("movieId")["rating"]
        .agg(rating_count="count", avg_rating="mean")
        .reset_index()
    )
    rating_stats["avg_rating"] = rating_stats["avg_rating"].round(2)

    # Merge with movie metadata
    popular = movies_df.merge(rating_stats, on="movieId", how="inner")

    # Sort by rating count descending, then by avg_rating
    popular = popular.sort_values(
        ["rating_count", "avg_rating"], ascending=[False, False]
    ).head(n)

    popular.reset_index(drop=True, inplace=True)
    return popular
