"""
tests/test_recommender.py
--------------------------
Unit tests for the CineMatch recommendation system.

Tests cover:
  1.  Dataset loads successfully.
  2.  Movie titles are present and non-empty.
  3.  TF-IDF matrix is generated with correct shape.
  4.  Cosine similarity matrix has correct dimensions.
  5.  Recommendations are returned for a valid movie.
  6.  The selected movie is NOT included in its own recommendations.
  7.  Top-5 returns exactly 5 results (when enough movies exist).
  8.  Top-10 returns exactly 10 results (when enough movies exist).
  9.  An invalid movie title produces a friendly error (not a crash).
  10. Missing genres are handled without raising an exception.

Run with:
    python -m pytest tests/test_recommender.py -v
or:
    python tests/test_recommender.py
"""

import os
import sys
import unittest

# ------------------------------------------------------------------ #
# Make project root importable
# ------------------------------------------------------------------ #
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ------------------------------------------------------------------ #
# Bootstrap data before importing anything else
# ------------------------------------------------------------------ #
def _ensure_data():
    data_dir = os.path.join(ROOT, "data")
    movies_p = os.path.join(data_dir, "movies.csv")
    ratings_p = os.path.join(data_dir, "ratings.csv")
    if not (os.path.exists(movies_p) and os.path.exists(ratings_p)):
        import subprocess
        gen = os.path.join(data_dir, "generate_sample_data.py")
        if os.path.exists(gen):
            subprocess.run([sys.executable, gen], timeout=30, check=False)

_ensure_data()

import pandas as pd
from utils.data_loader import load_movies, load_ratings
from utils.preprocessing import clean_movies, prepare_genre_features, get_genre_list
from models.recommender import MovieRecommender


# ------------------------------------------------------------------ #
# Shared fixture – build one recommender for all tests
# ------------------------------------------------------------------ #
class _RecommenderFixture(unittest.TestCase):
    """Base class: builds the recommender once and shares it."""

    @classmethod
    def setUpClass(cls):
        """Load data and build the model once before any tests run."""
        # We bypass the Streamlit cache decorator for plain unit testing
        import pandas as pd
        movies_path = os.path.join(ROOT, "data", "movies.csv")
        cls.movies_df_raw = pd.read_csv(movies_path)

        cls.recommender = MovieRecommender()
        cls.recommender.build(cls.movies_df_raw)

        ratings_path = os.path.join(ROOT, "data", "ratings.csv")
        cls.ratings_df = pd.read_csv(ratings_path)


# ------------------------------------------------------------------ #
# Test classes
# ------------------------------------------------------------------ #

class TestDataLoading(_RecommenderFixture):
    """Tests 1 & 2 – Dataset loading."""

    def test_01_movies_loads_successfully(self):
        """movies.csv loads and returns a non-empty DataFrame."""
        self.assertIsInstance(self.movies_df_raw, pd.DataFrame)
        self.assertGreater(len(self.movies_df_raw), 0, "movies.csv is empty")

    def test_02_ratings_loads_successfully(self):
        """ratings.csv loads and returns a non-empty DataFrame."""
        self.assertIsInstance(self.ratings_df, pd.DataFrame)
        self.assertGreater(len(self.ratings_df), 0, "ratings.csv is empty")

    def test_03_movie_titles_present(self):
        """Every row in movies.csv has a non-empty title."""
        self.assertIn("title", self.movies_df_raw.columns)
        empty_titles = self.movies_df_raw["title"].isna().sum()
        self.assertEqual(empty_titles, 0, "Some movies have missing titles")

    def test_04_movies_has_required_columns(self):
        """movies.csv has all three required columns."""
        for col in ["movieId", "title", "genres"]:
            self.assertIn(col, self.movies_df_raw.columns, f"Missing column: {col}")

    def test_05_ratings_has_required_columns(self):
        """ratings.csv has all four required columns."""
        for col in ["userId", "movieId", "rating", "timestamp"]:
            self.assertIn(col, self.ratings_df.columns, f"Missing column: {col}")


