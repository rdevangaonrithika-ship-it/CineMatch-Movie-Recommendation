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

/* ═══════════════════════════════ RESET ═══════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: #0a0a0f !important;
    color: #f1f1f1 !important;
    font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════════ HIDE CHROME ═════════════════════════ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ═══════════════════════════════ SIDEBAR ═════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #0a0a0f 100%) !important;
    border-right: 1px solid #1e2a3a !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 24px 16px !important; }
[data-testid="stSidebar"] * { color: #c8d0dc !important; }
[data-testid="stSidebar"] a { text-decoration: none !important; }

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

/* ═══════════════════════════════ TYPOGRAPHY ══════════════════════════ */
h1,h2,h3,h4,h5,h6 { font-family: 'Inter', sans-serif !important; }
h1 { font-size: 2.4rem !important; font-weight: 800 !important; letter-spacing: -1px; }
h2 { font-size: 1.7rem !important; font-weight: 700 !important; }
h3 { font-size: 1.25rem !important; font-weight: 600 !important; }
p  { color: #8892a4 !important; line-height: 1.75 !important; }

/* ═══════════════════════════════ BUTTONS ═════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #e50914, #c40812) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 11px 28px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(229,9,20,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(229,9,20,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.btn-ghost > button {
    background: transparent !important;
    color: #f1f1f1 !important;
    border: 1px solid #2d3748 !important;
    box-shadow: none !important;
}
.btn-ghost > button:hover {
    border-color: #e50914 !important; color: #e50914 !important;
    box-shadow: none !important; transform: translateY(-1px) !important;
}
.btn-sm > button {
    padding: 6px 16px !important;
    font-size: 12px !important;
}

/* ═══════════════════════════════ INPUTS ══════════════════════════════ */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stMultiSelect > div > div {
    background-color: #12121a !important;
    color: #f1f1f1 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.15) !important;
}
.stTextInput label, .stSelectbox label, .stMultiSelect label {
    color: #8892a4 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════════ POSTER CARD ═════════════════════════ */
/*
 * Cards are now rendered with st.image() + st.markdown() per column.
 * The CSS below styles the st.image wrapper and the footer text.
 */

/* Force every st.image inside a card column to be 2:3 and cover-fit */
[data-testid="stImage"] {
    display: block !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #1e2a3a !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease,
                border-color 0.3s ease !important;
}
[data-testid="stImage"]:hover {
    transform: translateY(-6px) !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.65),
                0 0 0 1px rgba(229,9,20,0.4) !important;
    border-color: rgba(229,9,20,0.4) !important;
    z-index: 10 !important;
}
[data-testid="stImage"] img {
    width: 100% !important;
    aspect-ratio: 2/3 !important;
    object-fit: cover !important;
    display: block !important;
    transition: transform 0.4s ease !important;
}
[data-testid="stImage"]:hover img {
    transform: scale(1.05) !important;
}

/* Legacy .poster-card  (used by HTML fallback / tests) */
.poster-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #12121a;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    border: 1px solid #1e2a3a;
    display: block;
}
.poster-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 20px 50px rgba(0,0,0,0.65),
                0 0 0 1px rgba(229,9,20,0.4);
    z-index: 20;
}
.poster-card img.poster-img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    transition: transform 0.4s ease;
}
.poster-card:hover img.poster-img { transform: scale(1.05); }

/* gradient overlay — renders over the img, under the text */
.poster-card .poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top,
        rgba(0,0,0,0.90) 0%,
        rgba(0,0,0,0.40) 45%,
        transparent 75%
    );
    pointer-events: none;
}
.poster-card:hover .poster-overlay {
    background: linear-gradient(
        to top,
        rgba(0,0,0,0.95) 0%,
        rgba(0,0,0,0.60) 55%,
        rgba(0,0,0,0.10) 100%
    );
}

