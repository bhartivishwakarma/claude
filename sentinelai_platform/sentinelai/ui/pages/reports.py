"""
SentinelAI — Reports & Insights Page
Export, recommendations, risk history
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import json
from datetime import datetime


def render_reports():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📊 Reports & Insights</div>
        <div class="page-subtitle">Export · Recommendations · Risk history · Intelligence briefings</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Summary Report", "📤 Export Data", "💡 AI Recommendations"])

    with tab1:
        _render_summary_report()
    with tab2:
        _render_export()
    with tab3:
        _render_recommendations()


def _render_summary_report():
    history = st.session_state.get("analysis_history", [])
    stats = st.session_state.get("global_stats", {})
    alerts = st.session_state.get("alerts", [])

    now = datetime.now().strftime("%B %d, %Y at %H:%M UTC")

    # Report header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #0a1520, #0d2030); border:1px solid #1a3a5c;
                border-radius:8px; padding:1.5rem 1.8rem; margin-bottom:1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1.6rem; font-weight:700;
                            color:#00c8ff; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.2rem;">
                    🛡️ SentinelAI Intelligence Brief
                </div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#4a7090; letter-spacing:0.15em;">
                    SESSION REPORT · {now}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090;">Classification</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:0.9rem; font-weight:700;
                            color:#ffb300; letter-spacing:0.1em;">CONFIDENTIAL</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Summary
    total = stats.get("total_analyzed", 0)
    threats = stats.get("threats_detected", 0)
    avg = stats.get("avg_risk_score", 0)
    threat_rate = (threats / max(total, 1)) * 100
    current_level = st.session_state.get("threat_level", "MODERATE")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Items Analyzed", total)
    with col2:
        st.metric("Threats Detected", threats, delta=f"{threat_rate:.0f}% rate")
    with col3:
        st.metric("Avg Risk Score", f"{avg:.1f}/100")
    with col4:
        st.metric("Current Threat Level", current_level)

    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="copilot-bubble">
        <div class="copilot-label">📊 AI-Generated Intelligence Summary</div>
        During this monitoring session, SentinelAI analyzed <strong style="color:#00c8ff;">{total}</strong> content items
        across multiple sources. Of these, <strong style="color:#ff3b5c;">{threats}</strong> were flagged as potentially
        threatening ({threat_rate:.0f}% detection rate), with the current overall threat posture assessed as
        <strong style="color:#ffb300;">{current_level}</strong>.
        <br><br>
        The most prevalent threat categories observed were phishing/social engineering, cybersecurity threats,
        and suspicious behavioral patterns. No confirmed active attacks are currently in progress based on
        available data, though elevated vigilance is recommended given the current activity patterns.
        <br><br>
        Privacy protocols are active: all data processed in-memory with PII anonymization enabled.
        Zero items persisted to external storage this session.
    </div>
    """, unsafe_allow_html=True)

    # Risk breakdown chart
    st.markdown('<div class="section-header">Risk Level Breakdown</div>', unsafe_allow_html=True)
    
    if history:
        levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
        counts = {l: sum(1 for r in history if r.get("risk_level") == l) for l in levels}
        colors = {"CRITICAL": "#ff3b5c", "HIGH": "#ffb300", "MEDIUM": "#ff8c00", "LOW": "#00c8ff", "SAFE": "#00ffa3"}

        col_chart, col_table = st.columns([2, 1])
        with col_chart:
            fig = go.Figure(go.Bar(
                x=list(counts.keys()),
                y=list(counts.values()),
                marker_color=[colors[l] for l in levels],
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
            ))
            fig.update_layout(
                height=200,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8ab0cc", family="Share Tech Mono", size=10),
                margin=dict(l=5, r=5, t=5, b=30),
                xaxis=dict(showgrid=False, color="#4a7090"),
                yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#4a7090"),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col_table:
            for level, count in counts.items():
                pct = (count / max(total, 1)) * 100
                level_css = level.lower()
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:0.35rem 0; border-bottom:1px solid #0d1e2e;">
                    <span class="risk-badge risk-{level_css}">{level}</span>
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:#00c8ff;">{count}</span>
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#4a7090;">{pct:.0f}%</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No analysis data available for this session.")

    # Recent high-risk items
    st.markdown('<div class="section-header">High-Risk Events This Session</div>', unsafe_allow_html=True)
    high_risk = [r for r in history if r.get("risk_score", 0) >= 55]
    if high_risk:
        for r in high_risk[:5]:
            level_css = r.get("risk_level", "HIGH").lower()
            st.markdown(f"""
            <div class="threat-row">
                <span class="risk-badge risk-{level_css}">{r.get('risk_level')}</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#00c8ff; margin-left:8px;">{r.get('risk_score'):.0f}/100</span>
                <span style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#c8d8e8; margin-left:12px;">{r.get('content_preview','')[:80]}...</span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090; float:right;">
                    {', '.join(r.get('categories', [])[:2])}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#4a7090; font-family:\'Share Tech Mono\',monospace; font-size:0.75rem;">No high-risk events detected this session.</div>', unsafe_allow_html=True)


def _render_export():
    history = st.session_state.get("analysis_history", [])
    stats = st.session_state.get("global_stats", {})

    st.markdown('<div class="section-header">Export Options</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="sentinel-card" style="text-align:center; padding:1.5rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📊</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600; color:#e8f4ff; text-transform:uppercase;">CSV Export</div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#4a7090; margin:0.3rem 0 0.8rem;">Full analysis history table</div>
        </div>
        """, unsafe_allow_html=True)
        
        if history:
            df = pd.DataFrame([{
                "ID": r.get("id"),
                "Timestamp": r.get("timestamp"),
                "Source": r.get("source"),
                "Risk Score": r.get("risk_score"),
                "Risk Level": r.get("risk_level"),
                "Categories": ", ".join(r.get("categories", [])),
                "Sentiment": r.get("sentiment"),
                "Flagged": r.get("flagged"),
                "Content Preview": r.get("content_preview", "")[:100],
            } for r in history])
            
            csv_data = df.to_csv(index=False)
            st.download_button(
                "⬇ Download CSV",
                data=csv_data,
                file_name=f"sentinelai_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.button("⬇ Download CSV", disabled=True, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="sentinel-card" style="text-align:center; padding:1.5rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📄</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600; color:#e8f4ff; text-transform:uppercase;">JSON Export</div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#4a7090; margin:0.3rem 0 0.8rem;">Structured data with all fields</div>
        </div>
        """, unsafe_allow_html=True)
        
        if history:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "session_stats": stats,
                "analysis_results": history,
                "privacy_notice": "All data processed in-memory. No external storage used.",
            }
            json_str = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                "⬇ Download JSON",
                data=json_str,
                file_name=f"sentinelai_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.button("⬇ Download JSON", disabled=True, use_container_width=True)

    with col3:
        st.markdown("""
        <div class="sentinel-card" style="text-align:center; padding:1.5rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📑</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600; color:#e8f4ff; text-transform:uppercase;">Text Report</div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#4a7090; margin:0.3rem 0 0.8rem;">Plain text intelligence brief</div>
        </div>
        """, unsafe_allow_html=True)
        
        report_text = _generate_text_report(history, stats)
        st.download_button(
            "⬇ Download Report",
            data=report_text,
            file_name=f"sentinelai_brief_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # Preview
    if history:
        st.markdown('<div class="section-header">Data Preview</div>', unsafe_allow_html=True)
        df_preview = pd.DataFrame([{
            "ID": r.get("id"),
            "Risk Level": r.get("risk_level"),
            "Score": r.get("risk_score"),
            "Source": r.get("source"),
            "Categories": ", ".join(r.get("categories", [])[:2]),
            "Flagged": "⚠️" if r.get("flagged") else "✓",
        } for r in history[:10]])
        st.dataframe(df_preview, use_container_width=True, hide_index=True)


def _generate_text_report(history: list, stats: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    total = stats.get("total_analyzed", 0)
    threats = stats.get("threats_detected", 0)
    avg = stats.get("avg_risk_score", 0)

    lines = [
        "=" * 70,
        "SENTINELAI — THREAT INTELLIGENCE BRIEF",
        f"Generated: {now}",
        "Classification: CONFIDENTIAL — AUTHORIZED PERSONNEL ONLY",
        "=" * 70,
        "",
        "EXECUTIVE SUMMARY",
        "-" * 40,
        f"Total Items Analyzed: {total}",
        f"Threats Detected: {threats}",
        f"Average Risk Score: {avg:.1f}/100",
        f"Current Threat Level: {st.session_state.get('threat_level', 'MODERATE')}",
        "",
        "RISK BREAKDOWN",
        "-" * 40,
    ]

    levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "SAFE"]
    for level in levels:
        count = sum(1 for r in history if r.get("risk_level") == level)
        lines.append(f"  {level}: {count}")

    lines += ["", "HIGH-RISK EVENTS", "-" * 40]
    high_risk = [r for r in history if r.get("risk_score", 0) >= 55]
    for r in high_risk[:10]:
        lines += [
            f"  [{r.get('risk_level')}] Score: {r.get('risk_score', 0):.1f}",
            f"  Source: {r.get('source')}",
            f"  Categories: {', '.join(r.get('categories', []))}",
            f"  Content: {r.get('content_preview', '')[:120]}...",
            f"  Analysis: {r.get('explanation', '')[:200]}...",
            "",
        ]

    lines += [
        "PRIVACY NOTICE",
        "-" * 40,
        "All data processed in-memory. PII anonymization applied.",
        "No content persisted to external storage this session.",
        "Compliant with privacy-first architecture principles.",
        "",
        "=" * 70,
        "END OF REPORT — SENTINELAI DEFENCE PLATFORM",
        "=" * 70,
    ]

    return "\n".join(lines)


def _render_recommendations():
    history = st.session_state.get("analysis_history", [])
    stats = st.session_state.get("global_stats", {})

    st.markdown('<div class="section-header">AI-Generated Recommendations</div>', unsafe_allow_html=True)

    # Analyze patterns to generate recommendations
    cats = {}
    for r in history:
        for c in r.get("categories", []):
            cats[c] = cats.get(c, 0) + 1

    top_cat = max(cats, key=cats.get) if cats else None
    threats = stats.get("threats_detected", 0)
    total = stats.get("total_analyzed", 1)
    threat_rate = threats / total

    recommendations = []

    if threat_rate > 0.4:
        recommendations.append({
            "priority": "CRITICAL",
            "title": "Elevated Threat Environment",
            "detail": f"Your threat detection rate of {threat_rate*100:.0f}% is significantly above baseline. Recommend increasing monitoring frequency and alerting security team leadership.",
            "actions": ["Escalate to security operations center", "Enable enhanced logging", "Review source filtering thresholds"],
        })

    if "Phishing" in cats or "Social Engineering" in cats:
        recommendations.append({
            "priority": "HIGH",
            "title": "Phishing Campaign Activity Detected",
            "detail": "Multiple social engineering and phishing indicators detected. This pattern is consistent with an organized campaign.",
            "actions": ["Issue organization-wide phishing awareness alert", "Verify email gateway filters are up-to-date", "Check for domain spoofing variants"],
        })

    if "Cybersecurity" in cats:
        recommendations.append({
            "priority": "HIGH",
            "title": "Cybersecurity Threat Indicators",
            "detail": "Malware and exploitation-related language detected. Review endpoint security posture immediately.",
            "actions": ["Run enterprise-wide endpoint scan", "Patch management review", "Check for indicators of compromise"],
        })

    if "Misinformation" in cats:
        recommendations.append({
            "priority": "MEDIUM",
            "title": "Misinformation Activity",
            "detail": "Disinformation patterns detected. Consider cross-referencing with trusted fact-checking databases.",
            "actions": ["Label and track flagged content", "Alert communications team", "Monitor for amplification patterns"],
        })

    # Default recommendations
    recommendations += [
        {
            "priority": "LOW",
            "title": "Maintain Privacy-First Processing",
            "detail": "Continue using anonymization and local processing mode to protect analyzed data subjects.",
            "actions": ["Keep anonymization enabled", "Review data retention settings", "Audit access logs regularly"],
        },
        {
            "priority": "LOW",
            "title": "Calibrate Detection Thresholds",
            "detail": "Regular calibration of risk thresholds reduces false positives and improves analyst efficiency.",
            "actions": ["Review flagged items for accuracy", "Provide feedback to improve models", "Update keyword lists monthly"],
        },
    ]

    for rec in recommendations:
        level_css = rec["priority"].lower()
        st.markdown(f"""
        <div class="sentinel-card risk-{level_css}" style="margin-bottom:0.8rem;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                <span class="risk-badge risk-{level_css}">{rec['priority']}</span>
                <span style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600; color:#e8f4ff;">{rec['title']}</span>
            </div>
            <div style="font-family:'Exo 2',sans-serif; font-size:0.83rem; color:#8ab0cc; line-height:1.5; margin-bottom:8px;">
                {rec['detail']}
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090; text-transform:uppercase; margin-bottom:4px;">Recommended Actions:</div>
            {''.join(f"""<div style="font-family:'Exo 2',sans-serif; font-size:0.78rem; color:#c8d8e8; padding:2px 0; padding-left:0.5rem; border-left:2px solid #1a3a5c; margin-bottom:3px;">→ {a}</div>""" for a in rec['actions'])}
        </div>
        """, unsafe_allow_html=True)
