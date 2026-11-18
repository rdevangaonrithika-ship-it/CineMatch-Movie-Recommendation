"""
models/recommender.py
---------------------
Core Machine Learning module.

This module implements Content-Based Filtering using:
  - TF-IDF Vectorization  (sklearn.feature_extraction.text.TfidfVectorizer)
  - Cosine Similarity     (sklearn.metrics.pairwise.cosine_similarity)

Classes
-------
MovieRecommender
    Builds the TF-IDF feature matrix and provides the
    recommend_movies() function.
"""

import time
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.data_loader import load_movies
from utils.preprocessing import clean_movies, prepare_genre_features


# ------------------------------------------------------------------ #
# MovieRecommender class
# ------------------------------------------------------------------ #

class MovieRecommender:
    """
    Content-Based Movie Recommender using TF-IDF + Cosine Similarity.

    Attributes
    ----------
    movies_df       : cleaned movies DataFrame (movieId, title, genres)
    feature_df      : movies DataFrame with 'genre_features' column
    tfidf_matrix    : scipy sparse matrix of shape (n_movies, n_features)
    vectorizer      : fitted TfidfVectorizer instance
    cosine_sim      : (n_movies × n_movies) numpy array of similarities
    title_to_index  : dict mapping lowercase movie title → row index
    build_time_sec  : seconds taken to build the model
    n_movies        : number of movies in the model
    n_features      : number of TF-IDF features
    """

    def __init__(self):
        self.movies_df: pd.DataFrame | None = None
        self.feature_df: pd.DataFrame | None = None
        self.tfidf_matrix = None
        self.vectorizer: TfidfVectorizer | None = None
        self.cosine_sim: np.ndarray | None = None
        self.title_to_index: dict = {}
        self.build_time_sec: float = 0.0
        self.n_movies: int = 0
        self.n_features: int = 0

    # ---------------------------------------------------------------- #
    # Build / fit
    # ---------------------------------------------------------------- #

    def build(self, movies_df: pd.DataFrame) -> None:
        """
        Fit the TF-IDF vectorizer and compute the cosine-similarity matrix.

        Steps
        -----
        1. Clean the raw movies DataFrame.
        2. Prepare the genre text (pipe-separated → space-separated tokens).
        3. Fit TfidfVectorizer on the genre_features column.
        4. Compute pairwise cosine similarity for every movie pair.
        5. Build a title→index lookup dictionary.

        Parameters
        ----------
        movies_df : pd.DataFrame
            Raw or already-cleaned movies DataFrame.
        """
        start = time.time()

        # Step 1 – Clean
        self.movies_df = clean_movies(movies_df)

        # Step 2 – Prepare genre features
        self.feature_df = prepare_genre_features(self.movies_df)

        # Step 3 – TF-IDF Vectorization
        # min_df=1  : include genres that appear in at least 1 movie
        # max_df=1.0: no upper limit
        # sublinear_tf=True: apply 1 + log(tf) instead of raw tf to
        #                    reduce the influence of very frequent genres
        self.vectorizer = TfidfVectorizer(
            min_df=1,
            max_df=1.0,
            sublinear_tf=True,
            token_pattern=r"[A-Za-z]+"   # match alphabetic genre tokens
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.feature_df["genre_features"]
        )

        # Step 4 – Cosine Similarity matrix
        # Shape: (n_movies × n_movies)
        # cosine_sim[i][j] = cosine similarity between movie i and movie j
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Step 5 – Title lookup (lowercase for case-insensitive search)
        self.title_to_index = {
            title.lower(): idx
            for idx, title in enumerate(self.feature_df["title"])
        }

        self.n_movies = self.tfidf_matrix.shape[0]
        self.n_features = self.tfidf_matrix.shape[1]
        self.build_time_sec = round(time.time() - start, 4)

    # ---------------------------------------------------------------- #
    # Recommend
    # ---------------------------------------------------------------- #

    def recommend_movies(
        self,
        movie_title: str,
        number_of_recommendations: int = 10,
    ) -> dict:
        """
        Return the top-N most similar movies for a given title.

        Algorithm
        ---------
        1. Find the row index of the selected movie.
        2. Retrieve its cosine-similarity vector (one row of cosine_sim).
        3. Sort all movies by descending similarity score.
        4. Skip the selected movie itself (similarity = 1.0 with itself).
        5. Return the top-N results with title, genres, and similarity %.

        Parameters
        ----------
        movie_title              : str  – exact title as it appears in the dataset
        number_of_recommendations: int  – how many movies to return (5 or 10)

        Returns
        -------
        dict with keys:
            "success"         : bool
            "query_title"     : str  – the movie that was searched
            "query_genres"    : str  – its genres
            "recommendations" : list of dicts, each with:
                                  title, genres, similarity_score, similarity_pct
            "recommendation_time_sec" : float
            "error_message"   : str (only when success=False)
        """
        if self.cosine_sim is None:
            return {
                "success": False,
                "error_message": "Model has not been built yet. Call build() first.",
            }

        start = time.time()

        # Case-insensitive lookup
        search_key = movie_title.strip().lower()

        # Handle movies that do not exist in the index
        if search_key not in self.title_to_index:
            # Try partial match
            matches = [
                t for t in self.title_to_index
                if search_key in t
            ]
            if matches:
                suggestion = self.feature_df.iloc[self.title_to_index[matches[0]]]["title"]
                return {
                    "success": False,
                    "error_message": (
                        f"Movie '{movie_title}' not found. "
                        f"Did you mean: '{suggestion}'?"
                    ),
                }
            return {
                "success": False,
                "error_message": (
                    f"Movie '{movie_title}' not found in the dataset. "
                    "Please select a movie from the dropdown."
                ),
            }

        movie_idx = self.title_to_index[search_key]
        query_row = self.feature_df.iloc[movie_idx]

        # Get this movie's similarity scores with every other movie
        # cosine_sim[movie_idx] is a 1-D array of length n_movies
        sim_scores = list(enumerate(self.cosine_sim[movie_idx]))

        # Sort by similarity descending
        sim_scores.sort(key=lambda x: x[1], reverse=True)

        # Remove the query movie itself (score will be 1.0)
        sim_scores = [item for item in sim_scores if item[0] != movie_idx]

        # Take the top-N
        top_n = sim_scores[:number_of_recommendations]

        recommendations = []
        for idx, score in top_n:
            row = self.feature_df.iloc[idx]
            recommendations.append({
                "title": row["title"],
                "genres": row["genres"],
                "similarity_score": round(float(score), 4),
                "similarity_pct": f"{round(float(score) * 100, 1)}%",
            })

        elapsed = round(time.time() - start, 4)

        return {
            "success": True,
            "query_title": query_row["title"],
            "query_genres": query_row["genres"],
            "recommendations": recommendations,
            "recommendation_time_sec": elapsed,
            "error_message": None,
        }

    # ---------------------------------------------------------------- #
    # Utility helpers
    # ---------------------------------------------------------------- #

    def get_all_titles(self) -> list[str]:
        """Return a sorted list of all movie titles in the model."""
        if self.feature_df is None:
            return []
        return sorted(self.feature_df["title"].tolist())

    def get_movie_info(self, movie_title: str) -> dict | None:
        """
        Return basic info (title, genres) for a single movie.
        Returns None if the movie is not found.
        """
        key = movie_title.strip().lower()
        if key not in self.title_to_index:
            return None
        idx = self.title_to_index[key]
        row = self.feature_df.iloc[idx]
        return {
            "title": row["title"],
            "genres": row["genres"],
            "movieId": int(row["movieId"]),
        }

    def get_model_stats(self) -> dict:
        """Return a summary of the fitted model for display."""
        return {
            "n_movies": self.n_movies,
            "n_features": self.n_features,
            "build_time_sec": self.build_time_sec,
            "vectorizer_params": self.vectorizer.get_params() if self.vectorizer else {},
        }


# ------------------------------------------------------------------ #
# Cached singleton – shared across all Streamlit pages
# ------------------------------------------------------------------ #

@st.cache_resource(show_spinner="Building recommendation model…")
def get_recommender() -> MovieRecommender:
    """
    Build and cache the MovieRecommender model for the entire session.

    Using @st.cache_resource means the model is built once and reused
    across all pages and user interactions without re-computing.

    Returns
    -------
    MovieRecommender (fitted)
    """
    from utils.data_loader import load_movies  # local import avoids circular refs

    movies_df = load_movies()
    recommender = MovieRecommender()
    recommender.build(movies_df)
    return recommender
