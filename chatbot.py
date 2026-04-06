"""
chatbot.py — WhatsApp-style Chat Interface
Renders chat history, quick-action buttons, language selector,
voice input, and the message input box.
"""

import streamlit as st
from datetime import datetime
from responses import get_response
from voice_utils import render_voice_button, text_to_speech
from auth import logout


QUICK_ACTIONS = {
    "English": [
        ("💰", "Check Account Balance"),
        ("📋", "Recent Transactions"),
        ("🏠", "Loan Details"),
        ("💳", "Credit Card Details"),
        ("📈", "Fixed Deposit details"),
        ("📍", "Branch Location near me"),
        ("🎧", "Contact Customer Support"),
        ("🚨", "Report a fraud"),
        ("💸", "UPI Payment help"),
        ("📊", "Interest Rates"),
    ],
    "Hindi": [
        ("💰", "खाता शेष जांचें"),
        ("📋", "हाल के लेनदेन"),
        ("🏠", "ऋण विवरण"),
        ("💳", "क्रेडिट कार्ड"),
        ("📈", "सावधि जमा"),
        ("📍", "शाखा स्थान"),
        ("🎧", "ग्राहक सेवा"),
        ("🚨", "धोखाधड़ी रिपोर्ट"),
    ],
    "Telugu": [
        ("💰", "ఖాతా నిల్వ తనిఖీ"),
        ("📋", "ఇటీవలి లావాదేవీలు"),
        ("🏠", "రుణ వివరాలు"),
        ("💳", "క్రెడిట్ కార్డ్"),
        ("📈", "స్థిర డిపాజిట్లు"),
        ("📍", "శాఖ స్థానం"),
        ("🎧", "కస్టమర్ సపోర్ట్"),
        ("🚨", "మోసం నివేదించు"),
    ],
}


def get_timestamp():
    return datetime.now().strftime("%I:%M %p")


def render_sidebar(user: dict):
    """Sidebar with user info, navigation, language picker, logout."""
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="text-align:center; padding:1rem 0 0.5rem;">
            <div style="font-size:2.5rem;">🏦</div>
            <h2 style="color:#1e40af; margin:0.3rem 0 0; font-size:1.4rem;">NeoBank</h2>
            <p style="color:#64748b; font-size:0.8rem; margin:0;">AI Banking Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # User card
        initials = "".join([n[0] for n in user["full_name"].split()[:2]]).upper()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#1e40af,#7c3aed);
                    border-radius:14px; padding:1rem; color:white; margin-bottom:0.8rem;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <div style="width:42px; height:42px; border-radius:50%;
                            background:rgba(255,255,255,0.25); display:flex;
                            align-items:center; justify-content:center;
                            font-weight:700; font-size:1rem;">{initials}</div>
                <div>
                    <div style="font-weight:600; font-size:0.95rem;">{user['full_name']}</div>
                    <div style="font-size:0.75rem; opacity:0.8;">A/C: {user['acct_no']}</div>
                </div>
            </div>
            <div style="font-size:0.72rem; opacity:0.75; margin-bottom:2px;">Available Balance</div>
            <div style="font-size:1.4rem; font-weight:800;">₹ 1,42,580.00</div>
        </div>
        """, unsafe_allow_html=True)

        # Language selector
        st.markdown("**🌍 Language / भाषा / భాష**")
        lang_options = ["🇬🇧 English", "🇮🇳 Hindi", "🇮🇳 Telugu"]
        lang_map = {"🇬🇧 English": "English", "🇮🇳 Hindi": "Hindi", "🇮🇳 Telugu": "Telugu"}
        curr = st.session_state.language
        disp = [k for k, v in lang_map.items() if v == curr][0]
        selected = st.radio("", lang_options, index=lang_options.index(disp),
                            label_visibility="collapsed", key="lang_radio")
        new_lang = lang_map[selected]
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()

        st.divider()

        # Voice toggle
        st.markdown("**🎤 Voice Assistant**")
        if "voice_enabled" not in st.session_state:
            st.session_state.voice_enabled = False
        st.session_state.voice_enabled = st.toggle(
            "Enable voice responses", value=st.session_state.voice_enabled
        )

        st.divider()

        # Stats
        st.markdown("**📊 Session Info**")
        st.caption(f"Messages: {len(st.session_state.chat_history)}")
        st.caption(f"Language: {st.session_state.language}")
        st.caption(f"Session: {datetime.now().strftime('%d %b %Y')}")

        st.divider()

        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()


def render_chat_messages():
    """Render all messages in WhatsApp bubble style."""
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center; padding:3rem 1rem; color:#94a3b8;">
            <div style="font-size:3rem; margin-bottom:0.8rem;">🏦</div>
            <h3 style="color:#64748b; font-weight:600;">Welcome to NeoBank Assistant</h3>
            <p style="font-size:0.9rem;">Use the quick-action buttons or type your query below</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-row user-row">
                <div class="bubble user-bubble">
                    <div class="bubble-content">{msg['content']}</div>
                    <div class="bubble-time">{msg['time']} ✓✓</div>
                </div>
                <div class="avatar user-avatar">{msg.get('initials','U')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row bot-row">
                <div class="avatar bot-avatar">🤖</div>
                <div class="bubble bot-bubble">
                    <div class="bubble-content">{msg['content']}</div>
                    <div class="bubble-time">{msg['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def process_input(text: str, user: dict):
    """Process user query and add both messages to history."""
    if not text.strip():
        return
    initials = "".join([n[0] for n in user["full_name"].split()[:2]]).upper()
    st.session_state.chat_history.append({
        "role": "user", "content": text,
        "time": get_timestamp(), "initials": initials
    })
    response = get_response(text, user, st.session_state.language)
    st.session_state.chat_history.append({
        "role": "bot", "content": response,
        "time": get_timestamp()
    })
    if st.session_state.get("voice_enabled"):
        text_to_speech(response, st.session_state.language)


def show_chat_interface():
    """Main chat page rendered after login."""
    user = st.session_state.user
    render_sidebar(user)

    # Header
    st.markdown(f"""
    <div class="chat-header">
        <span style="font-size:1.8rem;">🤖</span>
        <div>
            <div class="header-name">NeoBank AI Assistant</div>
            <div class="header-status">● Online — Secure Banking Support</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick actions
    lang = st.session_state.language
    actions = QUICK_ACTIONS.get(lang, QUICK_ACTIONS["English"])
    cols_per_row = 4
    rows = [actions[i:i+cols_per_row] for i in range(0, len(actions), cols_per_row)]
    st.markdown('<div class="quick-actions-label">⚡ Quick Actions</div>', unsafe_allow_html=True)
    for row in rows:
        cols = st.columns(len(row))
        for col, (icon, label) in zip(cols, row):
            with col:
                if st.button(f"{icon} {label}", key=f"qa_{label}", use_container_width=True):
                    process_input(label, user)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat window
    chat_container = st.container(height=420, border=True)
    with chat_container:
        render_chat_messages()

    # Voice + Text input
    col_voice, col_input, col_send = st.columns([1, 6, 1])

    with col_voice:
        voice_text = render_voice_button(lang)
        if voice_text:
            process_input(voice_text, user)
            st.rerun()

    with col_input:
        user_text = st.chat_input("Type your banking query here...", key="chat_input")

    if user_text:
        process_input(user_text, user)
        st.rerun()

    # Clear chat
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