/* text pinned to bottom of card */
.poster-card .poster-info {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 14px 12px 12px;
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

/* rank / sim / TV badges */
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

/* ═══════════════════════════════ HORIZONTAL SCROLL ROW ═══════════════ */
.scroll-section { margin-bottom: 48px; }
.scroll-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}
.scroll-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
}
.scroll-title-bar {
    width: 4px; height: 22px;
    background: linear-gradient(180deg,#e50914,#7c3aed);
    border-radius: 4px; flex-shrink: 0;
}
.scroll-title-text {
    font-size: 20px; font-weight: 800;
    color: #f1f1f1; letter-spacing: -0.3px;
}
.scroll-title-sub {
    font-size: 12px; color: #8892a4; margin-left: 4px;
}
.scroll-see-all {
    font-size: 13px; color: #e50914; font-weight: 600;
    text-decoration: none; transition: opacity 0.2s;
}
.scroll-see-all:hover { opacity: 0.75; }

/* ═══════════════════════════════ MOVIE DETAIL PANEL ═════════════════ */
.detail-panel {
    background: linear-gradient(135deg,#0d0014 0%,#12121a 50%,#0d1a2e 100%);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 32px;
}
.detail-backdrop {
    width: 100%; height: 220px;
    object-fit: cover;
    object-position: center 30%;
    display: block;
    filter: brightness(0.45);
}
.detail-body {
    padding: 24px 28px 28px;
    display: flex;
    gap: 24px;
    margin-top: -60px;
    position: relative;
}
.detail-poster-wrap {
    flex-shrink: 0;
    width: 120px;
}
.detail-poster-wrap img {
    width: 120px;
    border-radius: 10px;
    border: 3px solid #1e2a3a;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    display: block;
}
.detail-info { flex: 1; min-width: 0; padding-top: 60px; }
.detail-title {
    font-size: 22px; font-weight: 900; color: #f1f1f1;
    letter-spacing: -0.5px; margin-bottom: 8px;
    line-height: 1.2;
}
.detail-meta-row {
    display: flex; flex-wrap: wrap; align-items: center;
    gap: 10px; margin-bottom: 12px;
}
.detail-pill {
    padding: 3px 10px; border-radius: 20px;
    font-size: 12px; font-weight: 600;
    white-space: nowrap;
}
.detail-pill-year   { background:rgba(229,9,20,0.12); color:#e50914; border:1px solid rgba(229,9,20,0.25);}
.detail-pill-rating { background:rgba(251,191,36,0.1); color:#fbbf24; border:1px solid rgba(251,191,36,0.2);}
.detail-pill-genre  { background:rgba(124,58,237,0.12); color:#a78bfa; border:1px solid rgba(124,58,237,0.25);}
.detail-pill-runtime{ background:rgba(16,185,129,0.1); color:#34d399; border:1px solid rgba(16,185,129,0.2);}
.detail-overview {
    font-size: 13px; color: #94a3b8; line-height: 1.7;
    margin-bottom: 16px; max-width: 680px;
}
.detail-tagline {
    font-size: 13px; color: #7c3aed; font-style: italic;
    margin-bottom: 10px;
}

/* ═══════════════════════════════ STAT CARD ═══════════════════════════ */
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
    font-size: 32px; font-weight: 900;
    background: linear-gradient(135deg,#e50914,#7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.1;
}
.cm-stat-label { font-size: 12px; color: #8892a4; margin-top: 6px; font-weight: 500; }

/* ═══════════════════════════════ GENRE CARD ══════════════════════════ */
.genre-card {
    border-radius: 12px; padding: 28px 20px;
    text-align: center; cursor: pointer;
    transition: transform 0.25s, box-shadow 0.25s;
    border: 1px solid rgba(255,255,255,0.05);
    position: relative; overflow: hidden;
}
.genre-card:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 16px 40px rgba(0,0,0,0.5);
}
.genre-card-icon  { font-size: 32px; margin-bottom: 10px; }
.genre-card-label { font-size: 14px; font-weight: 700; color: #f1f1f1; }
.genre-card-count { font-size: 11px; color: rgba(255,255,255,0.45); margin-top: 4px; }

/* ═══════════════════════════════ ABOUT BLOCKS ════════════════════════ */
.about-block {
    background: #12121a; border: 1px solid #1e2a3a;
    border-radius: 14px; padding: 28px 30px; margin-bottom: 20px;
    transition: border-color 0.2s;
}
.about-block:hover { border-color: rgba(229,9,20,0.25); }
.about-block h3 { font-size:17px !important; font-weight:700 !important;
                  color:#f1f1f1 !important; margin-bottom:12px; }
.about-block p  { font-size:14px !important; color:#8892a4 !important; line-height:1.75 !important; }
.about-block ul { padding-left:18px; }
.about-block li { color:#8892a4; font-size:14px; line-height:1.8; }
.formula-box {
    background:#0a0a0f; border:1px solid #1e2a3a; border-radius:10px;
    padding:20px 24px; font-family:'Courier New',monospace;
    color:#a78bfa; font-size:14px; text-align:center; margin:14px 0;
}
.tech-chip {
    display:inline-block; background:rgba(124,58,237,0.12);
    color:#a78bfa; border:1px solid rgba(124,58,237,0.25);
    padding:5px 14px; border-radius:20px; font-size:12px;
    font-weight:600; margin:4px;
}

/* ═══════════════════════════════ WATCHLIST CARD ══════════════════════ */
.wl-poster-wrap {
    position: relative;
    border-radius: 8px; overflow: hidden;
    border: 1px solid #1e2a3a;
}
.wl-poster-wrap img {
    width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block;
}

/* ═══════════════════════════════ TOAST / EMPTY ═══════════════════════ */
.cm-toast {
    background:#12121a; border:1px solid #1e2a3a;
    border-left:4px solid #e50914; border-radius:8px;
    padding:14px 18px; color:#f1f1f1; font-size:14px;
    line-height:1.5; margin:12px 0;
}
.cm-toast.success { border-left-color:#10b981; }
.cm-toast.info    { border-left-color:#7c3aed; }

.cm-empty-state {
    background:#12121a; border:2px dashed #1e2a3a;
    border-radius:16px; padding:64px 40px; text-align:center; margin:24px 0;
}
.cm-empty-state-icon  { font-size:56px; margin-bottom:16px; }
.cm-empty-state-title { font-size:20px; font-weight:700; color:#f1f1f1; margin-bottom:8px; }
.cm-empty-state-desc  { font-size:14px; color:#8892a4; max-width:400px;
                         margin:0 auto; line-height:1.65; }

/* ═══════════════════════════════ MISC ════════════════════════════════ */
.cm-divider { border:none; border-top:1px solid #1e2a3a; margin:36px 0; }
.cm-page { padding:32px 36px 0; max-width:1300px; margin:0 auto; }
.cm-footer {
    text-align:center; color:#4a5568; font-size:12px;
    padding:32px 0 48px; border-top:1px solid #1e2a3a; margin-top:48px;
}
.cm-footer a { color:#e50914; text-decoration:none; }

.sim-bar-wrap { background:#1e2a3a; border-radius:8px; height:5px;
                margin-top:8px; overflow:hidden; }
.sim-bar-fill { height:5px; border-radius:8px;
                background:linear-gradient(90deg,#e50914,#7c3aed); }

.selected-panel {
    background:linear-gradient(135deg,#1a0a1e 0%,#12121a 60%,#0d1a2e 100%);
    border:1px solid rgba(124,58,237,0.3); border-radius:14px;
    padding:24px 28px; margin-bottom:28px; position:relative; overflow:hidden;
}
.selected-panel-eyebrow { font-size:10px; color:#7c3aed; font-weight:700;
                            letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px; }
.selected-panel-title   { font-size:22px; font-weight:800; color:#f1f1f1; margin-bottom:12px; }

/* API key notice banner */
.api-banner {
    background: linear-gradient(135deg,rgba(124,58,237,0.08),rgba(229,9,20,0.05));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 10px; padding: 12px 18px;
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 20px; font-size: 13px; color: #8892a4;
}
.api-banner strong { color: #a78bfa; }

/* TV series badge */
.tv-badge {
    position:absolute; top:10px; left:10px; z-index:5;
    background:rgba(124,58,237,0.85); color:#fff;
    font-size:9px; font-weight:800; letter-spacing:1px;
    padding:3px 8px; border-radius:4px; text-transform:uppercase;
    backdrop-filter:blur(4px);
}

[data-testid="stSpinner"] > div { border-top-color: #e50914 !important; }
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def sidebar_nav(active_page: str = ""):
    with st.sidebar:
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
        st.markdown(
            '<p style="font-size:10px;color:#4a5568;font-weight:700;'
            'letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">Navigation</p>',
            unsafe_allow_html=True,
        )
        st.page_link("app.py",                      label="🏠  Home")
        st.page_link("pages/1_Recommend_Movies.py", label="🎯  Recommendations")
        st.page_link("pages/2_Explore_Movies.py",   label="🔍  Discover Movies")
        st.page_link("pages/5_Web_Series.py",       label="📺  Web Series")
        st.page_link("pages/4_Watchlist.py",        label="❤️  My Watchlist")
        st.page_link("pages/3_About_Project.py",    label="📖  About CineMatch")

        st.markdown("<hr style='border:none;border-top:1px solid #1e2a3a;margin:16px 0;'>",
                    unsafe_allow_html=True)
        wl    = st.session_state.get("watchlist", [])
        count = len(wl)
        bc    = "#e50914" if count > 0 else "#4a5568"
        st.markdown(
            f"""
            <div style="background:#12121a;border:1px solid #1e2a3a;border-radius:10px;
                        padding:12px 14px;display:flex;align-items:center;gap:10px;">
              <span style="font-size:18px;">❤️</span>
              <div>
                <div style="font-size:12px;font-weight:700;color:#f1f1f1;">My Watchlist</div>
                <div style="font-size:11px;color:{bc};font-weight:600;">
                  {count} movie{'s' if count!=1 else ''} saved
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section_header(title: str, subtitle: str = ""):
    sub = f'<div style="font-size:13px;color:#8892a4;margin-top:2px;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
          <div style="width:4px;height:22px;background:linear-gradient(180deg,#e50914,#7c3aed);
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
    Render a complete poster card inside a Streamlit column.

    Uses st.image() for the actual poster (the only reliable way to show
    arbitrary image URLs in Streamlit without them being stripped) and
    st.markdown() for the overlay badge + footer metadata.

    Call this instead of st.markdown(poster_card_html(...)).
    """
    genre_parts = [g.strip() for g in genres.replace("|", ",").split(",") if g.strip()]
    genre_text  = "  ·  ".join(genre_parts[:2]) if genre_parts else ""

    # Build the top badge HTML (shown ABOVE the image via markdown)
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
    # Clean title for display: strip the year suffix "(1995)" from footer text
    import re as _re
    display_title = _re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    with col:
        # ── top badge row ─────────────────────────────────────────────
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

        # ── poster image via st.image (never stripped by Streamlit) ───
        try:
            st.image(poster_url, use_container_width=True)
        except Exception:
            # Data-URI SVG placeholders also work via st.image
            from utils.tmdb import placeholder_img_url as _ph
            st.image(_ph(genres, title), use_container_width=True)

        # ── footer: title + meta ──────────────────────────────────────
        rating_html = (
            f'<span style="color:#fbbf24;font-size:11px;font-weight:700;">⭐ {rating}</span>'
            if rating else ""
        )
        year_html = (
            f'<span style="color:#94a3b8;font-size:11px;">{year}</span>'
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
    Legacy shim kept for backward compatibility with tests.
    New code should call render_poster_card() directly.

    Returns a self-contained HTML card that works when Streamlit's
    iframe security allows data: URIs (placeholders always work;
    https:// TMDB URLs require render_poster_card for reliability).
    """
    import re as _re
    genre_parts   = [g.strip() for g in genres.replace("|", ",").split(",") if g.strip()]
    genre_text    = "  ·  ".join(genre_parts[:2]) if genre_parts else ""
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
  <div class="poster-overlay"></div>
  <div class="poster-info">
    <div class="poster-title" title="{safe_title}">{display_title}</div>
    <div class="poster-meta">
      {year_html}
      {rating_html}
    </div>
  </div>
</div>"""


def empty_state(icon: str, title: str, desc: str):
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
    icons = {"info": "ℹ️", "success": "✅", "error": "⚠️"}
    cls   = {"info": "info", "success": "success", "error": ""}.get(kind, "")
    st.markdown(
        f'<div class="cm-toast {cls}">{icons.get(kind,"ℹ️")} {message}</div>',
        unsafe_allow_html=True,
    )


def extract_year(title: str) -> str:
    import re
    m = re.search(r"\((\d{4})\)\s*$", title)
    return m.group(1) if m else ""


def strip_year(title: str) -> str:
    import re
    return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()


# Keep old movie_card_html as thin wrapper around poster_card_html
# so existing tests that call it still work.
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
    from utils.tmdb import placeholder_img_url
    poster = placeholder_img_url(genres, title)
    return poster_card_html(
        title=title, poster_url=poster, genres=genres,
        year=year, rating=rating,
        similarity_pct=similarity_pct, rank=rank,
    )