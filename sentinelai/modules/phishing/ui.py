import streamlit as st
import re
from urllib.parse import urlparse


def check_url(url: str):
    score = 0
    reasons = []

    if not url.startswith("https"):
        score += 1
        reasons.append("Not HTTPS")

    domain = urlparse(url).netloc

    if re.search(r"\d+\.\d+\.\d+\.\d+", domain):
        score += 2
        reasons.append("IP address in domain")

    suspicious_words = ["login", "verify", "bank", "secure", "update", "password"]
    if any(w in url.lower() for w in suspicious_words):
        score += 1
        reasons.append("Suspicious keywords detected")

    if len(domain) > 30:
        score += 1
        reasons.append("Very long domain name")

    return score, reasons


def render_phishing_page():
    st.title("🎣 Phishing Detection")
    st.markdown("---")

    url = st.text_input("Enter URL to analyze", placeholder="https://example.com")

    if st.button("Analyze URL", use_container_width=True):
        if not url:
            st.warning("Please enter a URL")
            return

        score, reasons = check_url(url)

        st.markdown("### Detection Result")

        if score == 0:
            st.success("✅ **Safe** - No phishing indicators detected")
        elif score <= 2:
            st.warning("⚠️ **Suspicious** - Some risk factors present")
        else:
            st.error("🚨 **High Risk** - Multiple phishing indicators")

        if reasons:
            st.markdown("**Risk Factors:**")
            for reason in reasons:
                st.write(f"• {reason}")

        st.info(f"Risk Score: {score}/6")
