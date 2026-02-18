"""
SentinelAI — Core threat analysis service.

Performs multi-dimensional risk analysis using:
  1. Rule-based pattern matching (always available, zero dependencies)
  2. Claude AI via Anthropic API (when API key provided)

All processing happens in-memory; nothing is persisted.
"""

from __future__ import annotations

import re
import json
import time
import hashlib
import random
from datetime import datetime
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# ── THREAT KEYWORD PATTERNS ──────────────────────────────────────────────────

PATTERNS = {
    "violence": [
        r"\b(kill|murder|shoot|bomb|explode|attack|assault|stab|shoot|massacre)\b",
        r"\b(weapon|gun|knife|explosive|grenade|rpg|ied)\b",
        r"\b(threat|threaten|harm|hurt|destroy)\b.{0,30}\b(you|them|people|everyone)\b",
    ],
    "cybersecurity": [
        r"\b(malware|ransomware|phishing|exploit|vulnerability|zero.?day|ddos)\b",
        r"\b(hack|breach|compromise|infiltrate|backdoor|payload|injection)\b",
        r"\b(credentials?|password|token|api.?key).{0,20}\b(steal|leak|dump|expose)\b",
    ],
    "social_engineering": [
        r"\b(click here|verify your|confirm your|account suspended|urgent action)\b",
        r"\b(prize|winner|congratulations|claim now|limited time)\b",
        r"\b(bank|paypal|amazon|apple|microsoft).{0,30}\b(verify|confirm|update|suspend)\b",
    ],
    "hate_speech": [
        r"\b(hate|despise|inferior|subhuman).{0,20}\b(race|religion|gender|ethnic)\b",
        r"\b(extremist|radical|terrorist|jihad|supremacist)\b",
    ],
    "misinformation": [
        r"\b(breaking|exposed|they don'?t want you to know|secret|cover.?up)\b",
        r"\b(proven|scientifically proven|doctors hate|suppressed)\b",
        r"\b(conspiracy|hoax|fake|false flag)\b",
    ],
    "suspicious_activity": [
        r"\b(coordinates?|location|meet at|rendezvous|drop.?off|pick.?up)\b.{0,50}\b(tonight|tomorrow|after dark)\b",
        r"\b(encrypted|secure channel|no trace|burner|anonymous)\b",
        r"\b(shipment|package|cargo|delivery).{0,30}\b(location|coordinates|address)\b",
    ],
    "data_exfiltration": [
        r"\b(exfil|exfiltrate|extract|dump|steal|leak).{0,30}\b(data|database|records|files)\b",
        r"\b(send|transfer|upload).{0,20}\b(to my|to the|private|external)\b.{0,20}\b(server|drive|cloud)\b",
    ],
}

WEAPON_ENTITIES = [
    "gun", "rifle", "pistol", "bomb", "explosive", "grenade", "missile",
    "rpg", "ied", "weapon", "ammunition", "detonator", "c4", "tnt",
]

THREAT_ENTITIES = [
    "threat", "attack", "target", "victim", "hostage", "kidnap",
    "assassination", "execute", "eliminate",
]

LOCATION_RISK_TERMS = [
    "warehouse", "coordinates", "safe house", "drop point",
    "rendezvous", "border", "checkpoint", "facility",
]


def _pattern_score(text: str) -> tuple[float, dict]:
    """Run rule-based pattern matching and return (raw_score, category_hits)."""
    text_lower = text.lower()
    hits: dict[str, list[str]] = {}
    total_weight = 0.0

    weights = {
        "violence": 35,
        "cybersecurity": 28,
        "social_engineering": 22,
        "hate_speech": 30,
        "misinformation": 15,
        "suspicious_activity": 25,
        "data_exfiltration": 28,
    }

    for category, patterns in PATTERNS.items():
        matched = []
        for pattern in patterns:
            m = re.search(pattern, text_lower, re.IGNORECASE)
            if m:
                matched.append(m.group(0))
        if matched:
            hits[category] = matched
            total_weight += weights[category]

    # Cap at 95
    raw_score = min(95.0, total_weight)
    return raw_score, hits


def _extract_entities(text: str) -> dict:
    """Extract risk-relevant named entities using patterns."""
    text_lower = text.lower()
    found = {
        "weapons": [w for w in WEAPON_ENTITIES if w in text_lower],
        "threat_terms": [t for t in THREAT_ENTITIES if t in text_lower],
        "location_risk": [l for l in LOCATION_RISK_TERMS if l in text_lower],
    }
    return {k: v for k, v in found.items() if v}


def _sentiment_score(text: str) -> tuple[str, float]:
    """Simple rule-based sentiment analysis."""
    text_lower = text.lower()
    negative_terms = ["hate", "angry", "terrible", "awful", "kill", "threat", "danger",
                      "attack", "destroy", "furious", "outrage", "alarming", "crisis"]
    positive_terms = ["great", "wonderful", "love", "happy", "excellent", "beautiful",
                      "fantastic", "amazing", "good", "nice", "excited", "pleased"]

    neg = sum(1 for t in negative_terms if t in text_lower)
    pos = sum(1 for t in positive_terms if t in text_lower)

    total = neg + pos
    if total == 0:
        return "Neutral", 0.0
    score = (pos - neg) / total  # -1 to 1
    if score > 0.3:
        return "Positive", score
    elif score < -0.3:
        return "Negative", abs(score)
    else:
        return "Neutral", 0.0


