"""
pages/3_About_Project.py
------------------------
About CineMatch — clean product-style page.
"""

import os
import sys

import streamlit as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.recommender import get_recommender
from utils.styles import inject_global_css, sidebar_nav, section_header

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "About – CineMatch",
    page_icon  = "📖",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)
inject_global_css()
sidebar_nav("about")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# ── Model stats (sidebar only) ────────────────────────────────────────────────
try:
    recommender = get_recommender()
    stats = recommender.get_model_stats()
except Exception:
    stats = {}

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="cm-page">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="padding:40px 0 32px;">
      <div style="font-size:11px;color:#7c3aed;font-weight:700;
                  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
        About the Platform
      </div>
      <h1 style="font-size:2.4rem;font-weight:900;color:#f1f1f1;
                 letter-spacing:-1px;line-height:1.1;margin-bottom:14px;">
        About CineMatch
      </h1>
      <p style="color:#8892a4;font-size:16px;max-width:640px;line-height:1.75;">
        CineMatch is a movie discovery platform that helps users find movies they
        might love based on their preferences. It uses Machine Learning and
        content-based filtering to identify movies with similar characteristics.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — What is Content-Based Filtering?
# ═════════════════════════════════════════════════════════════════════════════
section_header("🧠 How It Works", "The machine learning behind recommendations")

col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown(
        """
        <div class="about-block">
          <h3>Content-Based Filtering</h3>
          <p>
            CineMatch uses <strong style="color:#f1f1f1;">Content-Based Filtering</strong> —
            a technique that recommends items by analysing their attributes rather than
            relying on what other users have watched.
          </p>
          <p style="margin-top:12px;">
            Each movie is described by its genres (e.g. Action, Drama, Sci-Fi).
            The system converts these genre labels into numerical vectors and measures
            how similar any two movies are using cosine similarity.
          </p>
          <p style="margin-top:12px;">
            When you pick a movie, CineMatch finds the other movies whose genre
            vectors are closest to it and returns them as recommendations.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-block">
          <h3>What is TF-IDF?</h3>
          <p>
            <strong style="color:#f1f1f1;">TF-IDF</strong> (Term Frequency–Inverse
            Document Frequency) converts text into numbers.
          </p>
          <ul style="margin-top:10px;">
            <li><strong style="color:#f1f1f1;">TF</strong> — how often a genre
              appears in a movie's genre list.</li>
            <li><strong style="color:#f1f1f1;">IDF</strong> — reduces the weight
              of genres that appear in almost every movie (like "Drama"), making
              rarer genres (like "Western") more distinctive.</li>
          </ul>
          <p style="margin-top:12px;">
            The result is a sparse numerical matrix — one row per movie,
            one column per unique genre — that feeds into the similarity calculation.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    # TF formula
    st.markdown(
        """
        <div class="about-block" style="text-align:center;">
          <h3 style="margin-bottom:20px;">Formulae</h3>
          <div style="font-size:11px;color:#8892a4;font-weight:600;
                      letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">
            TF-IDF Weight
          </div>
          <div class="formula-box">
            TF-IDF(t, d) = TF(t, d) × IDF(t)
          </div>
          <div class="formula-box" style="margin-top:8px;font-size:12px;">
            IDF(t) = log( N / df(t) ) + 1
          </div>
          <div style="font-size:11px;color:#8892a4;font-weight:600;
                      letter-spacing:1px;text-transform:uppercase;
                      margin:20px 0 6px;">
            Cosine Similarity
          </div>
          <div class="formula-box">
            sim(A, B) = (A · B) / (‖A‖ × ‖B‖)
          </div>
          <p style="font-size:12px;color:#4a5568;margin-top:12px;line-height:1.6;">
            Where A and B are TF-IDF genre vectors.
            Score ranges from 0.0 (no overlap) to 1.0 (identical genres).
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Score legend
    st.markdown(
        """
        <div class="about-block">
          <h3>Similarity Score Guide</h3>
          <div style="display:flex;flex-direction:column;gap:10px;margin-top:4px;">
        """,
        unsafe_allow_html=True,
    )
    for label, pct, color in [
        ("Identical genre composition", 100, "#10b981"),
        ("Strong genre overlap",         75, "#7c3aed"),
        ("Partial genre match",          45, "#e59914"),
        ("Minimal genre match",          15, "#e50914"),
    ]:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:50px;text-align:right;font-size:12px;
                          font-weight:700;color:#f1f1f1;">{pct}%</div>
              <div style="flex:1;background:#1e2a3a;border-radius:4px;height:6px;">
                <div style="width:{pct}%;height:6px;border-radius:4px;
                            background:{color};"></div>
              </div>
              <div style="font-size:11px;color:#8892a4;min-width:160px;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div></div>", unsafe_allow_html=True)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Dataset & Tech Stack