class TestPreprocessing(_RecommenderFixture):
    """Tests for data cleaning and feature preparation."""

    def test_06_clean_movies_removes_duplicates(self):
        """clean_movies should not produce duplicate rows."""
        cleaned = clean_movies(self.movies_df_raw)
        dup_count = cleaned.duplicated().sum()
        self.assertEqual(dup_count, 0, "Duplicate rows remain after cleaning")

    def test_07_clean_movies_handles_missing_genres(self):
        """Movies with no genres should not cause NaN in the genres column."""
        cleaned = clean_movies(self.movies_df_raw)
        na_genres = cleaned["genres"].isna().sum()
        self.assertEqual(na_genres, 0, "NaN values remain in genres column")

    def test_08_genre_features_column_created(self):
        """prepare_genre_features adds the 'genre_features' column."""
        cleaned = clean_movies(self.movies_df_raw)
        featured = prepare_genre_features(cleaned)
        self.assertIn("genre_features", featured.columns)

    def test_09_genre_features_no_pipes(self):
        """genre_features column should not contain pipe characters."""
        cleaned = clean_movies(self.movies_df_raw)
        featured = prepare_genre_features(cleaned)
        has_pipe = featured["genre_features"].str.contains("|", regex=False).any()
        self.assertFalse(has_pipe, "genre_features still contains '|' characters")

    def test_10_genre_list_non_empty(self):
        """get_genre_list should return a non-empty sorted list."""
        cleaned = clean_movies(self.movies_df_raw)
        genres = get_genre_list(cleaned)
        self.assertIsInstance(genres, list)
        self.assertGreater(len(genres), 0, "No genres extracted")
        self.assertEqual(genres, sorted(genres), "Genre list is not sorted")


class TestTFIDF(_RecommenderFixture):
    """Test 3 – TF-IDF matrix."""

    def test_11_tfidf_matrix_generated(self):
        """TF-IDF matrix should exist after build()."""
        self.assertIsNotNone(self.recommender.tfidf_matrix)

    def test_12_tfidf_matrix_correct_rows(self):
        """TF-IDF matrix should have one row per cleaned movie."""
        n_movies = self.recommender.n_movies
        self.assertEqual(
            self.recommender.tfidf_matrix.shape[0],
            n_movies,
            "TF-IDF matrix row count does not match number of movies",
        )

    def test_13_tfidf_matrix_has_features(self):
        """TF-IDF matrix should have at least 1 genre feature column."""
        self.assertGreater(
            self.recommender.tfidf_matrix.shape[1], 0,
            "TF-IDF matrix has no feature columns",
        )

    def test_14_n_features_matches_matrix(self):
        """n_features attribute should match the actual matrix width."""
        self.assertEqual(
            self.recommender.n_features,
            self.recommender.tfidf_matrix.shape[1],
        )


class TestCosineSimilarity(_RecommenderFixture):
    """Test 4 – Cosine similarity matrix."""

    def test_15_cosine_sim_matrix_exists(self):
        """cosine_sim matrix should exist after build()."""
        self.assertIsNotNone(self.recommender.cosine_sim)

    def test_16_cosine_sim_is_square(self):
        """cosine_sim should be a square matrix (n × n)."""
        n = self.recommender.n_movies
        self.assertEqual(self.recommender.cosine_sim.shape, (n, n))

    def test_17_diagonal_is_one(self):
        """Every movie should have cosine similarity of 1.0 with itself."""
        import numpy as np
        diag = self.recommender.cosine_sim.diagonal()
        self.assertTrue(
            np.allclose(diag, 1.0),
            "Diagonal of cosine_sim matrix is not all 1.0",
        )

    def test_18_values_between_zero_and_one(self):
        """All cosine similarity scores should be in [0.0, 1.0]."""
        import numpy as np
        self.assertTrue(
            (self.recommender.cosine_sim >= -1e-6).all(),
            "Some cosine similarity values are negative",
        )
        self.assertTrue(
            (self.recommender.cosine_sim <= 1.0 + 1e-6).all(),
            "Some cosine similarity values exceed 1.0",
        )