def _risk_level(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    elif score >= 55:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    elif score >= 10:
        return "LOW"
    else:
        return "SAFE"


def _anonymize(text: str) -> str:
    """Basic PII anonymization."""
    # Email
    text = re.sub(r'\b[\w.+-]+@[\w-]+\.\w+\b', '[EMAIL REDACTED]', text)
    # Phone (simple patterns)
    text = re.sub(r'\b(\+?\d[\d\s\-().]{7,14}\d)\b', '[PHONE REDACTED]', text)
    # IP address
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP REDACTED]', text)
    return text


def _build_explanation(score: float, hits: dict, entities: dict, sentiment: str) -> str:
    """Build a human-readable explanation of the risk assessment."""
    parts = []
    level = _risk_level(score)

    if not hits and not entities:
        parts.append("No significant threat indicators detected in this content.")
        parts.append("The text appears benign based on pattern analysis.")
    else:
        if hits:
            cats = list(hits.keys())
            readable = [c.replace("_", " ").title() for c in cats]
            parts.append(f"Detected threat indicators across {len(cats)} category(ies): {', '.join(readable)}.")

        if "violence" in hits:
            parts.append("Content contains language associated with violence or physical threats.")
        if "cybersecurity" in hits:
            parts.append("Cybersecurity threat patterns identified — potential malware or attack activity.")
        if "social_engineering" in hits:
            parts.append("Social engineering indicators found — possible phishing or manipulation attempt.")
        if "hate_speech" in hits:
            parts.append("Hate speech or extremist content detected.")
        if "misinformation" in hits:
            parts.append("Misinformation / disinformation markers present.")
        if "suspicious_activity" in hits:
            parts.append("Suspicious coordination language detected — possible clandestine activity.")

        if entities.get("weapons"):
            parts.append(f"Weapon-related entities: {', '.join(entities['weapons'])}.")
        if entities.get("threat_terms"):
            parts.append(f"Direct threat language: {', '.join(entities['threat_terms'])}.")
        if entities.get("location_risk"):
            parts.append(f"Location/operational security terms: {', '.join(entities['location_risk'])}.")

    if sentiment == "Negative":
        parts.append("Overall sentiment is strongly negative.")

    return " ".join(parts)


def _mitigation_steps(hits: dict, score: float) -> list[str]:
    """Generate actionable mitigation recommendations."""
    steps = []
    level = _risk_level(score)

    if level == "CRITICAL":
        steps.append("🔴 IMMEDIATE ACTION: Escalate to security team / incident response.")
        steps.append("🔒 Block and preserve the source for forensic analysis.")
    elif level == "HIGH":
        steps.append("🟠 Flag for urgent review by human analyst.")
        steps.append("📋 Document incident and cross-reference with known threat actors.")

    if "cybersecurity" in hits:
        steps.append("🛡️ Run endpoint scan; isolate affected systems if necessary.")
        steps.append("🔑 Rotate credentials and invalidate active sessions.")
    if "social_engineering" in hits:
        steps.append("📧 Do not click links or provide credentials. Report as phishing.")
        steps.append("🎓 Issue security awareness reminder to affected team/users.")
    if "violence" in hits:
        steps.append("⚠️ Notify appropriate authorities if credible and imminent.")
        steps.append("📍 Preserve evidence chain for potential legal action.")
    if "hate_speech" in hits:
        steps.append("🚫 Remove content from platform per community guidelines.")
        steps.append("📝 Report to platform trust & safety team.")
    if "misinformation" in hits:
        steps.append("✅ Fact-check against verified sources before sharing.")
        steps.append("🏷️ Label content as potentially misleading if platform allows.")
    if "suspicious_activity" in hits:
        steps.append("🕵️ Initiate deeper investigation of communication context.")
        steps.append("🔗 Map relationship network around this source.")

    if not steps:
        steps.append("✅ No immediate action required — continue routine monitoring.")
        steps.append("📊 Log for trend analysis and baseline comparison.")

    return steps


