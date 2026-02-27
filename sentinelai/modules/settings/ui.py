"""Streamlit UI for runtime settings (API keys).

This UI stores keys only in `st.session_state` via the service layer.
"""
from typing import Optional
import streamlit as st
from .service import save_keys, get_key, is_ai_enabled
import os
from dotenv import load_dotenv

load_dotenv()


def _status_label(exists: bool) -> str:
    """Return a small status label with colored text.

    Uses existing theme-friendly colors.
    """
    if exists:
        return "<span style='color:#00c8ff; font-weight:700;'>✔ Connected</span>"
    return "<span style='color:#ffb300; font-weight:700;'>⚠ Not Provided</span>"


def render_settings() -> None:
    """Render the Settings page where users can enter API keys at runtime.

    Keys are masked, validated for non-empty values, and stored only in
    `st.session_state` using the service functions.
    """
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px;'>
        <div style='font-size:1.6rem;'>⚙️</div>
        <div style='font-family:"Rajdhani",sans-serif; font-size:1.4rem; font-weight:700; color:#00c8ff;'>Settings</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("Configure runtime API keys for external services. Keys are stored only for this session.")

    # Load existing values safely from session state (do not log)
    openai_val = st.session_state.get("openai_api_key", "")
    news_val = st.session_state.get("news_api_key", "")
    youtube_val = st.session_state.get("youtube_api_key", "")

    col1, col2 = st.columns([3, 1])
    with col1:
        openai_input = st.text_input(
            "OpenAI API Key",
            value="",
            placeholder="sk-...",
            type="password",
            help="Enter your OpenAI API key. Kept in session only.",
            label_visibility="visible",
            key="_openai_input_temp",
        )

        news_input = st.text_input(
            "News API Key",
            value="",
            placeholder="news_api_...",
            type="password",
            help="API key for news content providers. Kept in session only.",
            label_visibility="visible",
            key="_news_input_temp",
        )

        youtube_input = st.text_input(
            "YouTube API Key",
            value="",
            placeholder="ya29...",
            type="password",
            help="YouTube Data API key. Kept in session only.",
            label_visibility="visible",
            key="_youtube_input_temp",
        )

    with col2:
        st.markdown("<div style='font-family:\'Share Tech Mono\',monospace; font-size:0.9rem; color:#4a7090; letter-spacing:0.08em; text-transform:uppercase;'>Status</div>", unsafe_allow_html=True)
        st.markdown(_status_label(bool(openai_val)), unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.markdown(_status_label(bool(news_val)), unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.markdown(_status_label(bool(youtube_val)), unsafe_allow_html=True)

    # Actions
    cols = st.columns([1, 1, 2])
    with cols[0]:
        if st.button("Save", use_container_width=True):
            # Only save non-empty inputs; do not overwrite existing keys with blanks
            save_keys(
                openai_input if openai_input and openai_input.strip() else None,
                news_input if news_input and news_input.strip() else None,
                youtube_input if youtube_input and youtube_input.strip() else None,
            )
            st.success("Keys saved to session.")
            # Refresh local view of session values
            st.rerun()

    with cols[1]:
        if st.button("Clear Keys", use_container_width=True):
            for k in ["openai_api_key", "news_api_key", "youtube_api_key"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.info("All keys cleared from session.")
            st.rerun()

    with cols[2]:
        ai_status = "AI Enabled" if is_ai_enabled() else "AI Disabled"
        color = "#00c8ff" if is_ai_enabled() else "#ffb300"
        st.markdown(f"<div style='text-align:right; font-weight:700; color:{color};'>{ai_status}</div>", unsafe_allow_html=True)

    # Provide a minimal explanation without exposing keys
    st.markdown("""
    <div style='margin-top:0.6rem; font-size:0.85rem; color:#8ab0cc;'>
    Keys are masked in the UI and stored only in memory for this Streamlit session. They are not written to
    disk or logs. Other modules can access keys via `modules.settings.service.get_key()`.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### API Configuration")

    openai_key = st.text_input(
        "OpenAI API Key",
        value=st.session_state.get("OPENAI_API_KEY", ""),
        type="password",
        placeholder="sk-proj-...",
    )
    if openai_key:
        st.session_state.OPENAI_API_KEY = openai_key

    news_key = st.text_input(
        "NewsAPI Key",
        value=st.session_state.get("NEWS_API_KEY", ""),
        type="password",
        placeholder="your_newsapi_key_here",
    )
    if news_key:
        st.session_state.NEWS_API_KEY = news_key

    st.markdown("---")
    st.markdown("### Privacy Controls")

    st.session_state.local_mode = st.toggle(
        "Local Processing Mode",
        value=st.session_state.get("local_mode", True),
        help="Process data locally without external API calls",
    )

    st.session_state.anonymize = st.toggle(
        "Data Anonymization",
        value=st.session_state.get("anonymize", True),
        help="Automatically anonymize PII in analyzed content",
    )

    st.session_state.temp_only = st.toggle(
        "Temporary Memory Only",
        value=st.session_state.get("temp_only", True),
        help="No persistent storage of analyzed content",
    )

    st.markdown("---")
    st.markdown("### AI Provider")

    st.session_state.ai_provider = st.selectbox(
        "Provider",
        ["Claude (Anthropic)", "Local Models", "OpenAI"],
        index=0,
        label_visibility="collapsed",
    )

    if st.session_state.ai_provider == "Claude (Anthropic)":
        anthropic_key = st.text_input(
            "Anthropic API Key",
            value=st.session_state.get("anthropic_api_key", ""),
            type="password",
            placeholder="sk-ant-...",
            label_visibility="visible",
        )
        if anthropic_key:
            st.session_state.anthropic_api_key = anthropic_key

    st.markdown("---")
    st.success("✅ Settings saved to session")
