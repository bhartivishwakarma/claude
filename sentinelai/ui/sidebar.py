"""
Sidebar navigation for SentinelAI
"""

import streamlit as st
from datetime import datetime


def render_sidebar():
    """Render the sidebar navigation and return the selected page."""
    with st.sidebar:
        # Logo / Branding
        st.markdown("""
        <div style="text-align:center; padding: 1.5rem 0 1rem;">
            <div style="font-size:2.5rem; margin-bottom:0.2rem;">🛡️</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                        letter-spacing:0.15em; color:#00c8ff; text-transform:uppercase;">
                SentinelAI
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem;
                        color:#4a7090; letter-spacing:0.25em; text-transform:uppercase; margin-top:2px;">
                Defence Intelligence v2.0
            </div>
        </div>
        <hr style="border:none; border-top:1px solid #1a3a5c; margin: 0.5rem 0 1rem;"/>
        """, unsafe_allow_html=True)

        # System status
        now = datetime.now().strftime("%H:%M:%S UTC")
        threat_level = st.session_state.get("threat_level", "MODERATE")
        threat_colors = {
            "LOW": "#00ffa3", "MODERATE": "#ffb300",
            "HIGH": "#ff8c00", "CRITICAL": "#ff3b5c"
        }
        color = threat_colors.get(threat_level, "#ffb300")

        st.markdown(f"""
        <div style="background:#0d1e2e; border:1px solid #1a3a5c; border-radius:6px;
                    padding:0.7rem 0.9rem; margin-bottom:1rem;">
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem;
                        color:#4a7090; letter-spacing:0.2em; text-transform:uppercase;">System Status</div>
            <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
                <span style="width:8px;height:8px;border-radius:50%;background:#00ffa3;
                             display:inline-block;box-shadow:0 0 6px #00ffa3;"></span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.72rem; color:#00ffa3;">ONLINE</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;">THREAT LVL:</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:{color}; font-weight:700;">{threat_level}</span>
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.58rem; color:#2a4a5c; margin-top:4px;">{now}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace; font-size:0.6rem; color:#4a7090; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.4rem;">Navigation</div>', unsafe_allow_html=True)

        pages = [
            "🏠 Home Dashboard",
            "📡 Live Monitoring",
            "🧪 Analysis Studio",
            "📖 Threat Intelligence",
            "📊 Reports & Insights",
            "🛡 Phishing Detection",
            "🎥 Security Awareness",
            "📰 Cyber News",
            "🔑 Password Analyzer",
            "🚨 Fraud Alerts",
            "🧠 Threat Analysis",
            "⚙️ Settings"
        ]

        if "current_page" not in st.session_state:
            st.session_state.current_page = pages[0]

        for page in pages:
            is_active = st.session_state.current_page == page
            btn_style = "background: rgba(0,200,255,0.12) !important; border-color: #00c8ff !important;" if is_active else ""
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

        st.markdown('<hr style="border:none; border-top:1px solid #1a3a5c; margin: 1rem 0;"/>', unsafe_allow_html=True)

        # Privacy controls
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace; font-size:0.6rem; color:#4a7090; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.5rem;">Privacy Controls</div>', unsafe_allow_html=True)

        st.session_state.local_mode = st.toggle(
            "Local Processing Mode",
            value=st.session_state.get("local_mode", True),
            help="Process data locally without external API calls"
        )
        st.session_state.anonymize = st.toggle(
            "Data Anonymization",
            value=st.session_state.get("anonymize", True),
            help="Automatically anonymize PII in analyzed content"
        )
        st.session_state.temp_only = st.toggle(
            "Temporary Memory Only",
            value=st.session_state.get("temp_only", True),
            help="No persistent storage of analyzed content"
        )

        st.markdown('<hr style="border:none; border-top:1px solid #1a3a5c; margin: 1rem 0;"/>', unsafe_allow_html=True)

        # AI Provider selector
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace; font-size:0.6rem; color:#4a7090; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.5rem;">AI Provider</div>', unsafe_allow_html=True)
        st.session_state.ai_provider = st.selectbox(
            "Provider",
            ["Claude (Anthropic)", "Local Models", "OpenAI"],
            index=0,
            label_visibility="collapsed"
        )

        # API key input
        if st.session_state.ai_provider == "Claude (Anthropic)":
            api_key = st.text_input(
                "Anthropic API Key",
                type="password",
                placeholder="sk-ant-...",
                value=st.session_state.get("anthropic_api_key", ""),
                label_visibility="visible"
            )
            if api_key:
                st.session_state.anthropic_api_key = api_key

        st.markdown('<hr style="border:none; border-top:1px solid #1a3a5c; margin: 1rem 0;"/>', unsafe_allow_html=True)

        # Stats summary
        stats = st.session_state.get("global_stats", {})
        analyzed = stats.get("total_analyzed", 0)
        threats = stats.get("threats_detected", 0)

        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.5rem;">Session Stats</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#8ab0cc;">Analyzed</span>
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#00c8ff;">{analyzed}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#8ab0cc;">Threats Found</span>
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#ff3b5c;">{threats}</span>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.current_page