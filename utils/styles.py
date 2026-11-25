"""
utils/styles.py
---------------
Shared CSS theme + UI helpers for CineMatch.
Call inject_global_css() at the top of every page.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ═══════════════════════════════ RESET & BASE ═════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: #08080c !important;
    color: #f1f1f1 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════════ HIDE DEFAULT STREAMLIT CHROME ═════════ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"] { display: none !important; }

/* ═══════════════════════════════ SIDEBAR REDESIGN ═════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0e16 0%, #08080c 100%) !important;
    border-right: 1px solid #1a1b26 !important;
    min-width: 250px !important;
    max-width: 250px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 24px 16px !important; }
[data-testid="stSidebar"] * { color: #c8d0dc !important; }
[data-testid="stSidebar"] a { text-decoration: none !important; }

[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 3px 0 !important;
    transition: all 0.25s ease !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: rgba(229, 9, 20, 0.12) !important;
    color: #ffffff !important;
    border-color: rgba(229, 9, 20, 0.3) !important;
    transform: translateX(4px) !important;
}
[data-testid="stSidebar"] [aria-current="page"] {
    background: linear-gradient(90deg, rgba(229,9,20,0.2) 0%, rgba(124,58,237,0.1) 100%) !important;
    border-left: 3px solid #e50914 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ═══════════════════════════════ TYPOGRAPHY ══════════════════════════ */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
}
h1 { font-size: 2.5rem !important; font-weight: 900 !important; letter-spacing: -1.2px; }
h2 { font-size: 1.8rem !important; font-weight: 800 !important; letter-spacing: -0.5px; }
h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
p  { color: #94a3b8 !important; line-height: 1.7 !important; }

/* ═══════════════════════════════ BUTTONS ═════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #e50914 0%, #c40812 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 18px rgba(229, 9, 20, 0.38) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(229, 9, 20, 0.55) !important;
    background: linear-gradient(135deg, #f01420 0%, #dc0a15 100%) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.btn-ghost > button {
    background: rgba(255,255,255,0.06) !important;
    color: #f1f1f1 !important;
    border: 1px solid #2a2b3d !important;
    box-shadow: none !important;
}
.btn-ghost > button:hover {
    border-color: #e50914 !important;
    color: #ffffff !important;
    background: rgba(229,9,20,0.15) !important;
}
.btn-sm > button {
    padding: 6px 14px !important;
    font-size: 12px !important;
}

/* ═══════════════════════════════ INPUTS ══════════════════════════════ */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stMultiSelect > div > div {
    background-color: #12131c !important;
    color: #f1f1f1 !important;
    border: 1px solid #202230 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.2) !important;
    background-color: #161724 !important;
}
.stTextInput label, .stSelectbox label, .stMultiSelect label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════════ POSTER CARDS ════════════════════════ */
[data-testid="stImage"] {
    display: block !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #1e2230 !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.35s ease !important;
    background: #111118 !important;
}
[data-testid="stImage"]:hover {
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: 0 20px 45px rgba(0,0,0,0.85),
                0 0 24px rgba(229,9,20,0.35) !important;
    border-color: rgba(229,9,20,0.55) !important;
    z-index: 10 !important;
}
[data-testid="stImage"] img {
    width: 100% !important;
    aspect-ratio: 2/3 !important;
    object-fit: cover !important;
    display: block !important;
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
[data-testid="stImage"]:hover img {
    transform: scale(1.06) !important;
}

/* Legacy & HTML .poster-card */
.poster-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #111118;
    cursor: pointer;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1),
                border-color 0.35s ease;
    border: 1px solid #1e2230;
    display: block;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.poster-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 45px rgba(0,0,0,0.85),
                0 0 24px rgba(229,9,20,0.35);
    border-color: rgba(229,9,20,0.55);
    z-index: 25;
}
.poster-card img.poster-img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}
.poster-card:hover img.poster-img {
    transform: scale(1.06);
}
.poster-card .poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        180deg,
        rgba(0,0,0,0.1) 0%,
        transparent 35%,
        rgba(0,0,0,0.65) 65%,
        rgba(8,8,12,0.98) 100%
    );
    pointer-events: none;
    transition: background 0.3s ease;
}
.poster-card:hover .poster-overlay {
    background: linear-gradient(
        180deg,
        rgba(0,0,0,0.2) 0%,
        rgba(0,0,0,0.45) 40%,
        rgba(8,8,12,0.95) 100%
    );
}
.poster-hover-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 6;
}
.poster-card:hover .poster-hover-overlay {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
}
.poster-hover-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(229,9,20,0.92);
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    padding: 7px 14px;
    border-radius: 20px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.poster-card .poster-info {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 12px 10px 10px;
    z-index: 5;
}
.poster-card .poster-title {
    font-size: 13px; font-weight: 700; color: #f1f1f1;
    line-height: 1.3; margin-bottom: 4px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.poster-card .poster-meta {
    display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
}
.poster-card .poster-year   { font-size: 11px; color: #94a3b8; font-weight: 500; }
.poster-card .poster-rating { font-size: 11px; color: #fbbf24; font-weight: 700; }
.poster-card .poster-genre-pill {
    font-size: 10px; color: #a78bfa;
    background: rgba(124,58,237,0.18); border: 1px solid rgba(124,58,237,0.28);
    padding: 1px 7px; border-radius: 20px; white-space: nowrap;
}

/* Badges */
.poster-rank {
    position: absolute; top: 10px; left: 10px;
    width: 26px; height: 26px; border-radius: 50%;
    background: linear-gradient(135deg,#e50914,#7c3aed);
    color: #fff; font-size: 11px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    z-index: 5; box-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.sim-badge-poster {
    position: absolute; top: 10px; left: 10px;
    background: linear-gradient(135deg,#e50914,#7c3aed);
    color: #fff; font-size: 10px; font-weight: 700;
    padding: 3px 8px; border-radius: 20px; z-index: 5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4); white-space: nowrap;
}
.tv-badge {
    position: absolute; top: 10px; left: 10px; z-index: 5;
    background: rgba(124,58,237,0.85); color: #fff;
    font-size: 9px; font-weight: 800; letter-spacing: 1px;
    padding: 3px 8px; border-radius: 4px; text-transform: uppercase;
    backdrop-filter: blur(4px);
}

/* ═══════════════════════════════ HORIZONTAL SCROLL ROW ═══════════════ */
.poster-scroll-row {
    display: flex;
    gap: 16px;
    overflow-x: auto;
    padding: 14px 4px 24px 4px;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}
.poster-scroll-row::-webkit-scrollbar {
    height: 8px;
}
.poster-scroll-row::-webkit-scrollbar-track {
    background: #111118;
    border-radius: 4px;
}
.poster-scroll-row::-webkit-scrollbar-thumb {
    background: #2a2a3e;
    border-radius: 4px;
}
.poster-scroll-row::-webkit-scrollbar-thumb:hover {
    background: #e50914;
}
.poster-scroll-item {
    flex: 0 0 195px;
    width: 195px;
    max-width: 195px;
}

/* ═══════════════════════════════ MOVIE DETAIL PANEL ═════════════════ */
.detail-panel {
    background: linear-gradient(135deg, #0e0e18 0%, #12131f 60%, #150f24 100%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 32px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}
.detail-backdrop {
    width: 100%; height: 260px;
    object-fit: cover;
    object-position: center 30%;
    display: block;
    filter: brightness(0.42);
}
.detail-body {
    padding: 24px 32px 32px;
    display: flex;
    gap: 28px;
    margin-top: -80px;
    position: relative;
}
.detail-poster-wrap {
    flex-shrink: 0;
    width: 140px;
}
.detail-poster-wrap img {
    width: 140px;
    border-radius: 12px;
    border: 3px solid #202232;
    box-shadow: 0 12px 36px rgba(0,0,0,0.7);
    display: block;
}
.detail-info { flex: 1; min-width: 0; padding-top: 75px; }
.detail-title {
    font-size: 26px; font-weight: 900; color: #f1f1f1;
    letter-spacing: -0.5px; margin-bottom: 8px;
    line-height: 1.2;
}
.detail-meta-row {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 10px; margin-bottom: 14px;
}
.detail-pill {
    padding: 4px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
    white-space: nowrap;
}
.detail-pill-year   { background:rgba(229,9,20,0.12); color:#e50914; border:1px solid rgba(229,9,20,0.25);}
.detail-pill-rating { background:rgba(251,191,36,0.1); color:#fbbf24; border:1px solid rgba(251,191,36,0.2);}
.detail-pill-genre  { background:rgba(124,58,237,0.14); color:#a78bfa; border:1px solid rgba(124,58,237,0.25);}
.detail-pill-runtime{ background:rgba(16,185,129,0.1); color:#34d399; border:1px solid rgba(16,185,129,0.2);}
.detail-overview {
    font-size: 14px; color: #94a3b8; line-height: 1.75;
    margin-bottom: 16px; max-width: 720px;
}
.detail-tagline {
    font-size: 14px; color: #a78bfa; font-style: italic;
    margin-bottom: 10px; font-weight: 500;
}

/* ═══════════════════════════════ STAT CARDS ══════════════════════════ */
.cm-stat-card {
    background: #111118;
    border: 1px solid #1e2230;
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
    transition: all 0.25s ease;
}
.cm-stat-card:hover {
    border-color: rgba(229,9,20,0.4);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.cm-stat-num {
    font-size: 34px; font-weight: 900;
    background: linear-gradient(135deg, #ffffff 30%, #e50914 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.1;
}
.cm-stat-label { font-size: 12px; color: #8892a4; margin-top: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }

/* ═══════════════════════════════ GENRE CARDS ═════════════════════════ */
.genre-card {
    border-radius: 14px; padding: 26px 18px;
    text-align: center; cursor: pointer;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    border: 1px solid rgba(255,255,255,0.06);
    position: relative; overflow: hidden;
}
.genre-card:hover {
    transform: translateY(-6px) scale(1.04);
    box-shadow: 0 18px 45px rgba(0,0,0,0.65);
    border-color: rgba(255,255,255,0.2);
}
.genre-card-icon  { font-size: 36px; margin-bottom: 10px; }
.genre-card-label { font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: -0.2px; }
.genre-card-count { font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 4px; font-weight: 500; }

/* ═══════════════════════════════ ABOUT BLOCKS ════════════════════════ */
.about-block {
    background: #111118; border: 1px solid #1e2230;
    border-radius: 14px; padding: 28px 30px; margin-bottom: 20px;
    transition: border-color 0.2s;
}
.about-block:hover { border-color: rgba(229,9,20,0.3); }
.about-block h3 { font-size: 18px !important; font-weight: 700 !important;
                  color: #f1f1f1 !important; margin-bottom: 12px; }
.about-block p  { font-size: 14px !important; color: #8892a4 !important; line-height: 1.75 !important; }
.about-block ul { padding-left: 18px; }
.about-block li { color: #8892a4; font-size: 14px; line-height: 1.8; }
.formula-box {
    background: #08080c; border: 1px solid #1e2230; border-radius: 10px;
    padding: 20px 24px; font-family: 'Courier New', monospace;
    color: #a78bfa; font-size: 14px; text-align: center; margin: 14px 0;
}
.tech-chip {
    display: inline-block; background: rgba(124,58,237,0.12);
    color: #a78bfa; border: 1px solid rgba(124,58,237,0.25);
    padding: 6px 14px; border-radius: 20px; font-size: 12px;
    font-weight: 600; margin: 4px;
}

/* ═══════════════════════════════ TOAST & EMPTY STATE ═════════════════ */
.cm-toast {
    background: #111118; border: 1px solid #1e2230;
    border-left: 4px solid #e50914; border-radius: 10px;
    padding: 14px 18px; color: #f1f1f1; font-size: 14px;
    line-height: 1.5; margin: 12px 0;
}
.cm-toast.success { border-left-color: #10b981; }
.cm-toast.info    { border-left-color: #7c3aed; }

.cm-empty-state {
    background: #111118; border: 2px dashed #202232;
    border-radius: 18px; padding: 64px 40px; text-align: center; margin: 24px 0;
}
.cm-empty-state-icon  { font-size: 56px; margin-bottom: 16px; }
.cm-empty-state-title { font-size: 20px; font-weight: 800; color: #f1f1f1; margin-bottom: 8px; }
.cm-empty-state-desc  { font-size: 14px; color: #8892a4; max-width: 440px;
                         margin: 0 auto; line-height: 1.65; }

/* ═══════════════════════════════ MISC & LAYOUT ═══════════════════════ */
.cm-divider { border: none; border-top: 1px solid #1e2230; margin: 36px 0; }
.cm-page { padding: 32px 40px 0; max-width: 1360px; margin: 0 auto; }
.cm-footer {
    text-align: center; color: #64748b; font-size: 12px;
    padding: 36px 0 48px; border-top: 1px solid #1e2230; margin-top: 56px;
}
.cm-footer a { color: #e50914; text-decoration: none; font-weight: 600; }

.api-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(229,9,20,0.06));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 12px; padding: 14px 20px;
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 24px; font-size: 13px; color: #94a3b8;
}
.api-banner strong { color: #a78bfa; }

[data-testid="stSpinner"] > div { border-top-color: #e50914 !important; }
</style>
"""


