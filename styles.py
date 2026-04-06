"""
styles.py — Global CSS Injection for Streamlit
Provides WhatsApp-style chat bubbles, header, and overall theming.
"""

import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Global ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 980px;
    }

    /* ── Chat Header ────────────────────────────────────── */
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 0.8rem;
        color: white;
        box-shadow: 0 4px 16px rgba(30,64,175,0.3);
    }

    .header-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: white;
    }

    .header-status {
        font-size: 0.78rem;
        color: #93c5fd;
    }

    /* ── Quick Actions ──────────────────────────────────── */
    .quick-actions-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Style quick-action buttons */
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button {
        background: white !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 20px !important;
        color: #334155 !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 0.3rem 0.5rem !important;
        transition: all 0.2s ease;
    }

    div[data-testid="column"] button:hover {
        background: #eff6ff !important;
        border-color: #93c5fd !important;
        color: #1e40af !important;
        transform: translateY(-1px);
    }

    /* ── Chat Bubbles ───────────────────────────────────── */
    .chat-row {
        display: flex;
        align-items: flex-end;
        gap: 8px;
        margin-bottom: 12px;
        animation: fadeIn 0.25s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .user-row { justify-content: flex-end; }
    .bot-row  { justify-content: flex-start; }

    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 700;
        flex-shrink: 0;
    }

    .bot-avatar {
        background: linear-gradient(135deg, #1e40af, #7c3aed);
        color: white;
        font-size: 1.1rem;
    }

    .user-avatar {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        font-size: 0.78rem;
    }

    .bubble {
        max-width: 72%;
        border-radius: 18px;
        padding: 10px 14px 6px;
        position: relative;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }

    .user-bubble {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
        border-bottom-right-radius: 4px;
    }

    .bot-bubble {
        background: white;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        border-bottom-left-radius: 4px;
    }

    .bubble-content {
        font-size: 0.88rem;
        line-height: 1.55;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* Make markdown tables in bot bubbles look clean */
    .bot-bubble table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        margin: 6px 0;
    }
    .bot-bubble th, .bot-bubble td {
        padding: 4px 8px;
        border-bottom: 1px solid #f1f5f9;
        text-align: left;
    }
    .bot-bubble th { font-weight: 600; color: #475569; }

    .bubble-time {
        font-size: 0.68rem;
        margin-top: 4px;
        text-align: right;
    }

    .user-bubble .bubble-time { color: rgba(255,255,255,0.65); }
    .bot-bubble  .bubble-time { color: #94a3b8; }

    /* ── Login Card ─────────────────────────────────────── */
    .login-wrapper {
        margin-top: 1rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8fafc;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #1e40af !important;
        color: white !important;
    }

    /* Form inputs */
    input[type="text"], input[type="password"], input[type="email"] {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        font-size: 0.9rem !important;
    }
    input:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 0 3px rgba(30,64,175,0.1) !important;
    }

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #1e40af, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.55rem 1rem !important;
        transition: all 0.2s;
    }
    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(30,64,175,0.35) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
    }
    [data-testid="stSidebar"] > div {
        padding: 0.8rem !important;
    }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }

    /* Chat input */
    .stChatInput textarea {
        border-radius: 22px !important;
        border: 1.5px solid #e2e8f0 !important;
        font-size: 0.9rem !important;
        padding: 10px 16px !important;
    }
    .stChatInput textarea:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 0 3px rgba(30,64,175,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
