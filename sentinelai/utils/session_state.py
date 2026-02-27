"""
Session state initialization for SentinelAI
"""

import streamlit as st
from datetime import datetime
import random


def init_session_state():
    """Initialize all session state variables with defaults."""

    defaults = {
        "current_page": "🏠 Home Dashboard",
        "threat_level": "MODERATE",
        "local_mode": True,
        "anonymize": True,
        "temp_only": True,
        "ai_provider": "Claude (Anthropic)",
        "anthropic_api_key": "",
        "analysis_history": [],
        "live_feed": [],
        "global_stats": {
            "total_analyzed": 0,
            "threats_detected": 0,
            "false_positives": 0,
            "avg_risk_score": 0.0,
        },
        "alerts": [],
        "monitoring_active": False,
        "copilot_chat": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Seed some demo data if history is empty
    if not st.session_state.analysis_history:
        _seed_demo_data()


def _seed_demo_data():
    """Seed demo analysis history for visualization."""
    import random
    from datetime import timedelta

    sample_results = [
        {
            "id": f"SENT-{random.randint(10000,99999)}",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
            "source": random.choice(["Text Input", "Document Upload", "Live Feed", "Social Media"]),
            "content_preview": text,
            "risk_score": score,
            "risk_level": level,
            "categories": cats,
            "entities": entities,
            "sentiment": sentiment,
            "language": "English",
            "flagged": score > 40,
        }
        for text, score, level, cats, entities, sentiment in [
            ("System update required immediately. Click here to verify your account.",
             72, "HIGH", ["Phishing", "Social Engineering"], ["account", "verify"], "Urgent"),
            ("Had a great meeting today, excited about the new project direction.",
             8, "SAFE", [], [], "Positive"),
            ("The shipment will arrive at the warehouse district tonight. Coordinates sent separately.",
             55, "MEDIUM", ["Suspicious Activity", "Location Data"], ["warehouse", "coordinates"], "Neutral"),
            ("Breaking: Multiple explosions reported near the city center. Casualties unknown.",
             63, "HIGH", ["Violence", "Breaking News"], ["explosions", "city center"], "Alarming"),
            ("Please find attached the Q3 financial report for your review.",
             5, "SAFE", [], [], "Professional"),
            ("They will regret this. I know where they live and work. Watch.",
             91, "CRITICAL", ["Threat", "Harassment", "Violence"], ["threat", "location"], "Hostile"),
            ("New malware strain detected targeting financial institutions globally.",
             68, "HIGH", ["Cybersecurity", "Malware"], ["malware", "financial"], "Alarming"),
            ("The community garden project is coming along beautifully this spring.",
             3, "SAFE", [], [], "Positive"),
        ]
    ]

    st.session_state.analysis_history = sample_results
    st.session_state.global_stats = {
        "total_analyzed": len(sample_results),
        "threats_detected": sum(1 for r in sample_results if r["flagged"]),
        "false_positives": 1,
        "avg_risk_score": sum(r["risk_score"] for r in sample_results) / len(sample_results),
    }

    # Seed alerts
    st.session_state.alerts = [
        {"level": "CRITICAL", "message": "Threat language detected in live feed stream", "time": "2 min ago"},
        {"level": "HIGH", "message": "Suspicious document uploaded — weapons reference found", "time": "8 min ago"},
        {"level": "MEDIUM", "message": "Anomalous behavioral pattern from feed source #3", "time": "15 min ago"},
        {"level": "LOW", "message": "Elevated phishing keywords in monitored channel", "time": "32 min ago"},
    ]
