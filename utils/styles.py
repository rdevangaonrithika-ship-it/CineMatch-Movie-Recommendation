"""
utils/styles.py
---------------
Shared CSS theme for CineMatch.
Import and call inject_global_css() at the top of every page.
"""

import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Colour tokens  (reference inside CSS as literals)
# ─────────────────────────────────────────────────────────────────────────────
# BG_DEEP      = #0a0a0f
# BG_CARD      = #12121a
# BG_SURFACE   = #1a1a2e
# BG_ELEVATED  = #16213e
# ACCENT_RED   = #e50914
# ACCENT_PURPLE= #7c3aed
# ACCENT_GRAD  = linear-gradient(135deg,#e50914,#7c3aed)
# TEXT_PRIMARY = #f1f1f1
# TEXT_MUTED   = #8892a4
# TEXT_DIM     = #4a5568
# BORDER       = #1e2a3a
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════
   RESET & ROOT
═══════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: #0a0a0f !important;
    color: #f1f1f1 !important;
    font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
}

/* Remove default Streamlit padding */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════════════════════════════════════════════
   HIDE DEFAULT STREAMLIT CHROME
═══════════════════════════════════════════════════════════════════ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ═══════════════════════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a0a0f 100%) !important;
    border-right: 1px solid #1e2a3a !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 24px 16px !important;
}
[data-testid="stSidebar"] * { color: #c8d0dc !important; }
[data-testid="stSidebar"] a { text-decoration: none !important; }

/* Sidebar page-link active/hover */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin: 2px 0 !important;
    transition: background 0.2s, color 0.2s !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: rgba(229,9,20,0.12) !important;
    color: #e50914 !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"].active {
    background: rgba(229,9,20,0.18) !important;
    color: #e50914 !important;
    border-left: 3px solid #e50914 !important;
}

/* ═══════════════════════════════════════════════════════════════════
   TYPOGRAPHY
═══════════════════════════════════════════════════════════════════ */
h1,h2,h3,h4,h5,h6 { font-family: 'Inter', sans-serif !important; }
h1 { font-size: 2.4rem !important; font-weight: 800 !important; letter-spacing: -1px; line-height: 1.15; }
h2 { font-size: 1.7rem !important; font-weight: 700 !important; }
h3 { font-size: 1.25rem !important; font-weight: 600 !important; }
p  { color: #8892a4 !important; line-height: 1.75 !important; }

/* ═══════════════════════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #e50914, #c40812) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 11px 28px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(229,9,20,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(229,9,20,0.5) !important;
    background: linear-gradient(135deg, #f40612, #e50914) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary ghost button */
.btn-ghost > button {
    background: transparent !important;
    color: #f1f1f1 !important;
    border: 1px solid #2d3748 !important;
    box-shadow: none !important;
}
.btn-ghost > button:hover {
    border-color: #e50914 !important;
    color: #e50914 !important;
    box-shadow: none !important;
    transform: translateY(-1px) !important;
}

/* Purple accent button */
.btn-purple > button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
}
.btn-purple > button:hover {
    box-shadow: 0 8px 25px rgba(124,58,237,0.5) !important;
}

/* ═══════════════════════════════════════════════════════════════════
   FORM INPUTS
═══════════════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stMultiSelect > div > div {
    background-color: #12121a !important;
    color: #f1f1f1 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.15) !important;
}
.stTextInput label, .stSelectbox label, .stMultiSelect label {
    color: #8892a4 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════════════════════════════════════════════
   MOVIE CARDS  (shared across all pages)
═══════════════════════════════════════════════════════════════════ */
.cm-card {
    background: #12121a;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e2a3a;
    transition: transform 0.3s cubic-bezier(.25,.8,.25,1),
                box-shadow 0.3s ease,
                border-color 0.3s ease;
    position: relative;
    cursor: pointer;
}
.cm-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 30px rgba(229,9,20,0.15);
    border-color: rgba(229,9,20,0.4);
    z-index: 10;
}
.cm-card-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a2e 0%, #12121a 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}
.cm-card-poster img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}
.cm-card:hover .cm-card-poster img { transform: scale(1.06); }
.cm-card-poster-placeholder {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a2e 0%, #0d0d1a 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
.cm-card-poster-placeholder .film-icon {
    font-size: 48px;
    opacity: 0.3;
}
.cm-card-poster-placeholder .film-title-preview {
    font-size: 11px;
    color: #4a5568;
    text-align: center;
    padding: 0 12px;
    font-weight: 500;
}
.cm-card-body {
    padding: 14px 14px 16px;
}
.cm-card-title {
    color: #f1f1f1;
    font-size: 13.5px;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.cm-card-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}
.cm-card-year {
    color: #8892a4;
    font-size: 11px;
    font-weight: 500;
}
.cm-card-rating {
    display: flex;
    align-items: center;
    gap: 3px;
    color: #fbbf24;
    font-size: 11px;
    font-weight: 700;
}
.cm-card-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 4px;
}
.cm-genre-pill {
    background: rgba(124,58,237,0.15);
    color: #a78bfa;
    border: 1px solid rgba(124,58,237,0.25);
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    white-space: nowrap;
}
.cm-card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top,
        rgba(0,0,0,0.92) 0%,
        rgba(0,0,0,0.5) 50%,
        transparent 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 16px;
    gap: 8px;
}
.cm-card:hover .cm-card-overlay { opacity: 1; }
.cm-overlay-btn {
    display: block;
    text-align: center;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}
