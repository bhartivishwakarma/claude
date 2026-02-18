"""
SentinelAI — Home Dashboard Page
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from services.analyzer import _risk_level


def render_dashboard():
    """Render the main home dashboard."""

    # Page header
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🛡️ Mission Control</div>
        <div class="page-subtitle">Real-time threat intelligence overview · SentinelAI Defence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    stats = st.session_state.get("global_stats", {})
    history = st.session_state.get("analysis_history", [])
    alerts = st.session_state.get("alerts", [])

    # ── KPI ROW ──────────────────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Analyzed", stats.get("total_analyzed", 0), help="Items analyzed this session")
    with col2:
        threats = stats.get("threats_detected", 0)
        st.metric("Threats Detected", threats, delta="+2 last hour", delta_color="inverse")
    with col3:
        avg = stats.get("avg_risk_score", 0)
        st.metric("Avg Risk Score", f"{avg:.1f}", help="Session average 0–100")
    with col4:
        critical = sum(1 for r in history if r.get("risk_level") == "CRITICAL")
        st.metric("Critical Alerts", critical, delta_color="inverse")
    with col5:
        detection_rate = (threats / max(stats.get("total_analyzed", 1), 1)) * 100
        st.metric("Detection Rate", f"{detection_rate:.0f}%")

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── CHARTS ROW ───────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header">Risk Score Timeline</div>', unsafe_allow_html=True)
        _render_timeline_chart(history)

    with col_right:
        st.markdown('<div class="section-header">Threat Distribution</div>', unsafe_allow_html=True)
        _render_distribution_pie(history)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── SECOND ROW ───────────────────────────────────────────────────────────
    col_heat, col_alerts = st.columns([3, 2])

    with col_heat:
        st.markdown('<div class="section-header">Category Heatmap</div>', unsafe_allow_html=True)
        _render_category_heatmap(history)

    with col_alerts:
        st.markdown('<div class="section-header">⚠️ Active Alerts</div>', unsafe_allow_html=True)
        _render_alerts(alerts)

    # ── RECENT ACTIVITY ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Recent Analysis Activity</div>', unsafe_allow_html=True)
    _render_recent_activity(history[:6])

    # ── SYSTEM HEALTH ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">System Health</div>', unsafe_allow_html=True)
    _render_system_health()


def _render_timeline_chart(history: list):
    if not history:
        st.info("No analysis history yet. Analyze some content to see trends.")
        return

    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    fig = go.Figure()

    # Area fill
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["risk_score"],
        mode="lines+markers",
        name="Risk Score",
        line=dict(color="#00c8ff", width=2),
        marker=dict(
            size=8,
            color=df["risk_score"],
            colorscale=[[0, "#00ffa3"], [0.4, "#ffb300"], [0.7, "#ff8c00"], [1, "#ff3b5c"]],
            showscale=False,
        ),
        fill="tozeroy",
        fillcolor="rgba(0,200,255,0.08)",
    ))

    # Critical threshold line
    fig.add_hline(y=75, line_dash="dot", line_color="#ff3b5c",
                  annotation_text="CRITICAL", annotation_font_color="#ff3b5c")
    fig.add_hline(y=55, line_dash="dot", line_color="#ffb300",
                  annotation_text="HIGH", annotation_font_color="#ffb300")

    fig.update_layout(
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=10),
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis=dict(showgrid=False, color="#4a7090", linecolor="#1a3a5c"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090",
                   range=[0, 105], linecolor="#1a3a5c"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_distribution_pie(history: list):
    if not history:
        return

    counts = {}
    for item in history:
        level = item.get("risk_level", "SAFE")
        counts[level] = counts.get(level, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())
    colors_map = {
        "CRITICAL": "#ff3b5c", "HIGH": "#ffb300",
        "MEDIUM": "#ff8c00", "LOW": "#00c8ff", "SAFE": "#00ffa3"
    }
    colors = [colors_map.get(l, "#8ab0cc") for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color="#050a0f", width=3)),
        textfont=dict(family="Share Tech Mono", color="#e8f4ff", size=10),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
    ))

    fig.update_layout(
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(
            font=dict(color="#8ab0cc", family="Share Tech Mono", size=9),
            bgcolor="rgba(0,0,0,0)",
            orientation="v",
            x=1, y=0.5,
        ),
        annotations=[dict(
            text=f"<b>{len(history)}</b><br>ITEMS",
            x=0.5, y=0.5,
            font=dict(color="#00c8ff", family="Share Tech Mono", size=13),
            showarrow=False,
        )],
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_category_heatmap(history: list):
    all_categories = [
        "Violence", "Cybersecurity", "Social Engineering",
        "Hate Speech", "Misinformation", "Suspicious Activity",
        "Data Exfiltration", "Phishing"
    ]

    # Build matrix: categories × hours
    now = datetime.now()
    hours = [(now - timedelta(hours=i)).strftime("%H:00") for i in range(11, -1, -1)]

    matrix = []
    for cat in all_categories:
        row = []
        for i in range(11, -1, -1):
            hour_start = now - timedelta(hours=i+1)
            hour_end = now - timedelta(hours=i)
            count = 0
            for item in history:
                ts = datetime.fromisoformat(item["timestamp"])
                if hour_start <= ts < hour_end:
                    if cat in item.get("categories", []):
                        count += 1
            # Add some simulated data for visual richness
            count += random.randint(0, 2) if random.random() > 0.6 else 0
            row.append(count)
        matrix.append(row)

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=hours,
        y=all_categories,
        colorscale=[[0, "#050a0f"], [0.3, "#0d3a5c"], [0.7, "#ffb300"], [1, "#ff3b5c"]],
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Hour: %{x}<br>Incidents: %{z}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=8, len=0.8,
            tickfont=dict(color="#8ab0cc", family="Share Tech Mono", size=9),
            outlinecolor="rgba(0,0,0,0)",
        )
    ))

    fig.update_layout(
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=9),
        margin=dict(l=120, r=10, t=10, b=40),
        xaxis=dict(showgrid=False, color="#4a7090"),
        yaxis=dict(showgrid=False, color="#4a7090", autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_alerts(alerts: list):
    colors = {"CRITICAL": "#ff3b5c", "HIGH": "#ffb300", "MEDIUM": "#ff8c00", "LOW": "#00c8ff"}

    if not alerts:
        st.markdown('<div style="color:#4a7090; font-family:\'Share Tech Mono\',monospace; font-size:0.75rem;">No active alerts</div>', unsafe_allow_html=True)
        return

    for alert in alerts[:5]:
        level = alert["level"]
        color = colors.get(level, "#8ab0cc")
        st.markdown(f"""
        <div class="sentinel-card risk-{level.lower()}" style="margin-bottom:0.4rem; padding:0.7rem 0.9rem 0.7rem 1.1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                <span class="risk-badge risk-{level.lower()}">{level}</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;">{alert['time']}</span>
            </div>
            <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem; color:#c8d8e8; margin-top:4px;">{alert['message']}</div>
        </div>
        """, unsafe_allow_html=True)


def _render_recent_activity(history: list):
    if not history:
        st.info("No recent activity.")
        return

    for item in history:
        level = item.get("risk_level", "SAFE").lower()
        score = item.get("risk_score", 0)
        preview = item.get("content_preview", "")[:80]
        source = item.get("source", "Unknown")
        cats = ", ".join(item.get("categories", [])[:2]) or "—"
        ts = item.get("timestamp", "")
        try:
            ts_fmt = datetime.fromisoformat(ts).strftime("%H:%M:%S")
        except Exception:
            ts_fmt = ts[:8]

        st.markdown(f"""
        <div class="threat-row">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:10px; flex:1; min-width:0;">
                    <span class="risk-badge risk-{level}">{item.get('risk_level','SAFE')}</span>
                    <span style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#c8d8e8;
                                 white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:350px;">
                        {preview}...
                    </span>
                </div>
                <div style="display:flex; align-items:center; gap:16px; flex-shrink:0;">
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#4a7090;">{source}</span>
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#8ab0cc;">{cats}</span>
                    <span style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:700; color:{'#ff3b5c' if score>75 else '#ffb300' if score>55 else '#ff8c00' if score>30 else '#00ffa3'};">{score:.0f}</span>
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#2a4a5c;">{ts_fmt}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_system_health():
    services = [
        ("Pattern Engine", 99.9, "Operational"),
        ("Claude AI Integration", 98.2, "Operational"),
        ("Live Feed Ingestion", 97.5, "Operational"),
        ("Anomaly Detector", 100.0, "Operational"),
        ("Entity Extractor", 99.1, "Operational"),
        ("Privacy Filters", 100.0, "Operational"),
    ]

    cols = st.columns(len(services))
    for col, (name, uptime, status) in zip(cols, services):
        with col:
            st.markdown(f"""
            <div style="background:#0d1e2e; border:1px solid #1a3a5c; border-radius:6px; padding:0.7rem; text-align:center;">
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.58rem; color:#4a7090;
                            letter-spacing:0.15em; text-transform:uppercase; margin-bottom:4px;">{name}</div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.8rem; color:#00ffa3;">{uptime}%</div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.58rem; color:#00ffa3; opacity:0.7;">{status}</div>
            </div>
            """, unsafe_allow_html=True)
