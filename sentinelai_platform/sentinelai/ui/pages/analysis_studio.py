"""
SentinelAI — Analysis Studio Page
Deep-dive investigation with AI Copilot
"""

import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime
from services.analyzer import analyze_text


def render_analysis_studio():
    """Render the Analysis Studio."""

    st.markdown("""
    <div class="page-header">
        <div class="page-title">🔬 Analysis Studio</div>
        <div class="page-subtitle">Deep investigation · AI-powered threat intelligence · Explainable AI</div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Text Analysis",
        "📄 Document Upload",
        "🤖 AI Copilot",
        "🕵️ History",
    ])

    with tab1:
        _render_text_analysis()

    with tab2:
        _render_document_upload()

    with tab3:
        _render_ai_copilot()

    with tab4:
        _render_analysis_history()


def _render_text_analysis():
    col_input, col_results = st.columns([2, 3])

    with col_input:
        st.markdown('<div class="section-header">Input</div>', unsafe_allow_html=True)

        text_input = st.text_area(
            "Content to Analyze",
            height=200,
            placeholder="Enter text, message, or content to analyze for threats...\n\nExample:\n'URGENT: Your account has been suspended. Click here to verify your credentials immediately or lose access.'",
            label_visibility="collapsed",
            key="studio_text_input"
        )

        source = st.selectbox(
            "Source Type",
            ["Text Input", "Social Media Post", "Email", "Chat Message", "News Article", "Intelligence Report"],
            label_visibility="visible",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            use_claude = st.checkbox(
                "Use Claude AI",
                value=bool(st.session_state.get("anthropic_api_key")),
                help="Enhance analysis with Claude AI (requires API key in sidebar)",
            )
        with col_b:
            anon = st.checkbox(
                "Anonymize PII",
                value=st.session_state.get("anonymize", True),
            )

        analyze_btn = st.button("🔍 Analyze Threat", use_container_width=True, type="primary")

        # Quick examples
        st.markdown('<div class="section-header">Quick Examples</div>', unsafe_allow_html=True)
        examples = [
            ("⚠️ Phishing", "URGENT: Your PayPal account has been suspended. Verify your identity now: paypal-secure-verify.ru/confirm"),
            ("🔴 Violence", "They'll regret crossing me. I know where they live and I have what I need to make them pay."),
            ("💻 Malware", "New zero-day exploit targeting Windows authentication. Payload ready for deployment against financial sector."),
            ("✅ Benign", "Looking forward to our team lunch tomorrow at noon. See everyone there!"),
            ("📰 Disinfo", "BREAKING: Doctors are HIDING the real cure! Government suppressing this — share before it's deleted!"),
        ]
        for label, ex_text in examples:
            if st.button(label, use_container_width=True, key=f"ex_{label}"):
                st.session_state.studio_example = ex_text
                st.rerun()

        # Check for example injection
        if "studio_example" in st.session_state:
            text_input = st.session_state.pop("studio_example")

    with col_results:
        st.markdown('<div class="section-header">Analysis Results</div>', unsafe_allow_html=True)

        if analyze_btn and text_input.strip():
            with st.spinner("Running multi-dimensional threat analysis..."):
                api_key = st.session_state.get("anthropic_api_key", "")
                result = analyze_text(
                    text_input,
                    anonymize=anon,
                    source=source,
                    api_key=api_key if use_claude else None,
                    use_claude=use_claude and bool(api_key),
                )
                # Store for display
                st.session_state.last_result = result
                # Add to history
                st.session_state.analysis_history.insert(0, result)
                # Update global stats
                stats = st.session_state.get("global_stats", {})
                stats["total_analyzed"] = stats.get("total_analyzed", 0) + 1
                if result.get("flagged"):
                    stats["threats_detected"] = stats.get("threats_detected", 0) + 1
                    total = stats["total_analyzed"]
                    scores_sum = stats.get("_scores_sum", 0) + result["risk_score"]
                    stats["_scores_sum"] = scores_sum
                    stats["avg_risk_score"] = round(scores_sum / total, 1)
                st.session_state.global_stats = stats

        result = st.session_state.get("last_result")
        if result:
            _render_result_card(result)
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; border:1px dashed #1a3a5c; border-radius:8px;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">🔍</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; color:#4a7090; text-transform:uppercase; letter-spacing:0.1em;">
                    Awaiting Input
                </div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#2a4a5c; margin-top:0.3rem;">
                    Enter text and click Analyze to begin
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_result_card(result: dict):
    score = result.get("risk_score", 0)
    level = result.get("risk_level", "SAFE")
    level_css = level.lower()

    # Risk meter
    color = "#ff3b5c" if score > 75 else "#ffb300" if score > 55 else "#ff8c00" if score > 30 else "#00ffa3"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#4a7090",
                     "tickfont": {"family": "Share Tech Mono", "size": 9, "color": "#4a7090"}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#0d1e2e",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 10], "color": "#050a0f"},
                {"range": [10, 30], "color": "#071520"},
                {"range": [30, 55], "color": "#0a1f2e"},
                {"range": [55, 75], "color": "#0d1f28"},
                {"range": [75, 100], "color": "#1a0a10"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
        number={"font": {"family": "Rajdhani", "size": 42, "color": color}, "suffix": ""},
        title={"text": f"Risk Score", "font": {"family": "Rajdhani", "size": 13, "color": "#8ab0cc"}},
    ))

    fig.update_layout(
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=0),
        font=dict(color="#8ab0cc"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Risk level badge
    st.markdown(f"""
    <div style="text-align:center; margin: -0.5rem 0 0.8rem;">
        <span class="risk-badge risk-{level_css}" style="font-size:0.85rem; padding:4px 16px;">
            {level} RISK
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Categories
    cats = result.get("categories", [])
    if cats:
        badges = " ".join(f'<span style="background:#0d2a3a; border:1px solid #1a3a5c; border-radius:3px; padding:2px 8px; font-family:\'Share Tech Mono\',monospace; font-size:0.62rem; color:#8ab0cc; margin:2px;">{c}</span>' for c in cats)
        st.markdown(f'<div style="margin-bottom:0.8rem; text-align:center;">{badges}</div>', unsafe_allow_html=True)

    # Explanation
    st.markdown('<div class="section-header">AI Reasoning</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="copilot-bubble">
        <div class="copilot-label">⚙ Explainable AI Output</div>
        {result.get('explanation', 'No explanation available.')}
    </div>
    """, unsafe_allow_html=True)

    # Entities
    entities = result.get("entities", {})
    if entities:
        st.markdown('<div class="section-header">Detected Entities</div>', unsafe_allow_html=True)
        for ent_type, ent_list in entities.items():
            col_e1, col_e2 = st.columns([1, 3])
            with col_e1:
                st.markdown(f'<span style="font-family:\'Share Tech Mono\',monospace; font-size:0.65rem; color:#4a7090; text-transform:uppercase;">{ent_type.replace("_"," ")}</span>', unsafe_allow_html=True)
            with col_e2:
                tags = " ".join(f'<span style="background:#1a0a0a; border:1px solid #ff3b5c33; border-radius:2px; padding:1px 6px; font-family:\'Share Tech Mono\',monospace; font-size:0.62rem; color:#ff7090; margin:1px;">{e}</span>' for e in ent_list)
                st.markdown(tags, unsafe_allow_html=True)

    # Sentiment
    sentiment = result.get("sentiment", "Neutral")
    sent_color = "#ff3b5c" if sentiment == "Negative" else "#00ffa3" if sentiment == "Positive" else "#8ab0cc"
    st.markdown(f"""
    <div style="display:flex; gap:1rem; margin:0.5rem 0; font-family:'Share Tech Mono',monospace; font-size:0.65rem;">
        <span style="color:#4a7090;">SENTIMENT:</span>
        <span style="color:{sent_color};">{sentiment}</span>
        <span style="color:#4a7090; margin-left:auto;">PROCESSED IN {result.get('processing_time_ms',0)}ms</span>
        <span style="color:#4a7090;">MODEL: {result.get('model','N/A')}</span>
    </div>
    """, unsafe_allow_html=True)

    # Mitigation steps
    st.markdown('<div class="section-header">Recommended Actions</div>', unsafe_allow_html=True)
    for step in result.get("mitigation_steps", []):
        st.markdown(f"""
        <div style="background:#0a1a2a; border-left:2px solid #1a3a5c; border-radius:0 4px 4px 0;
                    padding:0.4rem 0.7rem; margin-bottom:0.3rem; font-family:'Exo 2',sans-serif;
                    font-size:0.82rem; color:#c8d8e8;">
            {step}
        </div>
        """, unsafe_allow_html=True)


def _render_document_upload():
    st.markdown('<div class="section-header">Upload Document for Analysis</div>', unsafe_allow_html=True)

    col_up, col_res = st.columns([1, 2])

    with col_up:
        uploaded_file = st.file_uploader(
            "Upload File",
            type=["txt", "md", "csv", "json", "log"],
            label_visibility="collapsed",
        )

        if uploaded_file:
            st.markdown(f"""
            <div style="background:#0d1e2e; border:1px solid #1a3a5c; border-radius:6px; padding:0.7rem; margin-top:0.5rem;">
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#4a7090; margin-bottom:4px;">FILE LOADED</div>
                <div style="font-family:'Exo 2',sans-serif; font-size:0.85rem; color:#00c8ff;">{uploaded_file.name}</div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; color:#8ab0cc; margin-top:2px;">
                    Size: {uploaded_file.size / 1024:.1f} KB · Type: {uploaded_file.type}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔍 Analyze Document", use_container_width=True, type="primary"):
                content = uploaded_file.read().decode("utf-8", errors="replace")
                # Chunk analysis for large docs
                chunks = [content[i:i+2000] for i in range(0, min(len(content), 10000), 2000)]

                with st.spinner(f"Analyzing {len(chunks)} chunk(s)..."):
                    results = []
                    for i, chunk in enumerate(chunks[:5]):
                        r = analyze_text(
                            chunk,
                            anonymize=st.session_state.get("anonymize", True),
                            source=f"Document: {uploaded_file.name}",
                        )
                        results.append(r)

                    st.session_state.doc_results = results
                    # Add highest-risk result to history
                    best = max(results, key=lambda x: x.get("risk_score", 0))
                    st.session_state.analysis_history.insert(0, best)
                    stats = st.session_state.get("global_stats", {})
                    stats["total_analyzed"] = stats.get("total_analyzed", 0) + len(results)
                    if any(r.get("flagged") for r in results):
                        stats["threats_detected"] = stats.get("threats_detected", 0) + 1
                    st.session_state.global_stats = stats

    with col_res:
        doc_results = st.session_state.get("doc_results", [])
        if doc_results:
            st.markdown('<div class="section-header">Document Analysis Results</div>', unsafe_allow_html=True)

            max_score = max(r.get("risk_score", 0) for r in doc_results)
            max_level = max(doc_results, key=lambda x: x.get("risk_score", 0)).get("risk_level", "SAFE")
            level_css = max_level.lower()

            st.markdown(f"""
            <div class="sentinel-card risk-{level_css}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-family:'Rajdhani',sans-serif; font-size:0.75rem; color:#4a7090;
                                    text-transform:uppercase; letter-spacing:0.1em;">Document Risk Assessment</div>
                        <div style="font-family:'Rajdhani',sans-serif; font-size:2rem; font-weight:700;
                                    color:{'#ff3b5c' if max_score>75 else '#ffb300' if max_score>55 else '#00ffa3'};">
                            {max_score:.1f}/100
                        </div>
                    </div>
                    <span class="risk-badge risk-{level_css}" style="font-size:0.9rem; padding:6px 16px;">{max_level}</span>
                </div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#4a7090; margin-top:8px;">
                    {len(doc_results)} chunk(s) analyzed · Highest risk chunk shown
                </div>
            </div>
            """, unsafe_allow_html=True)

            for i, r in enumerate(doc_results):
                lvl_css = r.get("risk_level", "SAFE").lower()
                with st.expander(f"Chunk {i+1} — Risk: {r.get('risk_score',0):.1f} ({r.get('risk_level','SAFE')})"):
                    st.markdown(f'<div class="copilot-bubble">{r.get("explanation","")}</div>', unsafe_allow_html=True)
                    for step in r.get("mitigation_steps", [])[:3]:
                        st.markdown(f"- {step}")
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; border:1px dashed #1a3a5c; border-radius:8px;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">📄</div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; color:#4a7090; text-transform:uppercase; letter-spacing:0.1em;">
                    Upload a Document
                </div>
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#2a4a5c; margin-top:0.3rem;">
                    Supports TXT, MD, CSV, JSON, LOG
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_ai_copilot():
    """AI Copilot chat interface for investigators."""

    st.markdown("""
    <div style="background:linear-gradient(135deg, #0a1f2e, #071520); border:1px solid #1a4a6c;
                border-radius:8px; padding:1rem 1.2rem; margin-bottom:1rem;">
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:600;
                    color:#00c8ff; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.3rem;">
            🤖 SentinelAI Copilot
        </div>
        <div style="font-family:'Exo 2',sans-serif; font-size:0.82rem; color:#8ab0cc; line-height:1.5;">
            Your AI-powered investigation assistant. Ask questions about threat analysis, get context-aware
            insights, or request deeper investigation into specific threats.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    chat_history = st.session_state.get("copilot_chat", [])

    # Chat display
    chat_container = st.container()
    with chat_container:
        if not chat_history:
            st.markdown("""
            <div class="copilot-bubble">
                <div class="copilot-label">🤖 Copilot · Ready</div>
                Hello, Analyst. I'm your SentinelAI Copilot. I can help you:
                <ul style="margin:0.5rem 0 0 1rem; color:#8ab0cc;">
                    <li>Investigate flagged content in detail</li>
                    <li>Explain threat categories and indicators</li>
                    <li>Suggest investigation strategies</li>
                    <li>Analyze behavioral patterns</li>
                    <li>Provide context-aware risk assessments</li>
                </ul>
                <br>What would you like to investigate?
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in chat_history:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    st.markdown(f"""
                    <div style="display:flex; justify-content:flex-end; margin-bottom:0.5rem;">
                        <div style="background:#0d2a3a; border:1px solid #1a5a7c; border-radius:8px 8px 0 8px;
                                    padding:0.6rem 0.9rem; max-width:75%; font-family:'Exo 2',sans-serif;
                                    font-size:0.85rem; color:#e8f4ff;">
                            {content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="copilot-bubble" style="margin-bottom:0.5rem;">
                        <div class="copilot-label">🤖 Copilot</div>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)

    # Input
    col_chat, col_send = st.columns([5, 1])
    with col_chat:
        user_input = st.text_input(
            "Message Copilot",
            placeholder="Ask the AI Copilot anything about threats, analysis, or investigation...",
            label_visibility="collapsed",
            key="copilot_input"
        )
    with col_send:
        send_btn = st.button("Send ➤", use_container_width=True)

    if send_btn and user_input.strip():
        # Add user message
        chat_history.append({"role": "user", "content": user_input})

        # Generate response
        with st.spinner("Copilot thinking..."):
            api_key = st.session_state.get("anthropic_api_key", "")
            response = _copilot_response(user_input, chat_history, api_key)
            chat_history.append({"role": "assistant", "content": response})
            st.session_state.copilot_chat = chat_history
        st.rerun()

    # Suggested questions
    suggestions = [
        "What makes a phishing attack effective?",
        "How do I investigate a suspicious IP?",
        "Explain the CRITICAL risk level threshold",
        "What are early warning signs of insider threats?",
        "How should I handle a CRITICAL threat alert?",
    ]

    st.markdown('<div class="section-header">Suggested Questions</div>', unsafe_allow_html=True)
    cols = st.columns(len(suggestions))
    for i, (col, sug) in enumerate(zip(cols, suggestions)):
        with col:
            if st.button(sug[:30] + "...", key=f"sug_{i}", use_container_width=True):
                chat_history.append({"role": "user", "content": sug})
                response = _copilot_response(sug, chat_history, st.session_state.get("anthropic_api_key", ""))
                chat_history.append({"role": "assistant", "content": response})
                st.session_state.copilot_chat = chat_history
                st.rerun()

    if st.button("🗑 Clear Conversation", key="clear_copilot"):
        st.session_state.copilot_chat = []
        st.rerun()


def _copilot_response(user_input: str, history: list, api_key: str) -> str:
    """Generate copilot response using Claude or local fallback."""

    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)

            # Build context from recent analysis
            recent = st.session_state.get("last_result")
            context = ""
            if recent:
                context = f"Recent analysis: Risk score {recent.get('risk_score')}, Level: {recent.get('risk_level')}, Categories: {recent.get('categories')}."

            messages = [{"role": m["role"], "content": m["content"]}
                        for m in history[-10:] if m["role"] in ("user", "assistant")]

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=f"""You are SentinelAI Copilot, an expert cybersecurity and threat intelligence AI assistant.
                You help security analysts investigate threats, understand risk indicators, and make better decisions.
                Be concise, analytical, and actionable. Use a professional but accessible tone.
                Current platform context: {context}
                Focus on practical intelligence and actionable insights.""",
                messages=messages,
            )
            return response.content[0].text
        except Exception as e:
            pass

    # Local fallback responses
    input_lower = user_input.lower()
    responses = {
        "phishing": "Phishing attacks exploit urgency, authority, and fear. Key indicators include: mismatched sender domains, urgent action required, generic greetings, suspicious links (hover to check URL), and requests for credentials. Our pattern engine flags these via social engineering rules.",
        "critical": "A CRITICAL risk score (75+) indicates high-confidence detection of imminent or severe threat indicators — violence, critical infrastructure threats, or confirmed malware. Immediate escalation to your security team is recommended. Document everything and preserve evidence.",
        "investigate": "Investigation workflow: 1) Preserve the content and source metadata, 2) Cross-reference with known threat actor TTPs, 3) Map entity relationships using the network graph, 4) Check for behavioral patterns over time, 5) Escalate if confidence is high.",
        "insider": "Insider threat indicators: unusual access times, mass data downloads, accessing restricted resources, communication with external parties about internal systems, and emotional indicators in communications. Our behavioral anomaly detection watches for deviations from baselines.",
        "false positive": "To reduce false positives: provide more context via the Analysis Studio, use the 'Benign' feedback option, and adjust sensitivity in settings. Our engine learns from corrections over time when in online learning mode.",
    }

    for key, response in responses.items():
        if key in input_lower:
            return response

    return (
        "Based on current threat intelligence patterns, I'd recommend examining the source context, "
        "cross-referencing against known threat actor TTPs, and considering the behavioral baseline. "
        "If you provide me with specific content or a risk report, I can give you a more targeted assessment. "
        "Would you like me to walk you through the investigation methodology?"
    )


def _render_analysis_history():
    history = st.session_state.get("analysis_history", [])

    if not history:
        st.info("No analysis history in this session.")
        return

    st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace; font-size:0.65rem; color:#4a7090; margin-bottom:0.8rem;">{len(history)} ITEMS IN HISTORY · SESSION ONLY · NO PERSISTENT STORAGE</div>', unsafe_allow_html=True)

    # Filter
    filter_flagged = st.checkbox("Show only flagged items", value=False)
    filtered = [r for r in history if r.get("flagged")] if filter_flagged else history

    for r in filtered[:20]:
        level = r.get("risk_level", "SAFE").lower()
        score = r.get("risk_score", 0)
        preview = r.get("content_preview", "")[:80]
        cats = ", ".join(r.get("categories", [])[:3]) or "None"
        ts = r.get("timestamp", "")
        try:
            ts_fmt = datetime.fromisoformat(ts).strftime("%m/%d %H:%M")
        except Exception:
            ts_fmt = ts[:10]

        with st.expander(f"[{r.get('risk_level','SAFE')}] {score:.0f}/100 — {preview[:50]}..."):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#8ab0cc;">
                    <div>ID: <span style="color:#00c8ff;">{r.get('id','N/A')}</span></div>
                    <div>Source: {r.get('source','N/A')}</div>
                    <div>Time: {ts_fmt}</div>
                    <div>Categories: {cats}</div>
                    <div>Sentiment: {r.get('sentiment','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-family:'Rajdhani',sans-serif; font-size:2.5rem; font-weight:700;
                                color:{'#ff3b5c' if score>75 else '#ffb300' if score>55 else '#ff8c00' if score>30 else '#00ffa3'};">
                        {score:.0f}
                    </div>
                    <span class="risk-badge risk-{level}">{r.get('risk_level','SAFE')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f'<div class="copilot-bubble" style="margin-top:0.5rem;">{r.get("explanation","")}</div>', unsafe_allow_html=True)
