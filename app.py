"""
NeoBank AI Banking Chatbot
Main Streamlit Application Entry Point
BTech Final Year Project
"""

import streamlit as st

st.set_page_config(
    page_title="NeoBank AI Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

from auth import show_login_page, show_register_page, logout
from chatbot import show_chat_interface
from styles import inject_css

# Inject global CSS
inject_css()

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Route to correct page
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        
        # Brand header
        st.markdown("""
        <div style="text-align:center; padding: 2rem 0 1rem;">
            <div style="font-size:3rem;">🏦</div>
            <h1 style="font-size:2rem; font-weight:800; color:#1e40af; margin:0.5rem 0 0.2rem;">NeoBank</h1>
            <p style="color:#64748b; font-size:0.95rem;">AI-Powered Banking Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Register"])
        with tab1:
            show_login_page()
        with tab2:
            show_register_page()

        st.markdown('</div>', unsafe_allow_html=True)
else:
    show_chat_interface()
