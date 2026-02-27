"""Service layer for session-only API key storage and retrieval.

This module stores keys only in `st.session_state`. No keys are written
to disk or logs. Other modules may import `get_key` and `is_ai_enabled`.
"""
from typing import Optional
import streamlit as st


def save_keys(openai: Optional[str], news: Optional[str], youtube: Optional[str]) -> None:
    """Save provided API keys into session state.

    Only non-empty values are stored. Keys are stored under the following
    session keys: `openai_api_key`, `news_api_key`, `youtube_api_key`.
    This function never logs or prints keys.

    Args:
        openai: OpenAI API key or None/empty to skip.
        news: News API key or None/empty to skip.
        youtube: YouTube API key or None/empty to skip.
    """
    if openai and openai.strip():
        st.session_state["openai_api_key"] = openai.strip()
    if news and news.strip():
        st.session_state["news_api_key"] = news.strip()
    if youtube and youtube.strip():
        st.session_state["youtube_api_key"] = youtube.strip()


def get_key(service_name: str) -> Optional[str]:
    """Retrieve the raw API key for a given service from session state.

    Args:
        service_name: one of 'openai', 'news', 'youtube' (case-insensitive).

    Returns:
        The API key string or None if not present.
    """
    name = service_name.strip().lower()
    mapping = {
        "openai": "openai_api_key",
        "news": "news_api_key",
        "youtube": "youtube_api_key",
    }
    key = mapping.get(name)
    if not key:
        return None
    return st.session_state.get(key)


def is_ai_enabled() -> bool:
    """Return True if an OpenAI key is present in session state.

    AI is considered enabled when `openai_api_key` exists and is non-empty.
    """
    return bool(st.session_state.get("openai_api_key"))
