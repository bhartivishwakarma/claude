import streamlit as st
import requests


def render_news_page():
    st.title("📰 Cyber News")
    st.markdown("---")

    api_key = st.session_state.get("NEWS_API_KEY")

    if not api_key:
        st.warning("📌 Add NEWS_API_KEY in Settings to enable live cyber news feed")
        st.info("Get your free API key at https://newsapi.org")
        return

    url = f"https://newsapi.org/v2/everything?q=cybersecurity%20OR%20hacking%20OR%20breach&sortBy=publishedAt&pageSize=6&apiKey={api_key}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            st.error(f"🔴 API Error: {data.get('message', 'Unknown error')}")
            return

        articles = data.get("articles", [])

        if not articles:
            st.info("No cybersecurity news found at this moment")
            return

        st.markdown(f"### Latest {len(articles)} Cybersecurity News Articles")

        for idx, article in enumerate(articles, 1):
            with st.container(border=True):
                st.subheader(f"{idx}. {article['title']}")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Source:** {article['source']['name']}")
                    st.write(f"**Date:** {article['publishedAt'][:10]}")
                with col2:
                    st.link_button("Read Article", article['url'])
                st.write(article['description'])

    except requests.exceptions.Timeout:
        st.error("🔴 Request timeout - NewsAPI unavailable")
    except requests.exceptions.ConnectionError:
        st.error("🔴 Connection error - Check internet connectivity")
    except Exception as e:
        st.error(f"🔴 Failed to load news: {str(e)}")
