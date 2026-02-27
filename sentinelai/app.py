"""
SentinelAI - Smarter Defence Through Innovation
Main application entry point
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def safe_page(import_path, func_name, label):
    try:
        module = __import__(import_path, fromlist=[func_name])
        return getattr(module, func_name)
    except Exception:
        def placeholder():
            st.title(label)
            st.warning("Module not installed yet — safe fallback active")
        return placeholder


# ===== UI CORE =====
from ui.theme import apply_theme
from ui.sidebar import render_sidebar

from ui.pages.dashboard import render_dashboard
from ui.pages.live_monitoring import render_live_monitoring
from ui.pages.analysis_studio import render_analysis_studio
from ui.pages.threat_intelligence import render_threat_intelligence
from ui.pages.reports import render_reports

# ===== OPTIONAL MODULES (SAFE IMPORTS) =====
render_settings = safe_page(
    "modules.settings.ui",
    "render_settings",
    "Settings"
)

render_phishing_page = safe_page(
    "modules.phishing.ui",
    "render_phishing_page",
    "Phishing Detection"
)

render_awareness_page = safe_page(
    "modules.awareness.ui",
    "render_awareness_page",
    "Security Awareness"
)

render_news_page = safe_page(
    "modules.news.ui",
    "render_news_page",
    "Cyber News"
)

render_password_page = safe_page(
    "modules.password.ui",
    "render_password_page",
    "Password Analyzer"
)

render_alerts_page = safe_page(
    "modules.alerts.ui",
    "render_alerts_page",
    "Fraud Alerts"
)

render_threat_analysis_page = safe_page(
    "modules.threat.ui",
    "render_threat_analysis_page",
    "Threat Analysis"
)

# ===== UTILS =====
from utils.session_state import init_session_state
from utils.logger import get_logger

logger = get_logger(__name__)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="SentinelAI — Defence Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():

    # Apply theme
    apply_theme()

    # Init session
    init_session_state()

    # Sidebar navigation
    current_page = render_sidebar()

    # ===== ROUTING =====
    # ===== ROUTING =====
    if current_page == "🏠 Home Dashboard":
        render_dashboard()

    elif current_page == "📡 Live Monitoring":
        render_live_monitoring()

    elif current_page == "🧪 Analysis Studio":
        render_analysis_studio()

    elif current_page == "📖 Threat Intelligence":
        render_threat_intelligence()

    elif current_page == "📊 Reports & Insights":
        render_reports()

    elif current_page == "🛡 Phishing Detection":
        render_phishing_page()

    elif current_page == "🎥 Security Awareness":
        render_awareness_page()

    elif current_page == "📰 Cyber News":
        render_news_page()

    elif current_page == "🔑 Password Analyzer":
        render_password_page()

    elif current_page == "🚨 Fraud Alerts":
        render_alerts_page()

    elif current_page == "🧠 Threat Analysis":
        render_threat_analysis_page()

    elif current_page == "⚙️ Settings":
        render_settings()

    else:
        render_dashboard()


if __name__ == "__main__":
    main()