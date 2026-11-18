"""
pages/3_About_Project.py
------------------------
Educational page explaining the project, algorithms, and dataset.
"""

import os
import sys

import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender

# ------------------------------------------------------------------ #
# Page config
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="About – CineMatch",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------ #
# CSS
# ------------------------------------------------------------------ #
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #141414; color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #333; }
    [data-testid="stSidebar"] * { color: #e5e5e5 !important; }
    #MainMenu, footer, header { visibility: hidden; }
    h1 { color: #E50914 !important; font-weight: 800; }
    h2 { color: #FFFFFF !important; font-weight: 700; }
    h3 { color: #E50914 !important; font-weight: 600; }
    p  { color: #c8c8c8; line-height: 1.8; font-size: 15px; }
    li { color: #c8c8c8; line-height: 1.8; font-size: 15px; }
    code {
        background: #2a2a2a; color: #E50914;
        padding: 2px 6px; border-radius: 4px; font-size: 13px;
    }
    .about-card {
        background: #1f1f1f;
        border-radius: 12px;
        padding: 28px 28px;
        margin-bottom: 20px;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #E50914;
    }
    .tech-pill {
        display: inline-block;
        background: #2a2a2a;
        color: #E50914;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
        border: 1px solid #3a3a3a;
    }
    .formula-box {
        background: #0d0d0d;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px 24px;
        font-family: 'Courier New', monospace;
        color: #E50914;
        font-size: 15px;
        margin: 16px 0;
        text-align: center;
    }
    .arch-box {
        background: #0d0d0d;
        border: 1px dashed #444;
        border-radius: 8px;
        padding: 20px 24px;
        font-family: 'Courier New', monospace;
        color: #b3b3b3;
        font-size: 13px;
        line-height: 2;
    }
    .arch-box span { color: #E50914; font-weight: 700; }
    .sidebar-logo { font-size: 28px; font-weight: 900; color: #E50914 !important; letter-spacing: -1px; margin-bottom: 4px; }
    .sidebar-tagline { font-size: 11px; color: #888 !important; letter-spacing: 1px; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Sidebar
# ------------------------------------------------------------------ #
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎬 CineMatch</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">MOVIE RECOMMENDATION SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                          label="🏠  Home")
    st.page_link("pages/1_Recommend_Movies.py",     label="🎯  Recommend Movies")
    st.page_link("pages/2_Explore_Movies.py",       label="🔍  Explore Movies")
    st.page_link("pages/3_About_Project.py",        label="📖  About Project")
    st.markdown("---")
    try:
        recommender = get_recommender()
        stats = recommender.get_model_stats()
        st.markdown(
            f'<div style="font-size:11px; color:#666; line-height:1.8;">'
            f'Movies: {stats["n_movies"]}<br>'
            f'Features: {stats["n_features"]}<br>'
            f'Build time: {stats["build_time_sec"]}s</div>',
            unsafe_allow_html=True,
        )
    except Exception:
        pass

# ------------------------------------------------------------------ #
# Page header
# ------------------------------------------------------------------ #
st.markdown("# 📖 About This Project")
st.markdown(
    '<p style="color:#b3b3b3; font-size:15px; margin-top:-10px;">Learn how CineMatch works — the algorithms, dataset, and technology behind it.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ------------------------------------------------------------------ #
# Section 1 – What is a Movie Recommendation System?
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>🎬 What is a Movie Recommendation System?</h3>
    <p>
        A <strong>Movie Recommendation System</strong> is a type of information filtering system
        that predicts which movies a user is likely to enjoy, based on certain criteria.
        These systems are widely used by streaming platforms such as Netflix, Amazon Prime, and Disney+
        to help users discover content relevant to their interests.
    </p>
    <p>
        There are three main types of recommendation systems:
    </p>
    <ul>
        <li><strong>Content-Based Filtering</strong> – Recommends items similar to what the user has
            already liked, based on item features (genres, descriptions, cast).</li>
        <li><strong>Collaborative Filtering</strong> – Recommends items based on the preferences of
            similar users.</li>
        <li><strong>Hybrid Filtering</strong> – Combines both approaches.</li>
    </ul>
    <p>
        <strong>CineMatch uses Content-Based Filtering exclusively</strong>, analysing movie genres
        to find similar films.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 2 – Content-Based Filtering
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>🧠 Content-Based Filtering</h3>
    <p>
        Content-Based Filtering analyses the <strong>attributes of items</strong> (in this case, movies)
        to find other items with similar characteristics.
    </p>
    <p>
        In CineMatch, the primary attribute used is <strong>genre</strong>.
        Each movie in the MovieLens dataset has one or more genres, such as:
    </p>
    <ul>
        <li>Action, Adventure, Animation, Comedy, Crime</li>
        <li>Drama, Fantasy, Horror, Musical, Mystery</li>
        <li>Romance, Sci-Fi, Thriller, War, Western</li>
    </ul>
    <p>
        The system converts these genre strings into numerical vectors and calculates how similar
        any two movies are based on their genre composition.
    </p>
    <p>
        <strong>Advantage:</strong> No user history is required. Any movie can receive recommendations
        based purely on its content.<br>
        <strong>Limitation:</strong> Recommendations are limited to genre similarity and do not account
        for plot, cast, director, or individual user preferences.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 3 – TF-IDF
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>📐 TF-IDF  (Term Frequency – Inverse Document Frequency)</h3>
    <p>
        <strong>TF-IDF</strong> is a numerical technique from information retrieval used to represent
        text as a vector of numbers. It measures how important a term (word) is within a document
        relative to a collection of documents.
    </p>
    <p>In CineMatch:</p>
    <ul>
        <li>Each <strong>movie</strong> is treated as a "document".</li>
        <li>Each <strong>genre</strong> (e.g., "Action", "Comedy") is a "term".</li>
        <li>The entire movie dataset is the "corpus".</li>
    </ul>
    <p><strong>TF (Term Frequency)</strong> measures how often a genre appears in a movie's genre list.</p>
    <p>
        <strong>IDF (Inverse Document Frequency)</strong> reduces the weight of genres that appear
        in almost every movie (e.g., "Drama"), and increases the weight of rarer genres
        (e.g., "Western", "Musical") that are more distinctive.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown(
        """
        <div class="formula-box">
            TF(t, d) = (count of t in d) / (total terms in d)
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_f2:
    st.markdown(
        """
        <div class="formula-box">
            IDF(t) = log( N / df(t) ) + 1
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="about-card" style="margin-top:0;">
    <p style="margin:0; font-size:13px; color:#888;">
        Where <code>t</code> = term (genre), <code>d</code> = document (movie), <code>N</code> = total movies,
        <code>df(t)</code> = number of movies containing genre <code>t</code>.
        The final TF-IDF score is TF × IDF. Scikit-learn's <code>TfidfVectorizer</code> handles
        this automatically and normalises each vector to unit length.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 4 – Cosine Similarity
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>📏 Cosine Similarity</h3>
    <p>
        <strong>Cosine Similarity</strong> measures the angle between two vectors in a
        multi-dimensional space. If two movies have very similar genre vectors, the angle between
        them is small, and the cosine similarity is close to <strong>1.0</strong> (100%).
        If the genres are completely different, the cosine similarity is close to <strong>0.0</strong>.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="formula-box" style="font-size:17px;">
        Cosine Similarity(A, B)  =  (A · B)  /  ( ‖A‖ × ‖B‖ )
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="about-card">
    <p>
        Where <code>A</code> and <code>B</code> are TF-IDF vectors of two movies,
        <code>A · B</code> is their dot product, and <code>‖A‖</code>, <code>‖B‖</code>
        are their magnitudes (Euclidean norms).
    </p>
    <p>
        In CineMatch, a full <strong>n × n cosine-similarity matrix</strong> is computed once
        at startup (where n = number of movies). When a user selects a movie, its row in the matrix
        is retrieved, sorted, and the top-N results are returned — this lookup takes milliseconds.
    </p>
    <ul>
        <li><strong>Score = 1.0</strong> → Identical genre composition</li>
        <li><strong>Score = 0.5–0.9</strong> → Strong genre overlap</li>
        <li><strong>Score = 0.1–0.4</strong> → Partial genre match</li>
        <li><strong>Score = 0.0</strong> → No common genres</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 5 – Dataset
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>📂 Dataset  –  MovieLens Small</h3>
    <p>
        CineMatch uses the <strong>MovieLens Small Dataset</strong> provided by
        <a href="https://grouplens.org/" target="_blank" style="color:#E50914;">GroupLens Research</a>
        at the University of Minnesota.
    </p>
    <table style="width:100%; border-collapse:collapse; color:#c8c8c8; font-size:14px; margin-top:10px;">
        <tr style="border-bottom:1px solid #333;">
            <th style="text-align:left; padding:8px; color:#E50914;">File</th>
            <th style="text-align:left; padding:8px; color:#E50914;">Records</th>
            <th style="text-align:left; padding:8px; color:#E50914;">Key Columns</th>
        </tr>
        <tr style="border-bottom:1px solid #2a2a2a;">
            <td style="padding:8px;">movies.csv</td>
            <td style="padding:8px;">~9,742 movies</td>
            <td style="padding:8px;">movieId, title, genres</td>
        </tr>
        <tr style="border-bottom:1px solid #2a2a2a;">
            <td style="padding:8px;">ratings.csv</td>
            <td style="padding:8px;">~100,836 ratings</td>
            <td style="padding:8px;">userId, movieId, rating, timestamp</td>
        </tr>
    </table>
    <p style="margin-top:14px;">
        Download from:
        <a href="https://grouplens.org/datasets/movielens/latest/" target="_blank" style="color:#E50914;">
        grouplens.org/datasets/movielens/latest/
        </a>
    </p>
    <p>
        <strong>Note:</strong> If the real dataset cannot be downloaded, CineMatch automatically
        generates a representative sample dataset with the same schema for demonstration purposes.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 6 – Technology Stack
# ------------------------------------------------------------------ #
st.markdown("### 🛠️ Technologies Used")

tech_items = [
    "Python 3.x", "Streamlit", "Pandas", "NumPy",
    "Scikit-learn", "TfidfVectorizer", "cosine_similarity",
    "MovieLens Dataset", "VS Code", "Git & GitHub",
]
tech_html = " ".join(f'<span class="tech-pill">{t}</span>' for t in tech_items)
st.markdown(f'<div style="margin-bottom:28px;">{tech_html}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ #
# Section 7 – System Architecture
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>🏗️ System Architecture</h3>
    <div class="arch-box">
        <span>USER</span> selects a movie in the Streamlit UI<br>
              ↓<br>
        <span>STREAMLIT APP</span>  (app.py + pages/)<br>
              ↓<br>
        <span>DATA LOADER</span>  (utils/data_loader.py)  →  loads movies.csv &amp; ratings.csv<br>
              ↓<br>
        <span>PREPROCESSOR</span>  (utils/preprocessing.py)  →  cleans data, prepares genre text<br>
              ↓<br>
        <span>TFIDF VECTORIZER</span>  →  converts genre strings to numerical vectors<br>
              ↓<br>
        <span>COSINE SIMILARITY</span>  →  computes n×n similarity matrix<br>
              ↓<br>
        <span>RECOMMENDER</span>  (models/recommender.py)  →  recommend_movies(title, N)<br>
              ↓<br>
        <span>TOP-N RESULTS</span>  displayed as movie cards with similarity %
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 8 – Project Files
# ------------------------------------------------------------------ #
st.markdown(
    """
    <div class="about-card">
    <h3>📁 Project File Structure</h3>
    <pre style="color:#b3b3b3; font-size:13px; background:#0d0d0d; padding:16px; border-radius:8px; overflow-x:auto;">
Movie_Recommendation_System/
│
├── <span style="color:#E50914;">app.py</span>                    ← Home page (Streamlit entry point)
├── requirements.txt           ← Python dependencies
├── README.md                  ← Full documentation
├── .gitignore
│
├── <span style="color:#E50914;">data/</span>
│   ├── movies.csv             ← MovieLens movie titles + genres
│   ├── ratings.csv            ← MovieLens user ratings
│   ├── download_data.py       ← Downloads the real dataset
│   └── generate_sample_data.py← Generates fallback sample data
│
├── <span style="color:#E50914;">models/</span>
│   └── recommender.py         ← TF-IDF + Cosine Similarity model
│
├── <span style="color:#E50914;">utils/</span>
│   ├── data_loader.py         ← Loads and validates CSV files
│   └── preprocessing.py       ← Cleans data, prepares features
│
├── <span style="color:#E50914;">pages/</span>
│   ├── 1_Recommend_Movies.py  ← Recommendation UI page
│   ├── 2_Explore_Movies.py    ← Browse & filter movies page
│   └── 3_About_Project.py     ← This page
│
├── assets/
│   ├── placeholder.png        ← Default poster image
│   └── logo.png               ← App logo
│
└── tests/
    └── test_recommender.py    ← Unit tests
    </pre>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Section 9 – Limitations & Future Work
# ------------------------------------------------------------------ #
col_lim, col_fut = st.columns(2)

with col_lim:
    st.markdown(
        """
        <div class="about-card">
        <h3>⚠️ Limitations</h3>
        <ul>
            <li>Recommendations rely only on genre — no plot, cast, or director data.</li>
            <li>Movies with the same genres always have identical similarity scores among themselves.</li>
            <li>No personalisation based on user viewing history.</li>
            <li>The model does not learn or improve over time.</li>
            <li>Genre labels are coarse (e.g., "Drama" covers thousands of very different films).</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_fut:
    st.markdown(
        """
        <div class="about-card">
        <h3>🚀 Future Enhancements</h3>
        <ul>
            <li>Add Collaborative Filtering using user ratings for personalised suggestions.</li>
            <li>Integrate TMDB API for posters, overviews, and cast details.</li>
            <li>Use movie descriptions and tags as additional TF-IDF features.</li>
            <li>Implement a Hybrid model combining content and collaborative signals.</li>
            <li>Add user login and preference tracking.</li>
            <li>Deploy on Streamlit Cloud or a cloud platform.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ #
# Footer
# ------------------------------------------------------------------ #
st.markdown(
    """
    <hr style="border-color:#2a2a2a; margin-top:40px;">
    <div style="text-align:center; color:#666; font-size:12px; padding:16px 0 32px;">
        CineMatch · ML Mini Project · Computer Science &amp; Engineering<br>
        Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank" style="color:#E50914;">MovieLens</a>
        by GroupLens Research, University of Minnesota
    </div>
    """,
    unsafe_allow_html=True,
)
