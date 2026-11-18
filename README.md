# 🎬 CineMatch – Machine Learning Movie Recommendation System

> **Academic Mini Project | Computer Science & Engineering | Machine Learning Subject**

---

## 📌 Project Introduction

**CineMatch** is a content-based movie recommendation system built with Python and Streamlit. It analyses the genre characteristics of movies using TF-IDF Vectorization and finds similar films using Cosine Similarity.

When a user selects a movie, CineMatch instantly returns the Top 5 or Top 10 most similar movies from the MovieLens dataset, displayed with their genres and similarity percentage.

---

## 🧩 Problem Statement

Streaming platforms serve thousands of movies, making it difficult for users to discover titles they will enjoy. A recommendation system solves this by automatically suggesting relevant content based on the characteristics of movies the user is already interested in.

---

## 🎯 Objectives

1. Build a functional content-based movie recommendation system.
2. Use TF-IDF to represent movie genres as numerical vectors.
3. Use Cosine Similarity to measure how alike two movies are.
4. Display recommendations through an attractive, Netflix-inspired web interface.
5. Demonstrate the system using the MovieLens Small Dataset.

---

## 📂 Dataset Information

**Source:** [GroupLens Research – MovieLens Latest Small](https://grouplens.org/datasets/movielens/latest/)

| File         | Records           | Columns                              |
|--------------|-------------------|--------------------------------------|
| movies.csv   | ~9,742 movies     | movieId, title, genres               |
| ratings.csv  | ~100,836 ratings  | userId, movieId, rating, timestamp   |

**Genres used** (18 categories):
Action, Adventure, Animation, Children, Comedy, Crime, Documentary, Drama, Fantasy, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western

---

## 🛠️ Technologies Used

| Category        | Technology                              |
|-----------------|-----------------------------------------|
| Language        | Python 3.x                              |
| Data Processing | Pandas, NumPy                           |
| Machine Learning| Scikit-learn (TfidfVectorizer, cosine_similarity) |
| Web UI          | Streamlit                               |
| Dataset         | MovieLens Small (GroupLens Research)    |
| Version Control | Git, GitHub                             |
| Editor          | VS Code                                 |

---

## 🧠 Machine Learning Algorithm

### Content-Based Filtering

This project uses **Content-Based Filtering** – recommendations are based on the features (genres) of the movies themselves, not user behaviour.

### Step 1 – TF-IDF Vectorization

Each movie's genre list (e.g., `"Action|Adventure|Sci-Fi"`) is converted to a space-separated string (`"Action Adventure SciFi"`) and fed into `TfidfVectorizer`.

TF-IDF assigns each genre a numerical weight:

```
TF(t, d) = count of genre t in movie d / total genres in movie d
IDF(t)   = log(N / number of movies with genre t) + 1
TF-IDF   = TF × IDF
```

The result is a sparse matrix of shape `(n_movies × n_genre_features)`.

### Step 2 – Cosine Similarity

The pairwise cosine similarity between all movie vectors is calculated:

```
cosine_similarity(A, B) = (A · B) / (‖A‖ × ‖B‖)
```

This produces an `n × n` similarity matrix where each cell represents how similar two movies are (0.0 to 1.0).

### Step 3 – Recommendation

```python
recommend_movies(movie_title, number_of_recommendations=10)
```

1. Find the row index of the selected movie in the matrix.
2. Retrieve its similarity scores with every other movie.
3. Sort scores in descending order.
4. Remove the query movie itself.
5. Return the top-N results with title, genres, and similarity percentage.

---

## 🏗️ System Architecture

```
USER selects a movie
       ↓
STREAMLIT UI  (app.py + pages/)
       ↓
DATA LOADER  (utils/data_loader.py)
       ↓
PREPROCESSOR  (utils/preprocessing.py)
       ↓
TF-IDF VECTORIZER  →  Genre feature matrix
       ↓
COSINE SIMILARITY  →  n × n similarity matrix
       ↓
RECOMMENDER  (models/recommender.py)
       ↓
TOP-N RESULTS displayed as movie cards
```

---

## 📁 Project Folder Structure

```
Movie_Recommendation_System/
│
├── app.py                      ← Home page (Streamlit entry point)
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
├── .gitignore
│
├── data/
│   ├── movies.csv              ← Movie titles + genres
│   ├── ratings.csv             ← User ratings
│   ├── download_data.py        ← Downloads the real MovieLens dataset
│   └── generate_sample_data.py ← Generates sample dataset as fallback
│
├── models/
│   └── recommender.py          ← TF-IDF + Cosine Similarity model
│
├── utils/
│   ├── data_loader.py          ← CSV loading + validation
│   └── preprocessing.py        ← Data cleaning + feature preparation
│
├── pages/
│   ├── 1_Recommend_Movies.py   ← Movie selection + recommendations
│   ├── 2_Explore_Movies.py     ← Browse, search, filter movies
│   └── 3_About_Project.py      ← Project explanation page
│
├── assets/
│   ├── placeholder.png         ← Default poster image
│   └── logo.png                ← App logo
│
└── tests/
    └── test_recommender.py     ← 29 unit tests
```

---

## ⚙️ Installation Instructions

### Prerequisites

- Python 3.9 or higher installed
- `pip` available
- Internet connection (optional – for real MovieLens dataset)

### Step 1 – Clone or Download the Project

```bash
git clone https://github.com/yourusername/Movie_Recommendation_System.git
cd Movie_Recommendation_System
```

Or download and extract the ZIP file.

### Step 2 – Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3 – Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 4 – Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5 – Get the Dataset

**Option A – Download the real MovieLens dataset (recommended):**
```bash
python data/download_data.py
```

**Option B – Generate a sample dataset (works offline):**
```bash
python data/generate_sample_data.py
```

The app will also auto-generate the sample dataset on first launch if no CSV files are found.

---

## ▶️ How to Run the Application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## ✅ Running the Tests

```bash
python -m pytest tests/test_recommender.py -v
```

or directly:

```bash
python tests/test_recommender.py
```

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| Movie Search | Searchable dropdown with all movie titles |
| Genre-Based Recommendations | TF-IDF + Cosine Similarity |
| Top 5 / Top 10 | Choose how many results to display |
| Similarity Score | Each recommendation shows a match percentage |
| Genre Filter | Filter movies by one or more genres |
| Movie Exploration | Browse all movies with search and pagination |
| Performance Metrics | Shows recommendation generation time |
| Caching | Model built once and cached for the session |
| Error Handling | Friendly messages for missing movies or data |
| Netflix-Inspired UI | Dark theme, red accents, modern card layout |

---

## 📸 Screenshots

> Run the application and take screenshots for your project report.

| Page | Description |
|------|-------------|
| Home | Hero section, stats, popular movies |
| Recommend Movies | Movie selector, genre tags, recommendation cards |
| Explore Movies | Browse all movies with genre filter |
| About Project | Algorithm explanations, architecture diagram |

---

## ⚠️ Limitations

- Recommendations are based solely on **genre similarity**. Movies with the same genre will always score identically against each other.
- No plot descriptions, cast information, or director data is used.
- No personalisation – every user gets the same recommendations for the same movie.
- The model does not learn from user feedback.

---

## 🚀 Future Enhancements

1. Add Collaborative Filtering using the ratings data.
2. Build a Hybrid model combining both approaches.
3. Integrate TMDB API for movie posters and plot summaries.
4. Use movie plot descriptions as additional TF-IDF features.
5. Add user authentication and personal watchlists.
6. Deploy on Streamlit Cloud or AWS.

---

## 📚 References

1. GroupLens Research. *MovieLens Datasets*. https://grouplens.org/datasets/movielens/
2. F. Maxwell Harper and Joseph A. Konstan. 2015. *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4).
3. Scikit-learn Documentation. *TfidfVectorizer*. https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
4. Scikit-learn Documentation. *Cosine Similarity*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
5. Streamlit Documentation. https://docs.streamlit.io/

---

## 👩‍💻 Author

**Computer Science & Engineering – ML Mini Project**

Built using Python, Streamlit, and Scikit-learn.

---

*CineMatch – Discover Movies You'll Love.*
