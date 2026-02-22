import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_alerts_page():
    st.title("🚨 Fraud Alerts")
    st.markdown("---")

    alert_types = ["Login attempt", "Suspicious IP", "Multiple failures", "New device", "Data export"]
    severities = ["Low", "Medium", "High", "Medium", "Low"]

    now = datetime.now()
    timestamps = [now - timedelta(minutes=i) for i in range(5)]

    alerts_data = {
        "Timestamp": [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps],
        "Alert Type": alert_types,
        "Severity": severities,
        "IP Address": ["192.168.1.100", "203.0.113.45", "198.51.100.12", "192.168.1.100", "203.0.113.78"],
        "Details": [
            "From USA region",
            "From Russia (unusual)",
            "5 failed attempts",
            "macOS device",
            "1.2GB exported",
        ],
    }

    df = pd.DataFrame(alerts_data)

    st.markdown("### Recent Security Alerts")
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High", len(df[df["Severity"] == "High"]))
    with col2:
        st.metric("🟡 Medium", len(df[df["Severity"] == "Medium"]))
    with col3:
        st.metric("🟢 Low", len(df[df["Severity"] == "Low"]))

    st.success("Module loaded successfully")
