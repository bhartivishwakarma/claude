"""
SentinelAI Theme — Dark military-grade intelligence aesthetic
"""

import streamlit as st

def apply_theme():
    """Apply the SentinelAI dark theme with custom CSS."""
    st.markdown("""
    <style>
    /* ── FONTS ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:ital,wght@0,100..900;1,100..900&display=swap');

    /* ── ROOT VARIABLES ────────────────────────────────────── */
    :root {
        --bg-primary:    #050a0f;
        --bg-secondary:  #0a1520;
        --bg-card:       #0d1e2e;
        --bg-card-hover: #112233;
        --border:        #1a3a5c;
        --border-glow:   #00c8ff44;
        --accent-cyan:   #00c8ff;
        --accent-teal:   #00ffa3;
        --accent-amber:  #ffb300;
        --accent-red:    #ff3b5c;
        --accent-purple: #9b59b6;
        --text-primary:  #e8f4ff;
        --text-secondary:#8ab0cc;
        --text-dim:      #4a7090;
        --font-mono:     'Share Tech Mono', monospace;
        --font-display:  'Rajdhani', sans-serif;
        --font-body:     'Exo 2', sans-serif;
    }

    /* ── BASE ──────────────────────────────────────────────── */
    html, body, [class*="css"] {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
    }

    .main .block-container {
        background-color: var(--bg-primary);
        padding: 1.5rem 2rem;
        max-width: 100%;
    }

    /* ── SIDEBAR ───────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060d16 0%, #0a1520 100%) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] * {
        font-family: var(--font-display) !important;
    }

    /* ── HEADERS ───────────────────────────────────────────── */
    h1, h2, h3, h4, h5 {
        font-family: var(--font-display) !important;
        letter-spacing: 0.05em;
        color: var(--text-primary) !important;
    }

    /* ── METRICS / KPI CARDS ───────────────────────────────── */
    [data-testid="metric-container"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 0 20px rgba(0,200,255,0.05) !important;
        transition: box-shadow 0.3s ease;
    }

    [data-testid="metric-container"]:hover {
        box-shadow: 0 0 30px rgba(0,200,255,0.12) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--font-mono) !important;
        color: var(--accent-cyan) !important;
        font-size: 2rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-family: var(--font-display) !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }

    /* ── BUTTONS ───────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #0a2a3a, #0d3550) !important;
        color: var(--accent-cyan) !important;
        border: 1px solid var(--accent-cyan) !important;
        border-radius: 4px !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0d3550, #0f4060) !important;
        box-shadow: 0 0 20px rgba(0,200,255,0.3) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00c8ff22, #00c8ff44) !important;
        box-shadow: 0 0 15px rgba(0,200,255,0.2) !important;
    }

    /* ── INPUTS ────────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-family: var(--font-mono) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 10px rgba(0,200,255,0.2) !important;
    }

    /* ── TABS ──────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border-bottom: 1px solid var(--border) !important;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-dim) !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        border-radius: 4px 4px 0 0 !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--bg-card) !important;
        color: var(--accent-cyan) !important;
        border-bottom: 2px solid var(--accent-cyan) !important;
    }

    /* ── EXPANDERS ─────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-family: var(--font-display) !important;
    }

    /* ── FILE UPLOADER ─────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 8px !important;
    }

    /* ── DATAFRAMES ────────────────────────────────────────── */
    .stDataFrame {
        border: 1px solid var(--border) !important;
    }

    /* ── ALERTS & INFO BOXES ───────────────────────────────── */
    .stAlert {
        border-radius: 4px !important;
        border-left: 4px solid var(--accent-cyan) !important;
    }

    /* ── SCROLLBARS ────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }

    /* ── CUSTOM COMPONENTS ─────────────────────────────────── */
    .sentinel-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .sentinel-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: var(--accent-cyan);
    }

    .sentinel-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 0 25px rgba(0,200,255,0.08);
    }

    .sentinel-card.risk-critical::before { background: var(--accent-red); }
    .sentinel-card.risk-high::before { background: var(--accent-amber); }
    .sentinel-card.risk-medium::before { background: #ff8c00; }
    .sentinel-card.risk-low::before { background: var(--accent-teal); }

    .risk-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 3px;
        font-family: var(--font-mono);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .risk-critical { background: rgba(255,59,92,0.2); color: #ff3b5c; border: 1px solid #ff3b5c55; }
    .risk-high     { background: rgba(255,179,0,0.2); color: #ffb300; border: 1px solid #ffb30055; }
    .risk-medium   { background: rgba(255,140,0,0.2); color: #ff8c00; border: 1px solid #ff8c0055; }
    .risk-low      { background: rgba(0,255,163,0.2); color: #00ffa3; border: 1px solid #00ffa355; }
    .risk-safe     { background: rgba(0,200,255,0.1); color: #00c8ff; border: 1px solid #00c8ff33; }

    .page-header {
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
    }

    .page-title {
        font-family: var(--font-display);
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        color: var(--text-primary);
        text-transform: uppercase;
    }

    .page-subtitle {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        color: var(--text-dim);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 0.2rem;
    }

    .stat-label {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--text-dim);
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .stat-value {
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent-cyan);
        line-height: 1.1;
    }

    .pulse-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: var(--accent-teal);
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 6px;
    }

    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(0,255,163,0.6); }
        70%  { box-shadow: 0 0 0 8px rgba(0,255,163,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,255,163,0); }
    }

    .threat-row {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-family: var(--font-body);
        transition: border-color 0.2s;
    }

    .threat-row:hover { border-color: var(--accent-cyan); }

    .mono-text {
        font-family: var(--font-mono);
        color: var(--accent-cyan);
        font-size: 0.85rem;
    }

    .section-header {
        font-family: var(--font-display);
        font-size: 0.75rem;
        color: var(--text-dim);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.4rem;
        margin-bottom: 0.8rem;
        margin-top: 1.2rem;
    }

    .copilot-bubble {
        background: linear-gradient(135deg, #0d2a3a, #0a2030);
        border: 1px solid var(--border-glow);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: var(--font-body);
        font-size: 0.9rem;
        line-height: 1.6;
        color: var(--text-primary);
        box-shadow: 0 0 30px rgba(0,200,255,0.06);
    }

    .copilot-label {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        color: var(--accent-cyan);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-teal)) !important;
    }

    /* Radio buttons */
    .stRadio > div { gap: 0.5rem; }
    .stRadio label {
        color: var(--text-secondary) !important;
        font-family: var(--font-display) !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] { color: var(--accent-cyan); }

    /* Checkbox */
    .stCheckbox label { color: var(--text-secondary) !important; font-family: var(--font-display) !important; }

    /* Select */
    [data-baseweb="select"] { background: var(--bg-card) !important; }

    /* Top scanline effect */
    body::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
        animation: scan 4s linear infinite;
        z-index: 9999;
        opacity: 0.6;
        pointer-events: none;
    }

    @keyframes scan {
        0%   { transform: translateX(-100%); }
        100% { transform: translateX(100vw); }
    }
    </style>
    """, unsafe_allow_html=True)
