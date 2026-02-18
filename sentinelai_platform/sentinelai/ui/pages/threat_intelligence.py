"""
SentinelAI — Threat Intelligence Page
Trends, heatmaps, behavioral patterns, network analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def render_threat_intelligence():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🗺️ Threat Intelligence</div>
        <div class="page-subtitle">Trend analysis · Behavioral patterns · Risk mapping · Early warning</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Trends",
        "🌡️ Risk Heatmap",
        "🕸️ Entity Network",
        "⚡ Early Warning",
    ])

    with tab1:
        _render_trends()
    with tab2:
        _render_heatmap()
    with tab3:
        _render_entity_network()
    with tab4:
        _render_early_warning()


def _generate_time_series(days=30, base_threat=25):
    """Generate realistic threat time series data."""
    dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
    threats = []
    base = base_threat
    for d in dates:
        # Weekday effect (more threats on weekdays)
        weekday_mult = 1.2 if d.weekday() < 5 else 0.7
        # Random spikes
        spike = random.uniform(2, 40) if random.random() > 0.85 else 0
        val = max(0, base * weekday_mult + random.gauss(0, 5) + spike)
        threats.append(round(val, 1))
        # Trend drift
        base += random.gauss(0, 0.5)
        base = max(10, min(50, base))
    return dates, threats


def _render_trends():
    st.markdown('<div class="section-header">Threat Volume Trends (30 Days)</div>', unsafe_allow_html=True)

    dates, threats = _generate_time_series(30)
    _, violence = _generate_time_series(30, 8)
    _, cyber = _generate_time_series(30, 12)
    _, phishing = _generate_time_series(30, 15)
    _, misinfo = _generate_time_series(30, 6)

    fig = go.Figure()

    # Total area
    fig.add_trace(go.Scatter(
        x=dates, y=threats, name="Total Threats",
        fill="tozeroy", fillcolor="rgba(0,200,255,0.06)",
        line=dict(color="#00c8ff", width=2),
        hovertemplate="<b>Total</b>: %{y:.0f}<br>%{x}<extra></extra>",
    ))

    category_colors = {
        "Violence": "#ff3b5c",
        "Cybersecurity": "#9b59b6",
        "Phishing": "#ffb300",
        "Misinformation": "#00ffa3",
    }

    for (name, data), color in zip(
        [("Violence", violence), ("Cybersecurity", cyber), ("Phishing", phishing), ("Misinformation", misinfo)],
        ["#ff3b5c", "#9b59b6", "#ffb300", "#00ffa3"]
    ):
        fig.add_trace(go.Scatter(
            x=dates, y=data, name=name,
            mode="lines",
            line=dict(color=color, width=1.5, dash="dot"),
            hovertemplate=f"<b>{name}</b>: %{{y:.0f}}<br>%{{x}}<extra></extra>",
        ))

    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=10),
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis=dict(showgrid=False, color="#4a7090", linecolor="#1a3a5c"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090", linecolor="#1a3a5c"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8ab0cc", size=9)),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Category breakdown bar chart
    st.markdown('<div class="section-header">Category Breakdown (Last 7 Days)</div>', unsafe_allow_html=True)

    categories = ["Violence", "Cybersecurity", "Phishing", "Misinformation",
                  "Suspicious Activity", "Hate Speech", "Data Exfiltration"]
    counts = [random.randint(2, 28) for _ in categories]
    colors = ["#ff3b5c", "#9b59b6", "#ffb300", "#00ffa3", "#00c8ff", "#ff8c00", "#e74c3c"]

    fig2 = go.Figure(go.Bar(
        x=counts, y=categories,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b>: %{x} incidents<extra></extra>",
    ))

    fig2.update_layout(
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=10),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090"),
        yaxis=dict(showgrid=False, color="#4a7090"),
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # Predictive scoring panel
    st.markdown('<div class="section-header">⚡ Predictive Threat Scoring (Next 7 Days)</div>', unsafe_allow_html=True)
    
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
    last_val = threats[-1]
    predictions = []
    confidence_upper = []
    confidence_lower = []
    for i in range(7):
        pred = last_val + random.gauss(2, 3) * (1 + i * 0.1)
        pred = max(0, pred)
        predictions.append(round(pred, 1))
        confidence_upper.append(round(pred + 8 + i * 1.5, 1))
        confidence_lower.append(round(max(0, pred - 8 - i * 1.5), 1))
        last_val = pred

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=future_dates + future_dates[::-1],
        y=confidence_upper + confidence_lower[::-1],
        fill="toself", fillcolor="rgba(255,179,0,0.05)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Confidence Band",
        hoverinfo="skip",
    ))
    fig3.add_trace(go.Scatter(
        x=future_dates, y=predictions,
        mode="lines+markers",
        line=dict(color="#ffb300", width=2, dash="dash"),
        marker=dict(size=7, color="#ffb300"),
        name="Predicted",
        hovertemplate="<b>Predicted</b>: %{y:.0f}<br>%{x}<extra></extra>",
    ))

    fig3.update_layout(
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=10),
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis=dict(showgrid=False, color="#4a7090"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8ab0cc", size=9)),
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


def _render_heatmap():
    st.markdown('<div class="section-header">Geographic Risk Distribution</div>', unsafe_allow_html=True)
    
    # Simulated geographic data
    countries = [
        ("United States", 37.09, -95.71, 72),
        ("Russia", 61.52, 105.32, 85),
        ("China", 35.86, 104.20, 78),
        ("Iran", 32.43, 53.69, 81),
        ("North Korea", 40.34, 127.51, 88),
        ("Germany", 51.17, 10.45, 32),
        ("United Kingdom", 55.38, -3.44, 28),
        ("Brazil", -14.24, -51.93, 41),
        ("India", 20.59, 78.96, 45),
        ("Australia", -25.27, 133.78, 22),
        ("Canada", 56.13, -106.35, 25),
        ("France", 46.23, 2.21, 30),
        ("Japan", 36.20, 138.25, 35),
        ("South Korea", 35.91, 127.77, 40),
        ("Turkey", 38.96, 35.24, 55),
    ]

    fig = go.Figure(go.Scattergeo(
        lat=[c[1] for c in countries],
        lon=[c[2] for c in countries],
        text=[f"{c[0]}<br>Risk: {c[3]}" for c in countries],
        marker=dict(
            size=[c[3] / 4 + 5 for c in countries],
            color=[c[3] for c in countries],
            colorscale=[[0, "#00ffa3"], [0.4, "#ffb300"], [0.7, "#ff8c00"], [1, "#ff3b5c"]],
            colorbar=dict(
                title=dict(text="Risk Score", font=dict(color="#8ab0cc", size=10)),
                tickfont=dict(color="#8ab0cc", size=9),
                outlinecolor="rgba(0,0,0,0)",
                bgcolor="rgba(0,0,0,0)",
                thickness=10,
            ),
            line=dict(color="#050a0f", width=1),
            opacity=0.85,
        ),
        hovertemplate="%{text}<extra></extra>",
        mode="markers",
    ))

    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showland=True, landcolor="#0d1e2e",
            showocean=True, oceancolor="#050a0f",
            showlakes=False,
            showcountries=True, countrycolor="#1a3a5c",
            showcoastlines=True, coastlinecolor="#1a3a5c",
            projection_type="natural earth",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Time-of-day heatmap
    st.markdown('<div class="section-header">Attack Timing Heatmap (Hour × Day of Week)</div>', unsafe_allow_html=True)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours = [f"{h:02d}:00" for h in range(24)]
    
    # Generate realistic data (business hours higher, night lower)
    data = []
    for day_idx, day in enumerate(days):
        row = []
        for hour in range(24):
            base = 2
            if day_idx < 5:  # Weekday
                if 9 <= hour <= 17:
                    base = random.randint(5, 20)
                elif 7 <= hour <= 22:
                    base = random.randint(2, 10)
            else:  # Weekend
                base = random.randint(1, 8)
            row.append(base + random.randint(0, 3))
        data.append(row)

    fig2 = go.Figure(go.Heatmap(
        z=data, x=hours, y=days,
        colorscale=[[0, "#050a0f"], [0.3, "#0d3a5c"], [0.6, "#ffb300"], [1, "#ff3b5c"]],
        hovertemplate="<b>%{y}</b> at <b>%{x}</b><br>Incidents: %{z}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=8, len=0.8,
            tickfont=dict(color="#8ab0cc", size=9),
            outlinecolor="rgba(0,0,0,0)",
        )
    ))

    fig2.update_layout(
        height=250,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8ab0cc", family="Share Tech Mono", size=9),
        margin=dict(l=80, r=10, t=10, b=50),
        xaxis=dict(showgrid=False, color="#4a7090", tickangle=45),
        yaxis=dict(showgrid=False, color="#4a7090"),
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})


def _render_entity_network():
    st.markdown('<div class="section-header">Entity Relationship Network</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#4a7090; margin-bottom:0.5rem;">
        Showing relationships between detected entities, threat actors, and risk categories
    </div>
    """, unsafe_allow_html=True)

    # Build network graph
    import math

    # Nodes
    central_node = {"id": "THREAT HUB", "x": 0, "y": 0, "size": 30, "color": "#ff3b5c", "type": "hub"}
    
    categories = [
        ("Violence", "#ff3b5c"), ("Cybersecurity", "#9b59b6"), ("Phishing", "#ffb300"),
        ("Misinformation", "#00ffa3"), ("Suspicious Activity", "#00c8ff"), ("Hate Speech", "#ff8c00"),
    ]
    entities = [
        "weapons", "malware", "exploit", "target", "credentials",
        "payload", "threat actor", "safe house", "coordinates",
    ]

    cat_nodes = []
    for i, (name, color) in enumerate(categories):
        angle = (2 * math.pi * i) / len(categories)
        r = 200
        cat_nodes.append({
            "id": name, "x": r * math.cos(angle), "y": r * math.sin(angle),
            "size": 18, "color": color
        })

    entity_nodes = []
    for i, ent in enumerate(entities):
        angle = (2 * math.pi * i) / len(entities) + 0.3
        r = random.uniform(100, 180)
        entity_nodes.append({
            "id": ent, "x": r * math.cos(angle), "y": r * math.sin(angle),
            "size": 10, "color": "#4a7090"
        })

    all_nodes = [central_node] + cat_nodes + entity_nodes

    # Edges
    edge_x, edge_y = [], []
    # Hub to categories
    for cat in cat_nodes:
        edge_x += [0, cat["x"], None]
        edge_y += [0, cat["y"], None]
    # Categories to entities
    for ent in entity_nodes:
        closest_cat = random.choice(cat_nodes)
        edge_x += [closest_cat["x"], ent["x"], None]
        edge_y += [closest_cat["y"], ent["y"], None]

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="#1a3a5c", width=1),
        hoverinfo="none",
        showlegend=False,
    ))

    # Nodes
    fig.add_trace(go.Scatter(
        x=[n["x"] for n in all_nodes],
        y=[n["y"] for n in all_nodes],
        mode="markers+text",
        marker=dict(
            size=[n["size"] for n in all_nodes],
            color=[n["color"] for n in all_nodes],
            line=dict(color="#050a0f", width=2),
            opacity=0.9,
        ),
        text=[n["id"] for n in all_nodes],
        textposition="top center",
        textfont=dict(family="Share Tech Mono", size=8, color="#8ab0cc"),
        hovertemplate="<b>%{text}</b><extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#050a0f",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        font=dict(color="#8ab0cc"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#2a4a5c; margin-top:-0.5rem;">
        Node size = frequency · Edge = relationship strength · Color = risk category
    </div>
    """, unsafe_allow_html=True)


def _render_early_warning():
    st.markdown("""
    <div style="background:linear-gradient(135deg, #1a0510, #0d0a1a); border:1px solid #3a1a3c;
                border-radius:8px; padding:1rem 1.2rem; margin-bottom:1.2rem;">
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700;
                    color:#ff3b5c; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.3rem;">
            ⚡ Early Warning System
        </div>
        <div style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#8ab0cc; line-height:1.5;">
            AI-driven predictive intelligence that detects emerging threat patterns before they escalate.
            Monitors baseline deviations, velocity changes, and cross-source correlation anomalies.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Warning indicators
    warnings = [
        {
            "title": "Phishing Campaign Detected",
            "level": "HIGH",
            "detail": "17% increase in social engineering attempts over last 6 hours. Pattern consistent with coordinated campaign targeting financial sector.",
            "confidence": 87,
            "trend": "▲ Rising",
            "trend_color": "#ff3b5c",
        },
        {
            "title": "Anomalous Communication Pattern",
            "level": "MEDIUM",
            "detail": "Behavioral deviation detected in Feed Source #3. Message frequency and keyword density 3.2σ above baseline.",
            "confidence": 72,
            "trend": "▲ Rising",
            "trend_color": "#ffb300",
        },
        {
            "title": "Misinformation Velocity Spike",
            "level": "MEDIUM",
            "detail": "Rapid propagation of unverified claims about infrastructure. Cross-referencing against known disinfo networks.",
            "confidence": 65,
            "trend": "→ Stable",
            "trend_color": "#ffb300",
        },
        {
            "title": "Credential Dump Keywords",
            "level": "HIGH",
            "detail": "Multiple sources referencing credential sales. Possible data breach activity on darknet channels.",
            "confidence": 78,
            "trend": "▲ Rising",
            "trend_color": "#ff3b5c",
        },
        {
            "title": "Multilingual Threat Spike",
            "level": "LOW",
            "detail": "Arabic and Farsi language threat indicators up 8% — within normal variance but flagged for watch.",
            "confidence": 45,
            "trend": "→ Stable",
            "trend_color": "#00c8ff",
        },
    ]

    for w in warnings:
        level_css = w["level"].lower()
        st.markdown(f"""
        <div class="sentinel-card risk-{level_css}" style="margin-bottom:0.6rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                <div>
                    <span class="risk-badge risk-{level_css}" style="margin-right:8px;">{w['level']}</span>
                    <span style="font-family:'Rajdhani',sans-serif; font-size:0.95rem; font-weight:600; color:#e8f4ff;">{w['title']}</span>
                </div>
                <div style="text-align:right; flex-shrink:0;">
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:{w['trend_color']};">{w['trend']}</div>
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;">CONF: {w['confidence']}%</div>
                </div>
            </div>
            <div style="font-family:'Exo 2',sans-serif; font-size:0.8rem; color:#8ab0cc; line-height:1.4; margin-bottom:6px;">
                {w['detail']}
            </div>
            <div style="background:#0a0a0f; border-radius:2px; height:4px; margin-top:6px;">
                <div style="background:{'#ff3b5c' if w['level']=='CRITICAL' else '#ffb300' if w['level']=='HIGH' else '#ff8c00' if w['level']=='MEDIUM' else '#00c8ff'};
                            width:{w['confidence']}%; height:100%; border-radius:2px; transition:width 0.3s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Multi-language detection indicator
    st.markdown('<div class="section-header">Multi-Language Threat Detection</div>', unsafe_allow_html=True)
    
    languages = [
        ("English", 58, "#00c8ff"),
        ("Arabic", 12, "#ffb300"),
        ("Russian", 9, "#ff3b5c"),
        ("Chinese", 7, "#9b59b6"),
        ("Farsi", 5, "#ff8c00"),
        ("Other", 9, "#4a7090"),
    ]

    fig = go.Figure(go.Pie(
        labels=[l[0] for l in languages],
        values=[l[1] for l in languages],
        hole=0.5,
        marker=dict(colors=[l[2] for l in languages], line=dict(color="#050a0f", width=2)),
        textfont=dict(family="Share Tech Mono", size=9, color="#e8f4ff"),
        hovertemplate="<b>%{label}</b><br>%{value}% of threats<extra></extra>",
    ))

    fig.update_layout(
        height=220,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color="#8ab0cc", size=9), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
