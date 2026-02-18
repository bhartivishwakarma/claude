"""
SentinelAI — Live Monitoring Page
"""

import streamlit as st
import time
import random
from datetime import datetime
from services.analyzer import generate_live_feed_item, analyze_text


def render_live_monitoring():
    """Render the live monitoring dashboard."""

    st.markdown("""
    <div class="page-header">
        <div class="page-title">📡 Live Monitoring</div>
        <div class="page-subtitle">Real-time threat detection stream · Auto-refresh enabled</div>
    </div>
    """, unsafe_allow_html=True)

    # ── CONTROLS ─────────────────────────────────────────────────────────────
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1, 1, 1, 2])

    with col_ctrl1:
        monitoring_active = st.session_state.get("monitoring_active", False)
        if st.button(
            "⏹ Stop Monitoring" if monitoring_active else "▶ Start Monitoring",
            type="primary" if not monitoring_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.monitoring_active = not monitoring_active
            st.rerun()

    with col_ctrl2:
        if st.button("🗑 Clear Feed", use_container_width=True):
            st.session_state.live_feed = []
            st.rerun()

    with col_ctrl3:
        refresh_rate = st.selectbox(
            "Refresh Rate",
            ["2s", "5s", "10s", "30s"],
            index=1,
            label_visibility="collapsed"
        )

    with col_ctrl4:
        filter_level = st.multiselect(
            "Filter by Risk Level",
            ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"],
            default=["CRITICAL", "HIGH", "MEDIUM"],
            label_visibility="collapsed",
        )

    # Status bar
    is_active = st.session_state.get("monitoring_active", False)
    status_color = "#00ffa3" if is_active else "#4a7090"
    status_text = "MONITORING ACTIVE" if is_active else "MONITORING STOPPED"

    st.markdown(f"""
    <div style="background:#0a1520; border:1px solid #1a3a5c; border-radius:6px;
                padding:0.6rem 1rem; margin:0.5rem 0; display:flex; align-items:center; gap:10px;">
        <span style="width:8px;height:8px;border-radius:50%;background:{status_color};
                     display:inline-block; {'animation:pulse 1.5s infinite;' if is_active else ''}"></span>
        <span style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:{status_color};
                     letter-spacing:0.15em;">{status_text}</span>
        <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090; margin-left:auto;">
            FEED SIZE: {len(st.session_state.get('live_feed', []))} ITEMS
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── LIVE FEED SIMULATION ──────────────────────────────────────────────────
    if is_active:
        # Add new items to the feed
        num_new = random.randint(1, 3)
        for _ in range(num_new):
            item = generate_live_feed_item()
            if "live_feed" not in st.session_state:
                st.session_state.live_feed = []
            st.session_state.live_feed.insert(0, item)

            # Update global stats
            stats = st.session_state.get("global_stats", {})
            stats["total_analyzed"] = stats.get("total_analyzed", 0) + 1
            if item["flagged"]:
                stats["threats_detected"] = stats.get("threats_detected", 0) + 1
                # Also add critical alerts
                if item["risk_level"] in ("CRITICAL", "HIGH"):
                    new_alert = {
                        "level": item["risk_level"],
                        "message": f"Live feed threat: {item['content_preview'][:60]}...",
                        "time": "just now"
                    }
                    alerts = st.session_state.get("alerts", [])
                    alerts.insert(0, new_alert)
                    st.session_state.alerts = alerts[:10]

            # Update threat level
            if item["risk_level"] == "CRITICAL":
                st.session_state.threat_level = "CRITICAL"
            elif item["risk_level"] == "HIGH" and st.session_state.get("threat_level") != "CRITICAL":
                st.session_state.threat_level = "HIGH"

            st.session_state.global_stats = stats

        # Keep feed bounded
        if len(st.session_state.live_feed) > 100:
            st.session_state.live_feed = st.session_state.live_feed[:100]

    # ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────────
    col_feed, col_detail = st.columns([3, 2])

    feed = st.session_state.get("live_feed", [])
    filtered_feed = [i for i in feed if not filter_level or i["risk_level"] in filter_level]

    with col_feed:
        st.markdown('<div class="section-header">Live Feed Stream</div>', unsafe_allow_html=True)

        if not filtered_feed:
            st.markdown("""
            <div style="text-align:center; color:#4a7090; font-family:'Share Tech Mono',monospace;
                        font-size:0.75rem; padding:2rem; border:1px dashed #1a3a5c; border-radius:8px;">
                No feed items match current filters.<br>Start monitoring or adjust filters above.
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in filtered_feed[:20]:
                _render_feed_item(item)

    with col_detail:
        st.markdown('<div class="section-header">Stream Analytics</div>', unsafe_allow_html=True)
        _render_stream_analytics(filtered_feed)

        st.markdown('<div class="section-header">Quick Analyze</div>', unsafe_allow_html=True)
        _render_quick_analyze()

    # Auto-refresh
    if is_active:
        rate_map = {"2s": 2, "5s": 5, "10s": 10, "30s": 30}
        wait_s = rate_map.get(refresh_rate, 5)
        time.sleep(wait_s)
        st.rerun()


def _render_feed_item(item: dict):
    level = item.get("risk_level", "SAFE").lower()
    score = item.get("risk_score", 0)
    preview = item.get("content_preview", "")[:100]
    source = item.get("source", "Unknown")
    cats = ", ".join(item.get("categories", [])[:2]) or "Clean"
    flagged = item.get("flagged", False)
    ts = item.get("timestamp", "")
    try:
        ts_fmt = datetime.fromisoformat(ts).strftime("%H:%M:%S")
    except Exception:
        ts_fmt = ts[:8]

    glow = "box-shadow:0 0 15px rgba(255,59,92,0.15);" if level == "critical" else \
           "box-shadow:0 0 10px rgba(255,179,0,0.1);" if level == "high" else ""

    st.markdown(f"""
    <div class="sentinel-card risk-{level}" style="margin-bottom:0.4rem; padding:0.7rem 0.9rem 0.7rem 1.1rem; {glow}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="risk-badge risk-{level}">{item.get('risk_level','SAFE')}</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;">{source}</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
                             color:{'#ff3b5c' if score>75 else '#ffb300' if score>55 else '#ff8c00' if score>30 else '#00ffa3'};">
                    {score:.0f}
                </span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.58rem; color:#2a4a5c;">{ts_fmt}</span>
            </div>
        </div>
        <div style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#c8d8e8; line-height:1.4;">
            {preview}{'...' if len(item.get('content_preview','')) > 100 else ''}
        </div>
        <div style="margin-top:4px; font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#4a7090;">
            {cats}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_stream_analytics(feed: list):
    if not feed:
        st.markdown('<div style="color:#4a7090; font-family:\'Share Tech Mono\',monospace; font-size:0.75rem; padding:1rem;">Awaiting stream data...</div>', unsafe_allow_html=True)
        return

    import plotly.graph_objects as go

    # Risk level breakdown
    levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    counts = {l: sum(1 for i in feed if i.get("risk_level") == l) for l in levels}
    colors = {"CRITICAL": "#ff3b5c", "HIGH": "#ffb300", "MEDIUM": "#ff8c00", "LOW": "#00c8ff", "SAFE": "#00ffa3"}

    fig = go.Figure(go.Bar(
        x=list(counts.keys()),
        y=list(counts.values()),
        marker_color=[colors[l] for l in levels],
        marker_line_width=0,
    ))
    fig.update_layout(
        height=160,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=9),
        margin=dict(l=5, r=5, t=5, b=30),
        xaxis=dict(showgrid=False, color="#4a7090", linecolor="#1a3a5c"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090", linecolor="#1a3a5c"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Quick stats
    flagged_count = sum(1 for i in feed if i.get("flagged"))
    avg_score = sum(i.get("risk_score", 0) for i in feed) / max(len(feed), 1)

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.5rem;">
        <div style="background:#0d1e2e; border:1px solid #1a3a5c; border-radius:4px; padding:0.5rem; text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.55rem; color:#4a7090;">FLAGGED</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.3rem; font-weight:700; color:#ff3b5c;">{flagged_count}</div>
        </div>
        <div style="background:#0d1e2e; border:1px solid #1a3a5c; border-radius:4px; padding:0.5rem; text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.55rem; color:#4a7090;">AVG RISK</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.3rem; font-weight:700; color:#00c8ff;">{avg_score:.1f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_quick_analyze():
    """Quick analysis input in monitoring panel."""
    text = st.text_area(
        "Enter text to analyze",
        placeholder="Paste or type text to analyze in real-time...",
        height=100,
        label_visibility="collapsed",
        key="live_analyze_input"
    )

    if st.button("⚡ Analyze Now", use_container_width=True, key="live_analyze_btn"):
        if text.strip():
            with st.spinner("Analyzing..."):
                result = analyze_text(
                    text,
                    anonymize=st.session_state.get("anonymize", True),
                    source="Quick Analyze",
                )

                # Add to history and feed
                st.session_state.analysis_history.insert(0, result)
                st.session_state.live_feed.insert(0, result)

                # Update stats
                stats = st.session_state.get("global_stats", {})
                stats["total_analyzed"] = stats.get("total_analyzed", 0) + 1
                if result.get("flagged"):
                    stats["threats_detected"] = stats.get("threats_detected", 0) + 1
                st.session_state.global_stats = stats

            level = result.get("risk_level", "SAFE")
            score = result.get("risk_score", 0)

            level_css = level.lower()
            st.markdown(f"""
            <div class="sentinel-card risk-{level_css}" style="margin-top:0.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="risk-badge risk-{level_css}">{level}</span>
                    <span style="font-family:'Rajdhani',sans-serif; font-size:1.5rem; font-weight:700;
                                 color:{'#ff3b5c' if score>75 else '#ffb300' if score>55 else '#ff8c00' if score>30 else '#00ffa3'};">
                        {score:.0f}/100
                    </span>
                </div>
                <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem; color:#8ab0cc; margin-top:6px;">
                    {result.get('explanation','')[:200]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