def inject_global_css():
    """Inject global CSS rules into the Streamlit session."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def sidebar_nav(active_page: str = ""):
    """Render the sleek, modern CineMatch sidebar navigation."""
    with st.sidebar:
        # CineMatch logo & branding
        st.markdown(
            """
            <div style="padding: 6px 0 20px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; border-radius: 10px;
                            background: linear-gradient(135deg, #e50914 0%, #7c3aed 100%);
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 16px rgba(229, 9, 20, 0.45); font-size: 20px;">
                  🎬
                </div>
                <div>
                  <div style="font-size: 22px; font-weight: 900;
                              background: linear-gradient(135deg, #ffffff 40%, #e50914 100%);
                              -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                              background-clip: text; letter-spacing: -0.5px; line-height: 1.1;">
                    CineMatch
                  </div>
                  <div style="font-size: 10px; color: #a78bfa; font-weight: 700;
                              letter-spacing: 1.8px; text-transform: uppercase;">
                    Stream &amp; Discover
                  </div>
                </div>
              </div>
            </div>
            <hr style="border: none; border-top: 1px solid #1e2230; margin: 0 0 16px;">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="font-size: 10px; color: #64748b; font-weight: 700;'
            'letter-spacing: 1.6px; text-transform: uppercase; margin-bottom: 8px;">Menu</p>',
            unsafe_allow_html=True,
        )

        # Navigation links
        st.page_link("app.py",                      label="Home",            icon="🏠")
        st.page_link("pages/2_Explore_Movies.py",   label="Discover",        icon="✨")
        st.page_link("pages/2_Explore_Movies.py",   label="Movies",          icon="🎬")
        st.page_link("pages/5_Web_Series.py",       label="Web Series",      icon="📺")
        st.page_link("pages/1_Recommend_Movies.py", label="Recommendations", icon="🎯")
        st.page_link("pages/2_Explore_Movies.py",   label="Genres",          icon="🎭")
        st.page_link("pages/4_Watchlist.py",        label="My Watchlist",    icon="❤️")
        st.page_link("pages/3_About_Project.py",    label="About",           icon="ℹ️")

        # Watchlist quick summary widget
        st.markdown("<hr style='border:none;border-top:1px solid #1e2230;margin:18px 0;'>",
                    unsafe_allow_html=True)
        wl    = st.session_state.get("watchlist", [])
        count = len(wl)
        bc    = "#e50914" if count > 0 else "#64748b"
        st.markdown(
            f"""
            <a href="/4_Watchlist" target="_self" style="text-decoration:none;">
              <div style="background: linear-gradient(135deg, rgba(229,9,20,0.08) 0%, rgba(124,58,237,0.08) 100%);
                          border: 1px solid rgba(229,9,20,0.25); border-radius: 12px;
                          padding: 12px 14px; display: flex; align-items: center; justify-content: space-between;
                          transition: all 0.2s ease;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span style="font-size: 18px;">❤️</span>
                  <div>
                    <div style="font-size: 12px; font-weight: 700; color: #f1f1f1;">My Watchlist</div>
                    <div style="font-size: 11px; color: {bc}; font-weight: 600;">
                      {count} saved title{'s' if count != 1 else ''}
                    </div>
                  </div>
                </div>
                <span style="color: #64748b; font-size: 14px;">→</span>
              </div>
            </a>
            """,
            unsafe_allow_html=True,
        )


def section_header(title: str, subtitle: str = ""):
    """Render a streaming-style section title bar."""
    sub = f'<div style="font-size:13px;color:#8892a4;margin-top:2px;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
          <div style="width:4px;height:24px;background:linear-gradient(180deg,#e50914,#7c3aed);
                      border-radius:4px;flex-shrink:0;"></div>
          <div>
            <div style="font-size:20px;font-weight:800;color:#f1f1f1;
                        letter-spacing:-0.3px;">{title}</div>
            {sub}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_poster_card(
    col,
    title: str,
    poster_url: str,
    genres: str = "",
    year: str = "",
    rating: str = "",
    similarity_pct: str = "",
    rank: int = 0,
    is_tv: bool = False,
):
    """
    Render a complete poster card inside a Streamlit column using st.image().
    """
    genre_parts = [g.strip() for g in genres.replace("|", ",").split(",") if g.strip()]
    genre_text  = " · ".join(genre_parts[:2]) if genre_parts else ""

    badge_parts = []
    if similarity_pct:
        badge_parts.append(
            f'<span style="display:inline-block;background:linear-gradient(135deg,#e50914,#7c3aed);'
            f'color:#fff;font-size:10px;font-weight:700;padding:3px 9px;'
            f'border-radius:20px;letter-spacing:0.3px;">✦ {similarity_pct}</span>'
        )
    if rank > 0 and not similarity_pct:
        badge_parts.append(
            f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:22px;height:22px;border-radius:50%;'
            f'background:linear-gradient(135deg,#e50914,#7c3aed);'
            f'color:#fff;font-size:11px;font-weight:800;">#{rank}</span>'
        )
    if is_tv:
        badge_parts.append(
            f'<span style="display:inline-block;background:rgba(124,58,237,0.85);'
            f'color:#fff;font-size:9px;font-weight:800;letter-spacing:1px;'
            f'padding:3px 8px;border-radius:4px;text-transform:uppercase;">SERIES</span>'
        )

    safe_title = title.replace("<", "&lt;").replace(">", "&gt;")
    import re as _re
    display_title = _re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    with col:
        if badge_parts:
            st.markdown(
                f'<div style="display:flex;gap:5px;align-items:center;'
                f'margin-bottom:5px;min-height:22px;">'
                + "".join(badge_parts)
                + "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div style="min-height:27px;"></div>', unsafe_allow_html=True)

        try:
            st.image(poster_url, use_container_width=True)
        except Exception:
            from utils.tmdb import placeholder_img_url as _ph
            st.image(_ph(genres, title), use_container_width=True)

        rating_html = (
            f'<span style="color:#fbbf24;font-size:11px;font-weight:700;">⭐ {rating}</span>'
            if rating else ""
        )
        year_html = (
            f'<span style="color:#94a3b8;font-size:11px;font-weight:500;">{year}</span>'
            if year else ""
        )
        meta_parts = [p for p in [year_html, rating_html] if p]
        meta_row   = (
            f'<div style="display:flex;align-items:center;gap:8px;margin-top:3px;">'
            + "".join(meta_parts)
            + "</div>"
        ) if meta_parts else ""

        genre_row = (
            f'<div style="margin-top:4px;">'
            f'<span style="font-size:10px;color:#a78bfa;background:rgba(124,58,237,0.15);'
            f'border:1px solid rgba(124,58,237,0.25);padding:1px 7px;border-radius:20px;">'
            f'{genre_text}</span></div>'
        ) if genre_text else ""

        st.markdown(
            f'<div style="padding:6px 2px 10px;">'
            f'  <div style="font-size:13px;font-weight:700;color:#f1f1f1;'
            f'              line-height:1.3;white-space:nowrap;overflow:hidden;'
            f'              text-overflow:ellipsis;" title="{safe_title}">'
            f'    {display_title}'
            f'  </div>'
            f'  {meta_row}'
            f'  {genre_row}'
            f'</div>',
            unsafe_allow_html=True,
        )


def poster_card_html(
    title: str,
    poster_url: str,
    genres: str = "",
    year: str = "",
    rating: str = "",
    similarity_pct: str = "",
    rank: int = 0,
    is_tv: bool = False,
) -> str:
    """
    Render a self-contained HTML poster card with hover overlay and metadata.
    """
    import re as _re
    genre_parts   = [g.strip() for g in genres.replace("|", ",").split(",") if g.strip()]
    genre_text    = " · ".join(genre_parts[:2]) if genre_parts else ""
    genre_pill    = f'<span class="poster-genre-pill">{genre_text}</span>' if genre_text else ""
    display_title = _re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()
    safe_title    = title.replace('"', "&quot;").replace("'", "&#39;")

    year_html   = f'<span class="poster-year">{year}</span>' if year else ""
    rating_html = f'<span class="poster-rating">⭐ {rating}</span>' if rating else ""

    if similarity_pct:
        top_badge = f'<div class="sim-badge-poster">✦ {similarity_pct}</div>'
    elif rank > 0:
        top_badge = f'<div class="poster-rank">#{rank}</div>'
    else:
        top_badge = ""
    if is_tv:
        top_badge += '<div class="tv-badge" style="top:40px;">SERIES</div>'

    return f"""
<div class="poster-card">
  {top_badge}
  <img class="poster-img" src="{poster_url}"
       alt="{safe_title}" loading="lazy"
       onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"
  />
  <div style="display:none;width:100%;aspect-ratio:2/3;background:#12121a;
              align-items:center;justify-content:center;flex-direction:column;gap:8px;">
    <span style="font-size:40px;opacity:.35;">🎬</span>
    <span style="font-size:11px;color:#4a5568;text-align:center;padding:0 12px;">{safe_title[:24]}</span>
  </div>
  <div class="poster-hover-overlay">
    <span class="poster-hover-btn">▶ View Details</span>
  </div>
  <div class="poster-overlay"></div>
  <div class="poster-info">
    <div class="poster-title" title="{safe_title}">{display_title}</div>
    <div class="poster-meta">
      {year_html}
      {rating_html}
      {genre_pill}
    </div>
  </div>
</div>"""


def horizontal_scroll_row_html(items: list[dict]) -> str:
    """
    Render a Netflix-style horizontal scrolling poster row from a list of movie/TV dicts.
    """
    cards_html = []
    for item in items:
        card = poster_card_html(
            title=item.get("title", ""),
            poster_url=item.get("poster_url", ""),
            genres=item.get("genres", ""),
            year=item.get("year", ""),
            rating=item.get("rating", ""),
            similarity_pct=item.get("similarity_pct", ""),
            rank=item.get("rank", 0),
            is_tv=item.get("is_tv", False),
        )
        cards_html.append(f'<div class="poster-scroll-item">{card}</div>')
    return f'<div class="poster-scroll-row">{"".join(cards_html)}</div>'


def empty_state(icon: str, title: str, desc: str):
    """Render an empty state card."""
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
    """Render an inline toast alert."""
    icons = {"info": "ℹ️", "success": "✅", "error": "⚠️"}
    cls   = {"info": "info", "success": "success", "error": ""}.get(kind, "")
    st.markdown(
        f'<div class="cm-toast {cls}">{icons.get(kind,"ℹ️")} {message}</div>',
        unsafe_allow_html=True,
    )


def extract_year(title: str) -> str:
    """Extract 4-digit release year from a MovieLens title."""
    import re
    m = re.search(r"\((\d{4})\)\s*$", title)
    return m.group(1) if m else ""


def strip_year(title: str) -> str:
    """Remove trailing (YYYY) from title."""
    import re
    return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()


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
    """Backward compatibility shim for existing unit tests."""
    from utils.tmdb import placeholder_img_url
    poster = placeholder_img_url(genres, title)
    return poster_card_html(
        title=title, poster_url=poster, genres=genres,
        year=year, rating=rating,
        similarity_pct=similarity_pct, rank=rank,
    )
