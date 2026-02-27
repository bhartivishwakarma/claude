import streamlit as st


def render_awareness_page():
    st.title("📚 Security Awareness")
    st.markdown("---")

    with st.expander("🎣 Phishing Tips", expanded=True):
        st.markdown(
            """
        **How to Identify Phishing Attacks:**
        
        • Check sender email address - phishers often use similar-looking addresses
        • Hover over links before clicking - verify the actual URL destination
        • Look for urgency - "Act now!" or "Verify account" are red flags
        • Grammar and spelling errors - legitimate companies proofread emails
        • Unexpected attachments - never open unless you requested them
        • requests for sensitive info - banks never ask for passwords via email
        • Small details - logos, fonts, or colors may be slightly off
        • Verify independently - call the company directly using official numbers
        """
        )

    with st.expander("🔐 Password Hygiene"):
        st.markdown(
            """
        **Best Practices for Strong Passwords:**
        
        • Use 12+ characters - longer passwords are exponentially harder to crack
        • Mix character types - uppercase, lowercase, numbers, and symbols
        • Avoid common words - dictionary words and names are vulnerable
        • Don't reuse passwords - if one service is breached, others stay safe
        • Use passphrases - "BlueMoon$42Ocean" is stronger than "Pas5w0rd!"
        • Never share passwords - not even with IT support or management
        • Use password managers - tools like Bitwarden or 1Password are secure
        • Enable 2FA - add a second factor (authenticator app or security key)
        • Update regularly - change passwords if accounts are compromised
        • Watch for keyloggers - use on-screen keyboards on shared computers
        """
        )

    with st.expander("🌐 Safe Browsing"):
        st.markdown(
            """
        **Internet Safety Guidelines:**
        
        • Use HTTPS only - lock icon confirms encrypted connection
        • Keep software updated - patches fix known security vulnerabilities
        • Use antivirus software - protect against malware and ransomware
        • Disable auto-fill - prevents credential theft on compromised sites
        • Clear cookies regularly - reduces tracking and session hijacking
        • Use VPN on public WiFi - encrypts traffic on untrusted networks
        • Disable JavaScript - can prevent some attacks (be aware of site issues)
        • Check SSL certificates - verify website legitimacy before login
        • Avoid downloading from untrusted sources - malware distribution hubs
        • Report suspicious sites - help browsers and authorities identify threats
        """
        )

    with st.expander("📱 Mobile Security"):
        st.markdown(
            """
        **Protecting Your Mobile Devices:**
        
        • Use strong PIN or biometric - unlock protection is critical
        • Install from official stores - Apple App Store and Google Play only
        • Review app permissions - why does a flashlight need your location?
        • Keep OS updated - security patches are released regularly
        • Use mobile VPN - public WiFi poses significant risks
        • Enable remote wipe - find my phone features let you erase if stolen
        • Avoid jailbreaking/rooting - removes security controls
        • Be careful with public charging - USB charging cables can transfer data
        • Use app-level security - banking apps should have PIN protection
        • Backup sensitive data - to secure cloud storage, not public clouds
        """
        )

    st.markdown("---")
    st.info("💡 **Tip:** Stay informed about the latest threats. Follow cybersecurity news and update your knowledge regularly!")
