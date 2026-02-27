# 🛡️ SentinelAI — Smarter Defence Through Innovation

> **A full-stack AI-powered threat intelligence and content analysis platform built with Python, Streamlit, and Claude AI.**

![SentinelAI Banner](https://via.placeholder.com/1200x300/050a0f/00c8ff?text=SentinelAI+%E2%80%94+Defence+Intelligence+Platform)

---

## 🎯 Overview

SentinelAI is a professional-grade security intelligence platform that detects harmful, suspicious, and risky content using multi-dimensional AI analysis. It provides real-time monitoring, explainable AI insights, and actionable mitigation recommendations — all while maintaining a **privacy-first architecture**.

### Key Capabilities

- **Multi-source threat detection** — text messages, documents, live feeds, social media streams
- **AI-powered analysis** — pattern matching + Claude AI for contextual reasoning
- **Real-time monitoring** — live dashboard with auto-refresh
- **Explainable AI** — every flagged item comes with detailed reasoning
- **Privacy-first** — in-memory processing, PII anonymization, no persistent storage
- **Export & reporting** — CSV, JSON, and text intelligence briefs

---

## 🏗️ Architecture

```
sentinelai/
├── app.py                      # Main Streamlit entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker support
├── docker-compose.yml          # Docker Compose config
├── .env.example               # Environment variable template
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── ui/                        # User interface layer
│   ├── theme.py               # Dark military-grade theme & CSS
│   ├── sidebar.py             # Navigation sidebar
│   └── pages/
│       ├── dashboard.py       # Home Dashboard (KPIs, charts, alerts)
│       ├── live_monitoring.py # Live feed monitoring & streaming
│       ├── analysis_studio.py # Deep investigation + AI Copilot
│       ├── threat_intelligence.py # Trends, heatmaps, network
│       └── reports.py         # Export & recommendations
│
├── services/
│   └── analyzer.py           # Core AI threat analysis engine
│
├── utils/
│   ├── session_state.py      # Streamlit session management
│   └── logger.py             # Logging configuration
│
└── data/
    └── sample_dataset.json   # Sample labeled dataset
```

### Analysis Engine (services/analyzer.py)

The analysis pipeline uses multiple detection layers:

1. **Pattern Matching** — Regex-based detection of 7 threat categories
2. **Entity Extraction** — Weapon, threat, and location risk terms
3. **Sentiment Analysis** — Positive/negative/neutral classification
4. **Claude AI Enhancement** — Optional contextual reasoning via API
5. **Explainable Output** — Human-readable reasoning for every decision
6. **Mitigation Generation** — Actionable response recommendations

---

## 📋 Pages

| Page | Description |
|------|-------------|
| 🏠 Home Dashboard | KPIs, risk timeline, category heatmap, alerts, system health |
| 📡 Live Monitoring | Streaming feed, real-time detection, auto-refresh, quick analyze |
| 🔬 Analysis Studio | Text/document analysis, AI Copilot chat, investigation history |
| 🗺️ Threat Intelligence | Trends, geographic heatmap, entity network, early warning |
| 📊 Reports & Insights | Summary reports, CSV/JSON export, AI recommendations |

---

## 🚀 Quick Start

### Option 1: Local Python

```bash
# Clone / extract the project
cd sentinelai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional)
cp .env.example .env
# Edit .env to add your ANTHROPIC_API_KEY

# Run the application
streamlit run app.py
```

Open your browser to **http://localhost:8501**

### Option 2: Docker

```bash
# Build and run
docker-compose up --build

# Or with Docker directly
docker build -t sentinelai .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your-key sentinelai
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude AI API key | — |
| `DEFAULT_ANONYMIZE` | Enable PII anonymization | `true` |
| `DEFAULT_LOCAL_MODE` | Process locally only | `true` |
| `CRITICAL_THRESHOLD` | Score for CRITICAL level | `75` |
| `HIGH_THRESHOLD` | Score for HIGH level | `55` |
| `MEDIUM_THRESHOLD` | Score for MEDIUM level | `30` |

### API Key Setup

1. Get an API key at [console.anthropic.com](https://console.anthropic.com)
2. Add it in the sidebar under "AI Provider" → Anthropic API Key
3. Enable "Use Claude AI" in Analysis Studio for enhanced reasoning

*Without an API key, the platform runs entirely locally using the built-in pattern engine.*

---

## 🔐 Privacy & Security

SentinelAI is built with **privacy-by-design** principles:

| Feature | Status |
|---------|--------|
| PII Anonymization | ✅ Automatic (emails, IPs, phones) |
| Temporary Processing | ✅ In-memory only by default |
| No Persistent Storage | ✅ Session data cleared on restart |
| Local Processing Mode | ✅ No external API calls required |
| Content Hashing | ✅ SHA-256 for deduplication |
| User Consent Toggle | ✅ Privacy controls in sidebar |

---

## 🧠 AI Features

| Feature | Implementation |
|---------|---------------|
| NLP Threat Detection | Regex + Claude AI |
| Toxicity Classification | Pattern matching engine |
| Misinformation Detection | Keyword/phrase patterns |
| Behavioral Anomaly | Statistical deviation detection |
| Sentiment Analysis | Lexicon-based scoring |
| Named Entity Detection | Term matching + categorization |
| Explainable AI | Human-readable reasoning generation |
| Predictive Scoring | Trend extrapolation |
| Multi-language Support | Architecture ready (langdetect optional) |
| AI Copilot | Claude-powered chat interface |
| Early Warning System | Velocity and pattern analysis |

---

## 📊 Risk Scoring

| Level | Score Range | Action |
|-------|-------------|--------|
| 🟢 SAFE | 0–9 | No action required |
| 🔵 LOW | 10–29 | Monitor and log |
| 🟡 MEDIUM | 30–54 | Flag for review |
| 🟠 HIGH | 55–74 | Urgent analyst review |
| 🔴 CRITICAL | 75–100 | Immediate escalation |

---

## 📦 Sample Dataset

`data/sample_dataset.json` contains 10 labeled examples:

- 3 benign messages
- 2 phishing/social engineering
- 2 critical threats (violence, cybersecurity)
- 1 misinformation sample
- 1 suspicious activity
- 1 hate speech example

Use these in **Analysis Studio → Document Upload** to test the platform.

---

## 🔧 Extending SentinelAI

### Adding New Threat Categories

Edit `services/analyzer.py` → `PATTERNS` dictionary:

```python
PATTERNS["new_category"] = [
    r"\b(keyword1|keyword2)\b",
    r"your pattern here",
]
```

### Integrating Additional AI Models

The `analyze_text()` function accepts an `api_key` parameter. To add a new provider, create a new function similar to `_analyze_with_claude()` and call it in the pipeline.

### Custom Data Sources

Connect real data sources by replacing `generate_live_feed_item()` in `services/analyzer.py` with your actual feed ingestion logic (API calls, WebSocket, etc.).

---

## 📜 License

MIT License — for educational and authorized security purposes only.

**⚠️ Important:** This platform is designed for legitimate security monitoring with proper authorization. Ensure compliance with applicable laws and regulations in your jurisdiction. Always obtain proper consent before monitoring communications.

---

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io) — Web application framework
- [Plotly](https://plotly.com) — Interactive visualizations
- [Claude AI](https://anthropic.com) — AI reasoning and analysis
- [Rajdhani](https://fonts.google.com/specimen/Rajdhani) + [Share Tech Mono](https://fonts.google.com/specimen/Share+Tech+Mono) fonts

---

*SentinelAI — Smarter Defence Through Innovation* 🛡️
