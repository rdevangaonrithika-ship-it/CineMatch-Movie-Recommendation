"""
utils/data_loader.py
--------------------
Responsible for loading and validating the MovieLens dataset.

Functions
---------
load_movies()   – Load movies.csv into a DataFrame.
load_ratings()  – Load ratings.csv into a DataFrame.
load_dataset()  – Load both files and return them together.
"""

import os
import sys
import subprocess
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------ #
# Paths
# ------------------------------------------------------------------ #
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MOVIES_PATH = os.path.join(DATA_DIR, "movies.csv")
RATINGS_PATH = os.path.join(DATA_DIR, "ratings.csv")


def _ensure_dataset_exists():
    """
    If movies.csv or ratings.csv is missing, try to download the
    real MovieLens dataset first; fall back to the sample generator.
    """
    if os.path.exists(MOVIES_PATH) and os.path.exists(RATINGS_PATH):
        return  # already present

    download_script = os.path.join(DATA_DIR, "download_data.py")
    sample_script = os.path.join(DATA_DIR, "generate_sample_data.py")

    # 1. Try the real download
    if os.path.exists(download_script):
        try:
            subprocess.run([sys.executable, download_script], timeout=60, check=False)
        except Exception:
            pass

    # 2. If still missing, generate sample data
    if not (os.path.exists(MOVIES_PATH) and os.path.exists(RATINGS_PATH)):
        if os.path.exists(sample_script):
            try:
                subprocess.run([sys.executable, sample_script], timeout=30, check=False)
            except Exception:
                pass


@st.cache_data(show_spinner=False)
def load_movies() -> pd.DataFrame:
    """
    Load movies.csv.

    Returns
    -------
    pd.DataFrame with columns: movieId, title, genres
    """
    _ensure_dataset_exists()

    if not os.path.exists(MOVIES_PATH):
        raise FileNotFoundError(
            f"movies.csv not found at {MOVIES_PATH}.\n"
            "Please run:  python data/download_data.py\n"
            "or:          python data/generate_sample_data.py"
        )

    df = pd.read_csv(MOVIES_PATH)

    # Validate expected columns
    required = {"movieId", "title", "genres"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"movies.csv is missing columns: {missing}")

    return df


@st.cache_data(show_spinner=False)
def load_ratings() -> pd.DataFrame:
    """
    Load ratings.csv.

    Returns
    -------
    pd.DataFrame with columns: userId, movieId, rating, timestamp
    """
    _ensure_dataset_exists()

    if not os.path.exists(RATINGS_PATH):
        raise FileNotFoundError(
            f"ratings.csv not found at {RATINGS_PATH}.\n"
            "Please run:  python data/download_data.py\n"
            "or:          python data/generate_sample_data.py"
        )

    df = pd.read_csv(RATINGS_PATH)

    required = {"userId", "movieId", "rating", "timestamp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"ratings.csv is missing columns: {missing}")

    return df


@st.cache_data(show_spinner=False)
def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience wrapper – loads both CSV files.

    Returns
    -------
    (movies_df, ratings_df)
    """
    movies_df = load_movies()
    ratings_df = load_ratings()
    return movies_df, ratings_df
