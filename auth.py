"""
auth.py — Login, Registration, and Session Management
Uses SQLite for persistent user storage with hashed passwords
"""

import sqlite3
import hashlib
import streamlit as st
from pathlib import Path

DB_PATH = Path(__file__).parent / "users.db"


# ─── Database Setup ────────────────────────────────────────────────────────────

def init_db():
    """Create users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    UNIQUE NOT NULL,
            full_name TEXT    NOT NULL,
            mobile    TEXT    NOT NULL,
            email     TEXT,
            password  TEXT    NOT NULL,
            acct_no   TEXT    NOT NULL,
            created   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Seed a demo user
    demo_pass = hash_password("demo1234")
    try:
        c.execute("""
            INSERT OR IGNORE INTO users (username, full_name, mobile, email, password, acct_no)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("demo", "Rajesh Kumar", "+91 98765 43210", "rajesh@demo.in", demo_pass, "SB00014521"))
    except Exception:
        pass
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0], "username": row[1], "full_name": row[2],
            "mobile": row[3], "email": row[4], "acct_no": row[6]
        }
    return None


def verify_credentials(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False


def register_user(username, full_name, mobile, email, password) -> tuple[bool, str]:
    """Returns (success, message)."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    import random
    acct_no = f"SB{random.randint(10000000, 99999999)}"
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (username, full_name, mobile, email, password, acct_no)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, full_name, mobile, email, hash_password(password), acct_no))
        conn.commit()
        conn.close()
        return True, "Account created successfully! Please sign in."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose another."
    except Exception as e:
        return False, str(e)


# ─── UI Components ─────────────────────────────────────────────────────────────

init_db()


def show_login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="e.g.  demo", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Password", key="login_pass")
        submitted = st.form_submit_button("Sign In 🔐", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        elif verify_credentials(username, password):
            user = get_user(username)
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.chat_history = []
            st.rerun()
        else:
            st.error("Invalid credentials. Try demo / demo1234")

    st.markdown("""
    <div style="text-align:center; margin-top:0.8rem; padding:0.7rem;
                background:#eff6ff; border-radius:10px; font-size:0.82rem; color:#1e40af;">
        <b>Demo Account:</b> &nbsp; Username: <code>demo</code> &nbsp; Password: <code>demo1234</code>
    </div>
    """, unsafe_allow_html=True)


def show_register_page():
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("register_form"):
        full_name = st.text_input("Full Name", placeholder="Priya Sharma")
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", placeholder="priya123")
        with col2:
            mobile = st.text_input("Mobile", placeholder="+91 99999 00000")
        email = st.text_input("Email (optional)", placeholder="priya@email.com")
        col3, col4 = st.columns(2)
        with col3:
            password = st.text_input("Password", type="password", placeholder="Min 6 chars")
        with col4:
            confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account ✨", use_container_width=True)

    if submitted:
        if not all([full_name, username, mobile, password]):
            st.error("Please fill all required fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, msg = register_user(username, full_name, mobile, email, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chat_history = []
    st.rerun()
