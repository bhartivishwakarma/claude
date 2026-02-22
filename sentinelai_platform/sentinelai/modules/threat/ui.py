import streamlit as st


def detect_threat_rule_based(text):
    text_lower = text.lower()

    high_risk_words = ["attack", "breach", "exploit", "malware", "ransomware"]
    medium_risk_words = ["suspicious", "unusual", "unknown", "unauthorized"]

    if any(word in text_lower for word in high_risk_words):
        return "HIGH", "Multiple critical threat indicators detected"
    elif any(word in text_lower for word in medium_risk_words):
        return "MEDIUM", "Some suspicious patterns identified"
    else:
        return "LOW", "No obvious threat indicators"


def render_threat_analysis_page():
    st.title("🧠 Threat Analysis AI")
    st.markdown("---")

    api_key = st.session_state.get("OPENAI_API_KEY")

    text = st.text_area(
        "Describe suspicious activity or potential threat",
        height=200,
        placeholder="Example: Multiple failed login attempts from unknown IP address...",
    )

    if st.button("Analyze Threat", use_container_width=True):
        if not text:
            st.warning("Please describe the suspicious activity")
            return

        if api_key:
            try:
                from openai import OpenAI

                client = OpenAI(api_key=api_key)

                with st.spinner("🔄 Analyzing with AI..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a cybersecurity analyst. Classify the threat risk as LOW, MEDIUM, or HIGH and provide a brief security assessment.",
                            },
                            {"role": "user", "content": text},
                        ],
                        max_tokens=400,
                        temperature=0.7,
                    )

                st.markdown("### AI Threat Assessment")
                st.write(response.choices[0].message.content)

            except ImportError:
                st.error("🔴 OpenAI library not installed. Run: pip install openai")
            except Exception as e:
                st.error(f"🔴 OpenAI API error: {str(e)}")
        else:
            st.info("📌 OpenAI API key not configured. Using rule-based detection...")
            risk_level, reason = detect_threat_rule_based(text)

            st.markdown("### Rule-Based Threat Assessment")

            if risk_level == "HIGH":
                st.error(f"🚨 **HIGH RISK** - {reason}")
            elif risk_level == "MEDIUM":
                st.warning(f"⚠️ **MEDIUM RISK** - {reason}")
            else:
                st.success(f"✅ **LOW RISK** - {reason}")

            st.info("Enable OpenAI in Settings for advanced AI-powered analysis")