def analyze_text(
    text: str,
    anonymize: bool = True,
    source: str = "Text Input",
    api_key: Optional[str] = None,
    use_claude: bool = False,
) -> dict:
    """
    Primary analysis function.

    Returns a rich result dict with risk score, categories, explanation,
    entities, sentiment, and mitigation steps.
    """
    start = time.time()

    if not text or not text.strip():
        return {"error": "Empty input provided."}

    # Anonymize PII if requested
    processed_text = _anonymize(text) if anonymize else text

    # Pattern-based analysis
    pattern_score, hits = _pattern_score(processed_text)
    entities = _extract_entities(processed_text)
    sentiment, sentiment_strength = _sentiment_score(processed_text)

    # Boost score for entity presence
    entity_boost = (
        len(entities.get("weapons", [])) * 8 +
        len(entities.get("threat_terms", [])) * 10 +
        len(entities.get("location_risk", [])) * 4
    )
    raw_score = min(97.0, pattern_score + entity_boost)

    # Claude API enhancement (if configured)
    claude_reasoning = None
    if use_claude and api_key:
        claude_reasoning = _analyze_with_claude(processed_text, raw_score, api_key)

    # Final risk calculations
    risk_score = raw_score
    risk_level = _risk_level(risk_score)
    categories = [k.replace("_", " ").title() for k in hits.keys()]

    explanation = _build_explanation(risk_score, hits, entities, sentiment)
    if claude_reasoning:
        explanation = f"**AI Analysis:** {claude_reasoning}\n\n**Pattern Analysis:** {explanation}"

    mitigation = _mitigation_steps(hits, risk_score)

    # Content hash for deduplication (privacy-safe)
    content_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

    result = {
        "id": f"SENT-{random.randint(10000,99999)}",
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "content_preview": text[:200] + ("..." if len(text) > 200 else ""),
        "content_hash": content_hash,
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "flagged": risk_score >= 30,
        "categories": categories,
        "entities": entities,
        "sentiment": sentiment,
        "sentiment_strength": round(sentiment_strength, 2),
        "language": "English",  # Would use langdetect in production
        "pattern_hits": {k: v for k, v in hits.items()},
        "explanation": explanation,
        "mitigation_steps": mitigation,
        "processing_time_ms": round((time.time() - start) * 1000, 1),
        "anonymized": anonymize,
        "model": "SentinelAI Pattern Engine" + (" + Claude" if claude_reasoning else ""),
    }

    logger.info(
        f"Analyzed [{result['id']}]: risk={risk_score:.1f} level={risk_level} "
        f"categories={categories} time={result['processing_time_ms']}ms"
    )

    return result


def _analyze_with_claude(text: str, pattern_score: float, api_key: str) -> Optional[str]:
    """
    Enhance analysis with Claude API for contextual reasoning.
    Returns Claude's analysis text or None on failure.
    """
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""You are a cybersecurity and threat intelligence analyst. Analyze the following text for potential threats, harmful intent, or suspicious content. 

Text to analyze:
<text>{text}</text>

Pattern analysis has given this a preliminary risk score of {pattern_score:.1f}/100.

Provide a concise 2-3 sentence analysis covering:
1. Your assessment of the actual threat level and why
2. Any nuance or context the pattern matching may have missed
3. Whether the pattern score seems appropriate

Be analytical, not alarmist. Focus on genuine risks."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        logger.warning(f"Claude API call failed: {e}")
        return None


def generate_live_feed_item() -> dict:
    """Generate a simulated live feed message for the monitoring dashboard."""
    import random

    samples = [
        ("Just checking in — everything okay on your end?", 5),
        ("URGENT: Verify your banking credentials immediately or account suspended.", 78),
        ("The quarterly report looks great, well done team.", 4),
        ("We need to talk. Meet me at the old warehouse at midnight. Delete this.", 72),
        ("Malware sample exfiltrating financial records from internal server.", 88),
        ("Happy to share the project update with everyone!", 6),
        ("Explosive devices rigged at three locations. Ready for signal.", 95),
        ("Can someone send me the API documentation link?", 3),
        ("They won't know what hit them. I have access to their systems.", 82),
        ("Great work on the presentation! See you at the conference.", 5),
        ("BREAKING: Source claims government suppressing cure — share before deleted!", 61),
        ("New zero-day exploit available for financial sector targets. $50k.", 91),
        ("Traffic's bad today, working from home this afternoon.", 2),
        ("The package will cross the border tonight. No records.", 69),
        ("Feeling anxious about the deadline but we'll manage it.", 8),
    ]

    text, base_score = random.choice(samples)
    noise = random.uniform(-5, 5)
    score = max(0, min(100, base_score + noise))

    return {
        "id": f"LIVE-{random.randint(10000,99999)}",
        "timestamp": datetime.now().isoformat(),
        "source": random.choice(["Twitter/X Stream", "Telegram Monitor", "Chat Simulator", "News Feed", "Email Gateway"]),
        "content_preview": text,
        "risk_score": round(score, 1),
        "risk_level": _risk_level(score),
        "flagged": score >= 30,
        "categories": _quick_categories(text),
        "sentiment": "Negative" if score > 50 else ("Positive" if score < 20 else "Neutral"),
        "language": "English",
    }


def _quick_categories(text: str) -> list[str]:
    text_lower = text.lower()
    cats = []
    if any(w in text_lower for w in ["kill", "explosive", "attack", "weapon"]):
        cats.append("Violence")
    if any(w in text_lower for w in ["malware", "exploit", "hack", "zero-day"]):
        cats.append("Cybersecurity")
    if any(w in text_lower for w in ["verify", "suspended", "urgent", "credentials"]):
        cats.append("Phishing")
    if any(w in text_lower for w in ["suppressed", "breaking", "share before"]):
        cats.append("Misinformation")
    if any(w in text_lower for w in ["warehouse", "border", "package", "midnight"]):
        cats.append("Suspicious Activity")
    return cats