.cm-overlay-btn-primary {
    background: #e50914;
    color: #fff;
}
.cm-overlay-btn-primary:hover { background: #f40612; }
.cm-overlay-btn-secondary {
    background: rgba(255,255,255,0.1);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(4px);
}
.cm-overlay-btn-secondary:hover { background: rgba(255,255,255,0.2); }

/* ═══════════════════════════════════════════════════════════════════
   SIMILARITY BADGE (recommendation page)
═══════════════════════════════════════════════════════════════════ */
.sim-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: linear-gradient(135deg, #e50914, #7c3aed);
    color: #fff;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* ═══════════════════════════════════════════════════════════════════
   SECTION HEADERS
═══════════════════════════════════════════════════════════════════ */
.section-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}
.section-label-line {
    width: 4px;
    height: 22px;
    background: linear-gradient(180deg, #e50914, #7c3aed);
    border-radius: 4px;
    flex-shrink: 0;
}
.section-label-text {
    font-size: 20px;
    font-weight: 800;
    color: #f1f1f1;
    letter-spacing: -0.3px;
}
.section-label-sub {
    font-size: 13px;
    color: #8892a4;
    margin-top: 2px;
}

/* ═══════════════════════════════════════════════════════════════════
   STAT / INFO CARDS
═══════════════════════════════════════════════════════════════════ */
.cm-stat-card {
    background: #12121a;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 20px 18px;
    text-align: center;
    transition: border-color 0.2s;
}
.cm-stat-card:hover { border-color: rgba(229,9,20,0.35); }
.cm-stat-num {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #e50914, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.cm-stat-label {
    font-size: 12px;
    color: #8892a4;
    margin-top: 6px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ═══════════════════════════════════════════════════════════════════
   GENRE CARDS (home page grid)
═══════════════════════════════════════════════════════════════════ */
.genre-card {
    border-radius: 12px;
    padding: 28px 20px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.25s, box-shadow 0.25s;
    border: 1px solid rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}
.genre-card::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0.07;
    background: inherit;
    filter: blur(20px);
}
.genre-card:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}
.genre-card-icon  { font-size: 32px; margin-bottom: 10px; }
.genre-card-label { font-size: 14px; font-weight: 700; color: #f1f1f1; letter-spacing: 0.2px; }
.genre-card-count { font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 4px; }

/* ═══════════════════════════════════════════════════════════════════
   WATCHLIST CARD
═══════════════════════════════════════════════════════════════════ */
.wl-card {
    background: #12121a;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: border-color 0.2s, transform 0.2s;
    margin-bottom: 10px;
}
.wl-card:hover { border-color: rgba(229,9,20,0.3); transform: translateX(4px); }
.wl-card-icon  { font-size: 28px; flex-shrink: 0; }
.wl-card-info  { flex: 1; min-width: 0; }
.wl-card-title { color: #f1f1f1; font-size: 14px; font-weight: 700;
                  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wl-card-genre { color: #8892a4; font-size: 12px; margin-top: 3px; }

/* ═══════════════════════════════════════════════════════════════════
   NOTIFICATION TOAST (success / error)
═══════════════════════════════════════════════════════════════════ */
.cm-toast {
    background: #12121a;
    border: 1px solid #1e2a3a;
    border-left: 4px solid #e50914;
    border-radius: 8px;
    padding: 14px 18px;
    color: #f1f1f1;
    font-size: 14px;
    line-height: 1.5;
    margin: 12px 0;
}
.cm-toast.success { border-left-color: #10b981; }
.cm-toast.info    { border-left-color: #7c3aed; }

/* ═══════════════════════════════════════════════════════════════════
   EMPTY STATE
═══════════════════════════════════════════════════════════════════ */
.cm-empty-state {
    background: #12121a;
    border: 2px dashed #1e2a3a;
    border-radius: 16px;
    padding: 64px 40px;
    text-align: center;
    margin: 24px 0;
}
.cm-empty-state-icon  { font-size: 56px; margin-bottom: 16px; }
.cm-empty-state-title { font-size: 20px; font-weight: 700; color: #f1f1f1; margin-bottom: 8px; }
.cm-empty-state-desc  { font-size: 14px; color: #8892a4; max-width: 400px;
                         margin: 0 auto; line-height: 1.65; }

/* ═══════════════════════════════════════════════════════════════════
   PROGRESS / SIMILARITY BAR
═══════════════════════════════════════════════════════════════════ */
.sim-bar-wrap  { background:#1e2a3a; border-radius:8px; height:5px; margin-top:8px; overflow:hidden; }
.sim-bar-fill  { height:5px; border-radius:8px;
                  background: linear-gradient(90deg,#e50914,#7c3aed); }

/* ═══════════════════════════════════════════════════════════════════
   HORIZONTAL SCROLL ROW
═══════════════════════════════════════════════════════════════════ */
.scroll-row-container { overflow-x: auto; padding-bottom: 12px; scrollbar-width: thin;
                         scrollbar-color: #1e2a3a transparent; }
.scroll-row-container::-webkit-scrollbar { height: 4px; }
.scroll-row-container::-webkit-scrollbar-track { background: transparent; }
.scroll-row-container::-webkit-scrollbar-thumb { background: #1e2a3a; border-radius: 4px; }

/* ═══════════════════════════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════════════════════════ */
.cm-divider { border: none; border-top: 1px solid #1e2a3a; margin: 36px 0; }

/* ═══════════════════════════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════════════════════════ */
.cm-footer {
    text-align: center;
    color: #4a5568;
    font-size: 12px;
    padding: 32px 0 48px;
    border-top: 1px solid #1e2a3a;
    margin-top: 48px;
}
.cm-footer a { color: #e50914; text-decoration: none; }
.cm-footer a:hover { text-decoration: underline; }

/* ═══════════════════════════════════════════════════════════════════
   PAGE WRAPPER  (consistent inner padding)
═══════════════════════════════════════════════════════════════════ */
.cm-page { padding: 32px 36px 0; max-width: 1300px; margin: 0 auto; }

/* ═══════════════════════════════════════════════════════════════════
   SELECTED MOVIE PANEL
═══════════════════════════════════════════════════════════════════ */
.selected-panel {
    background: linear-gradient(135deg, #1a0a1e 0%, #12121a 60%, #0d1a2e 100%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.selected-panel::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(229,9,20,0.08) 0%, transparent 70%);
}
.selected-panel-eyebrow { font-size: 10px; color:#7c3aed; font-weight:700;
                            letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px; }
.selected-panel-title   { font-size: 22px; font-weight:800; color:#f1f1f1; margin-bottom:12px; }

/* ═══════════════════════════════════════════════════════════════════
   ABOUT PAGE
═══════════════════════════════════════════════════════════════════ */
.about-block {
    background: #12121a;
    border: 1px solid #1e2a3a;
    border-radius: 14px;
    padding: 28px 30px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}
.about-block:hover { border-color: rgba(229,9,20,0.25); }
.about-block h3 { font-size: 17px !important; font-weight: 700 !important;
                   color: #f1f1f1 !important; margin-bottom: 12px; }
.about-block p  { font-size: 14px !important; color: #8892a4 !important; line-height:1.75 !important; }
.about-block ul { padding-left: 18px; }
.about-block li { color: #8892a4; font-size: 14px; line-height: 1.8; }
.formula-box {
    background: #0a0a0f;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 20px 24px;
    font-family: 'Courier New', monospace;
    color: #a78bfa;
    font-size: 14px;
    text-align: center;
    margin: 14px 0;
    letter-spacing: 0.5px;
}
.tech-chip {
    display: inline-block;
    background: rgba(124,58,237,0.12);
    color: #a78bfa;
    border: 1px solid rgba(124,58,237,0.25);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px;
}

/* ═══════════════════════════════════════════════════════════════════
   RANK NUMBER BADGE
═══════════════════════════════════════════════════════════════════ */
.rank-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #e50914, #7c3aed);
    color: #fff;
    font-size: 11px;
    font-weight: 800;
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════════════════════
   SPINNER OVERRIDE
═══════════════════════════════════════════════════════════════════ */
[data-testid="stSpinner"] > div {
    border-top-color: #e50914 !important;
}
</style>
"""


def inject_global_css():
    """Inject the shared CineMatch CSS into the current Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def sidebar_nav(active_page: str = ""):
    """
    Render the shared premium sidebar navigation.
    active_page: one of 'home','recommend','discover','genres','watchlist','about'
    """
    with st.sidebar:
        # ── Brand ──────────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding:4px 0 20px;">
              <div style="font-size:26px;font-weight:900;
                          background:linear-gradient(135deg,#e50914,#7c3aed);
                          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                          background-clip:text;letter-spacing:-1px;line-height:1;">
                🎬 CineMatch
              </div>
              <div style="font-size:10px;color:#4a5568;letter-spacing:2px;
                          text-transform:uppercase;margin-top:4px;">
                Movie Discovery Platform
              </div>
            </div>
            <hr style="border:none;border-top:1px solid #1e2a3a;margin:0 0 16px;">
            """,
            unsafe_allow_html=True,
        )

        # ── Nav links ───────────────────────────────────────────────
        st.markdown(
            '<p style="font-size:10px;color:#4a5568;font-weight:700;'
            'letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">Navigation</p>',
            unsafe_allow_html=True,
        )
        st.page_link("app.py",                          label="🏠  Home")
        st.page_link("pages/1_Recommend_Movies.py",     label="🎯  Recommendations")
        st.page_link("pages/2_Explore_Movies.py",       label="🔍  Discover Movies")
        st.page_link("pages/3_About_Project.py",        label="📖  About CineMatch")
        st.page_link("pages/4_Watchlist.py",            label="❤️  My Watchlist")

        st.markdown("<hr style='border:none;border-top:1px solid #1e2a3a;margin:16px 0;'>",
                    unsafe_allow_html=True)

        # ── Watchlist count badge ───────────────────────────────────
        wl = st.session_state.get("watchlist", [])
        count = len(wl)
        badge_color = "#e50914" if count > 0 else "#4a5568"
        st.markdown(
            f"""
            <div style="background:#12121a;border:1px solid #1e2a3a;border-radius:10px;
                        padding:12px 14px;display:flex;align-items:center;gap:10px;">
              <span style="font-size:18px;">❤️</span>
              <div>
                <div style="font-size:12px;font-weight:700;color:#f1f1f1;">My Watchlist</div>
                <div style="font-size:11px;color:{badge_color};font-weight:600;">
                  {count} movie{'s' if count != 1 else ''} saved
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section_header(title: str, subtitle: str = ""):
    """Render a branded section heading with a gradient left-bar."""
    sub_html = (
        f'<div class="section-label-sub">{subtitle}</div>' if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="section-label">
          <div class="section-label-line"></div>
          <div>
            <div class="section-label-text">{title}</div>
            {sub_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def movie_card_html(
    title: str,
    genres: str,
    year: str = "",
    rating: str = "",
    similarity_pct: str = "",
    rank: int = 0,
    similarity_score: float = 0.0,
    movie_id: int = 0,
) -> str:
    """
    Return the HTML for a single movie card.
    Uses placeholder art based on the first genre colour.
    """
    # Colour-coded gradient by genre family
    genre_colors = {
        "action":     ("linear-gradient(135deg,#7f1d1d,#991b1b)", "💥"),
        "adventure":  ("linear-gradient(135deg,#064e3b,#065f46)", "🗺️"),
        "animation":  ("linear-gradient(135deg,#1e3a5f,#1d4ed8)", "🎨"),
        "children":   ("linear-gradient(135deg,#4c1d95,#5b21b6)", "🧒"),
        "comedy":     ("linear-gradient(135deg,#78350f,#92400e)", "😂"),
        "crime":      ("linear-gradient(135deg,#111827,#1f2937)", "🔫"),
        "documentary":("linear-gradient(135deg,#1e3a5f,#1e40af)", "🎥"),
        "drama":      ("linear-gradient(135deg,#1a1a2e,#16213e)", "🎭"),
        "fantasy":    ("linear-gradient(135deg,#312e81,#3730a3)", "🧙"),
        "horror":     ("linear-gradient(135deg,#1a0000,#3b0000)", "👻"),
        "musical":    ("linear-gradient(135deg,#4a1d96,#6d28d9)", "🎵"),
        "mystery":    ("linear-gradient(135deg,#0f172a,#1e293b)", "🔍"),
        "romance":    ("linear-gradient(135deg,#831843,#9d174d)", "❤️"),
        "sci-fi":     ("linear-gradient(135deg,#0c1a3e,#1e3a8a)", "🚀"),
        "scifi":      ("linear-gradient(135deg,#0c1a3e,#1e3a8a)", "🚀"),
        "thriller":   ("linear-gradient(135deg,#1a0a0a,#2d1515)", "⚡"),
        "war":        ("linear-gradient(135deg,#1a1a0a,#2d2d1a)", "🎖️"),
        "western":    ("linear-gradient(135deg,#2d1a0a,#451a03)", "🤠"),
    }

    # Pick colour based on first genre
    first_genre = genres.split("|")[0].strip().lower().replace("-", "")
    grad, icon = genre_colors.get(first_genre, ("linear-gradient(135deg,#12121a,#1a1a2e)", "🎬"))

    # Genre pills (max 2)
    genre_parts = [g.strip() for g in genres.split("|") if g.strip()][:2]
    genre_pills = "".join(
        f'<span class="cm-genre-pill">{g}</span>' for g in genre_parts
    )

    year_html   = f'<span class="cm-card-year">{year}</span>' if year else ""
    rating_html = (
        f'<span class="cm-card-rating">⭐ {rating}</span>' if rating else ""
    )
    sim_html = (
        f'<div style="margin-top:8px;"><span class="sim-badge">✦ {similarity_pct} Match</span></div>'
        if similarity_pct else ""
    )
    rank_html = (
        f'<div style="position:absolute;top:10px;left:10px;z-index:5;">'
        f'<span class="rank-num">#{rank}</span></div>'
        if rank > 0 else ""
    )
    sim_bar = ""
    if similarity_score > 0:
        pct = int(similarity_score * 100)
        sim_bar = f"""
        <div class="sim-bar-wrap">
          <div class="sim-bar-fill" style="width:{pct}%;"></div>
        </div>"""

    return f"""
    <div class="cm-card">
      {rank_html}
      <div class="cm-card-poster">
        <div class="cm-card-poster-placeholder" style="background:{grad};">
          <div class="film-icon">{icon}</div>
          <div class="film-title-preview">{title[:28]}{'…' if len(title) > 28 else ''}</div>
        </div>
        <div class="cm-card-overlay">
          <button class="cm-overlay-btn cm-overlay-btn-primary">🎯 Get Similar</button>
          <button class="cm-overlay-btn cm-overlay-btn-secondary">❤️ Add to Watchlist</button>
        </div>
      </div>
      <div class="cm-card-body">
        <div class="cm-card-title" title="{title}">{title}</div>
        <div class="cm-card-meta">
          {year_html}
          {rating_html}
        </div>
        <div class="cm-card-genres">{genre_pills}</div>
        {sim_html}
        {sim_bar}
      </div>
    </div>"""


def empty_state(icon: str, title: str, desc: str):
    """Render a full-width empty-state placeholder."""
    st.markdown(
        f"""
        <div class="cm-empty-state">
          <div class="cm-empty-state-icon">{icon}</div>
          <div class="cm-empty-state-title">{title}</div>
          <div class="cm-empty-state-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def toast(message: str, kind: str = "info"):
    """Render an inline toast notification. kind = info | success | error"""
    icon_map = {"info": "ℹ️", "success": "✅", "error": "⚠️"}
    icon = icon_map.get(kind, "ℹ️")
    cls  = {"info": "info", "success": "success", "error": ""}.get(kind, "")
    st.markdown(
        f'<div class="cm-toast {cls}">{icon} {message}</div>',
        unsafe_allow_html=True,
    )


def extract_year(title: str) -> str:
    """Pull the 4-digit year from a MovieLens title like 'Toy Story (1995)'."""
    import re
    m = re.search(r"\((\d{4})\)\s*$", title)
    return m.group(1) if m else ""


def strip_year(title: str) -> str:
    """Return title without the trailing year, e.g. 'Toy Story (1995)' → 'Toy Story'."""
    import re
    return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
