"""
SentinelAI - Smarter Defence Through Innovation
Main application entry point
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.theme import apply_theme
from ui.sidebar import render_sidebar
from ui.pages.dashboard import render_dashboard
from ui.pages.live_monitoring import render_live_monitoring
from ui.pages.analysis_studio import render_analysis_studio
from ui.pages.threat_intelligence import render_threat_intelligence
from ui.pages.reports import render_reports
from utils.session_state import init_session_state
from utils.logger import get_logger

logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="SentinelAI — Defence Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    # Apply custom theme
    apply_theme()
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar and get current page
    current_page = render_sidebar()
    
    # Route to correct page
    pages = {
        "🏠 Home Dashboard": render_dashboard,
        "📡 Live Monitoring": render_live_monitoring,
        "🔬 Analysis Studio": render_analysis_studio,
        "🗺️ Threat Intelligence": render_threat_intelligence,
        "📊 Reports & Insights": render_reports,
    }
    
    if current_page in pages:
        pages[current_page]()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
