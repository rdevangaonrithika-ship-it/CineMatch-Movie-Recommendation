"""
pages/3_About_Project.py  –  About CineMatch
"""

import os, sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles       import inject_global_css, sidebar_nav, section_header
from utils.tmdb         import has_api_key

st.set_page_config(
    page_title="About – CineMatch",
    page_icon="📖", layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_css()
sidebar_nav("about")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

try:
    recommender = get_recommender()
    stats = recommender.get_model_stats()
except Exception:
    stats = {}

st.markdown('<div class="cm-page">', unsafe_allow_html=True)

st.markdown("""
<div style="padding:40px 0 28px;">
  <div style="font-size:11px;color:#7c3aed;font-weight:700;
              letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
    About the Platform
  </div>
  <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
             letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
    About CineMatch
  </h1>
  <p style="color:#8892a4;font-size:16px;max-width:640px;line-height:1.75;">
    CineMatch is a movie discovery platform that helps users find movies they might
    love based on their preferences. It uses Machine Learning and content-based
    filtering to identify movies with similar characteristics.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ── TMDB status ───────────────────────────────────────────────────────────────
api_color = "#10b981" if has_api_key() else "#e50914"
api_label = "Connected ✓" if has_api_key() else "Not configured"
api_note  = ("Real movie posters are loading from TMDB."
             if has_api_key() else
             "Add TMDB_API_KEY to .streamlit/secrets.toml for real posters.")

st.markdown(f"""
<div style="background:#12121a;border:1px solid #1e2a3a;border-radius:12px;
            padding:18px 24px;display:flex;align-items:center;gap:16px;
            margin-bottom:28px;">
  <div style="width:10px;height:10px;border-radius:50%;
              background:{api_color};flex-shrink:0;"></div>
  <div>
    <div style="font-size:14px;font-weight:700;color:#f1f1f1;">
      TMDB API — <span style="color:{api_color};">{api_label}</span>
    </div>
    <div style="font-size:12px;color:#8892a4;margin-top:2px;">{api_note}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
section_header("🧠 How It Works", "The machine learning behind recommendations")

col_a, col_b = st.columns([3,2])
with col_a:
    st.markdown("""
    <div class="about-block">
      <h3>Content-Based Filtering</h3>
      <p>CineMatch uses <strong style="color:#f1f1f1;">Content-Based Filtering</strong>
      — recommendations are based on the features of movies themselves, not user behaviour.
      Each movie is described by its genres. The system converts these into numerical
      vectors and measures similarity using cosine similarity.</p>
    </div>
    <div class="about-block">
      <h3>What is TF-IDF?</h3>
      <p><strong style="color:#f1f1f1;">TF-IDF</strong> (Term Frequency–Inverse Document
      Frequency) converts text into numbers. TF counts how often a genre appears in a
      movie's genre list. IDF reduces the weight of genres that appear in almost every movie
      (like Drama), making rarer genres (like Western) more distinctive.</p>
    </div>
    <div class="about-block">
      <h3>What is Cosine Similarity?</h3>
      <p>Cosine Similarity measures the angle between two TF-IDF vectors.
      If two movies share many genres, the angle is small and the score is close to 1.0.
      Completely different genres give a score near 0.0.
      The similarity matrix is computed once at startup for instant lookups.</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="about-block" style="text-align:center;">
      <h3 style="margin-bottom:20px;">Formulae</h3>
      <div style="font-size:11px;color:#8892a4;font-weight:600;letter-spacing:1px;
                  text-transform:uppercase;margin-bottom:6px;">TF-IDF Weight</div>
      <div class="formula-box">TF-IDF(t, d) = TF(t, d) × IDF(t)</div>
      <div class="formula-box" style="margin-top:8px;font-size:12px;">
        IDF(t) = log( N / df(t) ) + 1
      </div>
      <div style="font-size:11px;color:#8892a4;font-weight:600;letter-spacing:1px;
                  text-transform:uppercase;margin:20px 0 6px;">Cosine Similarity</div>
      <div class="formula-box">sim(A, B) = (A · B) / (‖A‖ × ‖B‖)</div>
    </div>
    """, unsafe_allow_html=True)

    if stats:
        st.markdown(f"""
        <div class="about-block">
          <h3>Live Model Stats</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px;">
            {"".join(
              f'<div style="background:#0a0a0f;border-radius:8px;padding:12px;'
              f'text-align:center;border:1px solid #1e2a3a;">'
              f'<div style="font-size:20px;font-weight:800;background:linear-gradient(135deg,#e50914,#7c3aed);'
              f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
              f'background-clip:text;">{num}</div>'
              f'<div style="font-size:11px;color:#8892a4;margin-top:4px;">{lbl}</div></div>'
              for num, lbl in [
                (stats.get("n_movies","—"), "Movies"),
                (stats.get("n_features","—"), "TF-IDF Features"),
                (f"{stats.get('build_time_sec','—')}s", "Build Time"),
                ("<1ms", "Query Time"),
              ]
            )}
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ── Dataset & Tech ────────────────────────────────────────────────────────────
section_header("📂 Dataset & Technology")

d1, d2 = st.columns(2)
with d1:
    st.markdown("""
    <div class="about-block">
      <h3>MovieLens Small Dataset</h3>
      <p>Dataset provided by
        <a href="https://grouplens.org/" target="_blank"
           style="color:#e50914;text-decoration:none;">GroupLens Research</a>
        at the University of Minnesota.
      </p>
      <table style="width:100%;border-collapse:collapse;margin-top:14px;
                    font-size:13px;color:#8892a4;">
        <tr style="border-bottom:1px solid #1e2a3a;">
          <th style="text-align:left;padding:7px 4px;color:#f1f1f1;">File</th>
          <th style="text-align:left;padding:7px 4px;color:#f1f1f1;">Records</th>
        </tr>
        <tr style="border-bottom:1px solid #1e2a3a;">
          <td style="padding:7px 4px;">movies.csv</td>
          <td style="padding:7px 4px;">~9,742 movies</td>
        </tr>
        <tr>
          <td style="padding:7px 4px;">ratings.csv</td>
          <td style="padding:7px 4px;">~100,836 ratings</td>
        </tr>
      </table>
      <p style="margin-top:12px;">
        Posters sourced from
        <a href="https://www.themoviedb.org/" target="_blank"
           style="color:#e50914;text-decoration:none;">TMDB (The Movie Database)</a>.
      </p>
    </div>
    """, unsafe_allow_html=True)

with d2:
    chips = "".join(
        f'<span class="tech-chip">{t}</span>'
        for t in ["Python 3.x","Streamlit","Pandas","NumPy",
                  "Scikit-learn","TfidfVectorizer","cosine_similarity",
                  "TMDB API","MovieLens","requests"]
    )
    st.markdown(f"""
    <div class="about-block">
      <h3>Technology Stack</h3>
      <div style="margin-top:8px;">{chips}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ── Architecture ──────────────────────────────────────────────────────────────
section_header("🏗️ System Architecture")
steps = [
    ("🧑","User"), ("→",None), ("🖥️","Streamlit UI"),
    ("→",None), ("📂","Data Loader"), ("→",None), ("🧹","Preprocessor"),
    ("→",None), ("📐","TF-IDF"), ("→",None), ("📏","Cosine Sim"),
    ("→",None), ("🎬","Top-N Results"),
]
arch_html = '<div class="about-block"><div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:0;">'
for icon, label in steps:
    if label is None:
        arch_html += '<div style="font-size:18px;color:#4a5568;padding:0 6px;align-self:center;">→</div>'
    else:
        arch_html += (
            f'<div style="background:#0a0a0f;border:1px solid #1e2a3a;border-radius:8px;'
            f'padding:12px 14px;text-align:center;min-width:72px;">'
            f'<div style="font-size:20px;">{icon}</div>'
            f'<div style="font-size:10px;color:#8892a4;margin-top:4px;font-weight:600;">{label}</div>'
            f'</div>'
        )
arch_html += '</div></div>'
st.markdown(arch_html, unsafe_allow_html=True)

st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ── Limitations & Roadmap ─────────────────────────────────────────────────────
section_header("⚠️ Limitations & Future Roadmap")
lc, rc = st.columns(2)
with lc:
    st.markdown("""
    <div class="about-block">
      <h3>Current Limitations</h3>
      <ul>
        <li>Genre-only recommendations — no plot, cast or director.</li>
        <li>Movies with identical genres always produce the same similarity scores.</li>
        <li>No personalisation based on individual viewing history.</li>
        <li>Watchlist is session-based — not persisted across browser sessions.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)
with rc:
    st.markdown("""
    <div class="about-block">
      <h3>Future Enhancements</h3>
      <ul>
        <li>Collaborative Filtering using the full ratings dataset.</li>
        <li>Hybrid model combining content and collaborative signals.</li>
        <li>TMDB plot summaries as additional TF-IDF features.</li>
        <li>User accounts and persistent watchlists.</li>
        <li>Deployment on Streamlit Community Cloud.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="cm-footer">
  CineMatch · Stream &amp; Discover Platform ·
  Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens</a>
  · Posters: <a href="https://www.themoviedb.org/" target="_blank">TMDB</a>
</div></div>""", unsafe_allow_html=True)
