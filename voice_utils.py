"""
voice_utils.py — Voice Assistant Module
Speech-to-Text (SpeechRecognition) + Text-to-Speech (pyttsx3)
Falls back gracefully if hardware/libraries are unavailable.
"""

import streamlit as st

# ─── Speech Recognition ───────────────────────────────────────────────────────

def speech_to_text(language: str = "English") -> str:
    """
    Capture microphone input and return transcribed text.
    Returns empty string on failure.

    Language codes:
        English → en-IN
        Hindi   → hi-IN
        Telugu  → te-IN
    """
    lang_code = {"English": "en-IN", "Hindi": "hi-IN", "Telugu": "te-IN"}.get(language, "en-IN")

    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 0.8

        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)

        st.info("🔄 Processing speech...")
        text = recognizer.recognize_google(audio, language=lang_code)
        return text

    except ImportError:
        st.warning("⚠️ SpeechRecognition library not installed. Run: pip install SpeechRecognition pyaudio")
        return ""
    except Exception as e:
        st.warning(f"Voice input error: {e}")
        return ""


# ─── Text-to-Speech ───────────────────────────────────────────────────────────

def text_to_speech(text: str, language: str = "English"):
    """
    Convert text to speech output using pyttsx3.
    Strips markdown symbols before speaking.
    """
    import re
    # Strip markdown for clean speech
    clean = re.sub(r"[*_`#|\[\]()]", "", text)
    clean = re.sub(r"\|.*?\|", "", clean)       # Remove table pipes
    clean = re.sub(r"\n{2,}", ". ", clean)
    clean = re.sub(r"\n", ", ", clean)
    clean = clean[:500]                          # Keep speech short

    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 155)
        engine.setProperty("volume", 0.95)

        # Try to pick a language-appropriate voice
        voices = engine.getProperty("voices")
        if language == "Hindi":
            for v in voices:
                if "hindi" in v.name.lower() or "hi" in v.id.lower():
                    engine.setProperty("voice", v.id)
                    break
        elif language == "Telugu":
            for v in voices:
                if "telugu" in v.name.lower() or "te" in v.id.lower():
                    engine.setProperty("voice", v.id)
                    break

        engine.say(clean)
        engine.runAndWait()
        engine.stop()

    except ImportError:
        st.warning("⚠️ pyttsx3 not installed. Run: pip install pyttsx3")
    except Exception as e:
        st.warning(f"Voice output error: {e}")


# ─── Voice Button UI ─────────────────────────────────────────────────────────

def render_voice_button(language: str) -> str:
    """
    Renders a voice-input button in Streamlit.
    Returns transcribed text or empty string.
    """
    result = ""
    if st.button("🎤 Voice Input", key="voice_btn", help="Click to speak your query"):
        result = speech_to_text(language)
        if result:
            st.success(f"✅ Heard: *{result}*")
    return result