class TestRecommendations(_RecommenderFixture):
    """Tests 5–9 – Recommendation function."""

    def _get_first_valid_title(self):
        """Return the first movie title from the model."""
        titles = self.recommender.get_all_titles()
        self.assertGreater(len(titles), 0, "No titles in model")
        return titles[0]

    def test_19_recommendations_returned_for_valid_movie(self):
        """recommend_movies() returns success=True for a valid title."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 5)
        self.assertTrue(result["success"], f"Failed for '{title}': {result.get('error_message')}")
        self.assertIn("recommendations", result)

    def test_20_selected_movie_not_in_recommendations(self):
        """The query movie itself must not appear in its own recommendations."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 10)
        self.assertTrue(result["success"])
        rec_titles = [r["title"].lower() for r in result["recommendations"]]
        self.assertNotIn(title.lower(), rec_titles, "Query movie appears in its own recommendations")

    def test_21_top5_returns_five_results(self):
        """Top-5 recommendation returns at most 5 results."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 5)
        self.assertTrue(result["success"])
        # Should return exactly 5 if enough movies exist, up to n_movies - 1
        expected = min(5, self.recommender.n_movies - 1)
        self.assertEqual(len(result["recommendations"]), expected)

    def test_22_top10_returns_ten_results(self):
        """Top-10 recommendation returns at most 10 results."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 10)
        self.assertTrue(result["success"])
        expected = min(10, self.recommender.n_movies - 1)
        self.assertEqual(len(result["recommendations"]), expected)

    def test_23_invalid_title_returns_error_not_crash(self):
        """An unknown movie title should return success=False, not raise an exception."""
        result = self.recommender.recommend_movies("XYZZY_NONEXISTENT_MOVIE_TITLE_12345", 5)
        self.assertFalse(result["success"])
        self.assertIn("error_message", result)
        self.assertIsNotNone(result["error_message"])

    def test_24_similarity_scores_are_floats_between_0_and_1(self):
        """All returned similarity scores must be valid floats in [0, 1]."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 10)
        self.assertTrue(result["success"])
        for rec in result["recommendations"]:
            score = rec["similarity_score"]
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0, f"Negative score: {score}")
            self.assertLessEqual(score, 1.0 + 1e-6, f"Score > 1.0: {score}")

    def test_25_recommendations_sorted_descending(self):
        """Recommendations must be sorted by similarity score in descending order."""
        title  = self._get_first_valid_title()
        result = self.recommender.recommend_movies(title, 10)
        self.assertTrue(result["success"])
        scores = [r["similarity_score"] for r in result["recommendations"]]
        self.assertEqual(
            scores, sorted(scores, reverse=True),
            "Recommendations are not sorted by descending similarity",
        )

    def test_26_all_titles_returns_list(self):
        """get_all_titles() must return a non-empty list of strings."""
        titles = self.recommender.get_all_titles()
        self.assertIsInstance(titles, list)
        self.assertGreater(len(titles), 0)
        for t in titles[:5]:
            self.assertIsInstance(t, str)

    def test_27_get_movie_info_valid_title(self):
        """get_movie_info() should return a dict for a known title."""
        title = self._get_first_valid_title()
        info  = self.recommender.get_movie_info(title)
        self.assertIsNotNone(info)
        self.assertIn("title",   info)
        self.assertIn("genres",  info)
        self.assertIn("movieId", info)

    def test_28_get_movie_info_invalid_title(self):
        """get_movie_info() should return None for an unknown title."""
        info = self.recommender.get_movie_info("NONEXISTENT_MOVIE_XYZ")
        self.assertIsNone(info)

    def test_29_model_stats_dict(self):
        """get_model_stats() should return a dict with expected keys."""
        stats = self.recommender.get_model_stats()
        for key in ["n_movies", "n_features", "build_time_sec"]:
            self.assertIn(key, stats)
        self.assertGreater(stats["n_movies"], 0)
        self.assertGreater(stats["n_features"], 0)
        self.assertGreater(stats["build_time_sec"], 0)


# ------------------------------------------------------------------ #
# Run directly
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()
    for test_class in [
        TestDataLoading,
        TestPreprocessing,
        TestTFIDF,
        TestCosineSimilarity,
        TestRecommendations,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