# ═════════════════════════════════════════════════════════════════════════════
section_header("📂 Dataset & Technology", "What powers CineMatch")

d1, d2 = st.columns(2)

with d1:
    st.markdown(
        """
        <div class="about-block">
          <h3>MovieLens Small Dataset</h3>
          <p>
            CineMatch uses the
            <strong style="color:#f1f1f1;">MovieLens Small Dataset</strong>
            provided by
            <a href="https://grouplens.org/" target="_blank"
               style="color:#e50914;text-decoration:none;">GroupLens Research</a>
            at the University of Minnesota.
          </p>
          <table style="width:100%;border-collapse:collapse;margin-top:16px;
                        font-size:13px;color:#8892a4;">
            <tr style="border-bottom:1px solid #1e2a3a;">
              <th style="text-align:left;padding:8px 4px;color:#f1f1f1;">File</th>
              <th style="text-align:left;padding:8px 4px;color:#f1f1f1;">Records</th>
              <th style="text-align:left;padding:8px 4px;color:#f1f1f1;">Key Columns</th>
            </tr>
            <tr style="border-bottom:1px solid #1e2a3a;">
              <td style="padding:8px 4px;">movies.csv</td>
              <td style="padding:8px 4px;">~9,742</td>
              <td style="padding:8px 4px;">movieId, title, genres</td>
            </tr>
            <tr>
              <td style="padding:8px 4px;">ratings.csv</td>
              <td style="padding:8px 4px;">~100,836</td>
              <td style="padding:8px 4px;">userId, movieId, rating</td>
            </tr>
          </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

with d2:
    tech_items = [
        "Python 3.x", "Streamlit 1.67",
        "Pandas", "NumPy",
        "Scikit-learn", "TfidfVectorizer",
        "cosine_similarity", "MovieLens Dataset",
    ]
    chips = "".join(f'<span class="tech-chip">{t}</span>' for t in tech_items)
    st.markdown(
        f"""
        <div class="about-block">
          <h3>Technology Stack</h3>
          <div style="margin-top:8px;">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Model live stats
    if stats:
        st.markdown(
            f"""
            <div class="about-block" style="margin-top:0;">
              <h3>Live Model Statistics</h3>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;
                          margin-top:8px;">
                <div style="background:#0a0a0f;border-radius:8px;padding:14px;
                            text-align:center;border:1px solid #1e2a3a;">
                  <div style="font-size:22px;font-weight:800;
                              background:linear-gradient(135deg,#e50914,#7c3aed);
                              -webkit-background-clip:text;
                              -webkit-text-fill-color:transparent;
                              background-clip:text;">
                    {stats.get('n_movies', '—')}
                  </div>
                  <div style="font-size:11px;color:#8892a4;margin-top:4px;">
                    Movies Indexed
                  </div>
                </div>
                <div style="background:#0a0a0f;border-radius:8px;padding:14px;
                            text-align:center;border:1px solid #1e2a3a;">
                  <div style="font-size:22px;font-weight:800;
                              background:linear-gradient(135deg,#e50914,#7c3aed);
                              -webkit-background-clip:text;
                              -webkit-text-fill-color:transparent;
                              background-clip:text;">
                    {stats.get('n_features', '—')}
                  </div>
                  <div style="font-size:11px;color:#8892a4;margin-top:4px;">
                    TF-IDF Features
                  </div>
                </div>
                <div style="background:#0a0a0f;border-radius:8px;padding:14px;
                            text-align:center;border:1px solid #1e2a3a;">
                  <div style="font-size:22px;font-weight:800;
                              background:linear-gradient(135deg,#e50914,#7c3aed);
                              -webkit-background-clip:text;
                              -webkit-text-fill-color:transparent;
                              background-clip:text;">
                    {stats.get('build_time_sec', '—')}s
                  </div>
                  <div style="font-size:11px;color:#8892a4;margin-top:4px;">
                    Model Build Time
                  </div>
                </div>
                <div style="background:#0a0a0f;border-radius:8px;padding:14px;
                            text-align:center;border:1px solid #1e2a3a;">
                  <div style="font-size:22px;font-weight:800;
                              background:linear-gradient(135deg,#e50914,#7c3aed);
                              -webkit-background-clip:text;
                              -webkit-text-fill-color:transparent;
                              background-clip:text;">
                    &lt;1ms
                  </div>
                  <div style="font-size:11px;color:#8892a4;margin-top:4px;">
                    Query Time
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Architecture
# ═════════════════════════════════════════════════════════════════════════════
section_header("🏗️ System Architecture")

st.markdown(
    """
    <div class="about-block">
      <div style="display:flex;flex-wrap:wrap;align-items:center;
                  justify-content:center;gap:0;margin:8px 0;">
    """,
    unsafe_allow_html=True,
)

arch_steps = [
    ("🧑", "User"),
    ("→", None),
    ("🖥️", "Streamlit UI"),
    ("→", None),
    ("📂", "Data Loader"),
    ("→", None),
    ("🧹", "Preprocessor"),
    ("→", None),
    ("📐", "TF-IDF"),
    ("→", None),
    ("📏", "Cosine Sim"),
    ("→", None),
    ("🎬", "Top-N Results"),
]
for icon, label in arch_steps:
    if label is None:
        st.markdown(
            '<div style="font-size:20px;color:#4a5568;padding:0 8px;'
            'align-self:center;">→</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="background:#0a0a0f;border:1px solid #1e2a3a;border-radius:10px;
                        padding:14px 16px;text-align:center;min-width:80px;">
              <div style="font-size:22px;">{icon}</div>
              <div style="font-size:11px;color:#8892a4;margin-top:6px;
                          font-weight:600;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown('<hr class="cm-divider">', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Limitations & Roadmap
# ═════════════════════════════════════════════════════════════════════════════
section_header("⚠️ Limitations & Future Roadmap")

lim_col, road_col = st.columns(2)

with lim_col:
    st.markdown(
        """
        <div class="about-block">
          <h3>Current Limitations</h3>
          <ul>
            <li>Recommendations based on genre only — no plot, cast or director.</li>
            <li>Movies with identical genre sets always produce the same similarity scores.</li>
            <li>No personalisation based on individual user history.</li>
            <li>The model is static — it does not learn from new user interactions.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with road_col:
    st.markdown(
        """
        <div class="about-block">
          <h3>Future Enhancements</h3>
          <ul>
            <li>Collaborative Filtering using the full ratings dataset.</li>
            <li>TMDB API integration for posters and plot summaries.</li>
            <li>Hybrid model combining content and collaborative signals.</li>
            <li>User accounts and personalised watchlists with persistence.</li>
            <li>Deployment on Streamlit Community Cloud.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="cm-footer">
      CineMatch &nbsp;·&nbsp; ML Mini Project &nbsp;·&nbsp;
      Dataset: <a href="https://grouplens.org/datasets/movielens/" target="_blank">
      MovieLens</a> by GroupLens Research
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
