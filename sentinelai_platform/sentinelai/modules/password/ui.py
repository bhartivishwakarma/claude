"""Streamlit UI for password strength analysis page.

This page never stores the entered password in session state or logs.
All computation is transient and performed in-memory only.
"""
import streamlit as st
import math
import string

def entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32

    if pool == 0:
        return 0

    return len(password) * math.log2(pool)


def get_strength_level(entropy_bits):
    if entropy_bits < 40:
        return "Weak", "error"
    elif entropy_bits < 60:
        return "Medium", "warning"
    else:
        return "Strong", "success"


def render_password_page():
    st.title("🔐 Password Analyzer")
    st.markdown("---")

    pwd = st.text_input("Enter password to analyze", type="password", placeholder="Your password here")

    if pwd:
        e = entropy(pwd)
        strength, status = get_strength_level(e)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Entropy", f"{round(e, 1)} bits")
        with col2:
            st.metric("Length", len(pwd))
        with col3:
            st.metric("Charset Types", pool_count(pwd))

        st.markdown("### Strength Assessment")

        if status == "error":
            st.error(f"🔴 **{strength}** - Too predictable, easy to crack")
        elif status == "warning":
            st.warning(f"🟡 **{strength}** - Acceptable but could be stronger")
        else:
            st.success(f"🟢 **{strength}** - Excellent entropy and resistance")

        st.info(f"Character pool: {charset_info(pwd)}")


def pool_count(password):
    count = 0
    if any(c.islower() for c in password):
        count += 1
    if any(c.isupper() for c in password):
        count += 1
    if any(c.isdigit() for c in password):
        count += 1
    if any(c in string.punctuation for c in password):
        count += 1
    return count


def charset_info(password):
    charsets = []
    if any(c.islower() for c in password):
        charsets.append("Lowercase")
    if any(c.isupper() for c in password):
        charsets.append("Uppercase")
    if any(c.isdigit() for c in password):
        charsets.append("Numbers")
    if any(c in string.punctuation for c in password):
        charsets.append("Symbols")
    return ", ".join(charsets)
