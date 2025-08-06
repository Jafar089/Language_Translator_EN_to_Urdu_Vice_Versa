import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# Streamlit app config
st.set_page_config(page_title="Real-Time Translator", layout="centered")
st.title("🎙️ Real-Time English ↔ Urdu Speech Translator")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Initialize recognizer
recognizer = sr.Recognizer()

# Language direction selector
mode = st.radio("Choose Translation Direction", ["English to Urdu", "Urdu to English"])

# ------------------------------
# 🎤 Voice Translation Section
# ------------------------------
st.subheader("🎤 Speak Now")

if st.button("Start Microphone"):
    with sr.Microphone() as source:
        st.info("Listening... Please speak clearly.")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)

            if mode == "English to Urdu":
                original = recognizer.recognize_google(audio, language='en-GB')
                translated = GoogleTranslator(source='en', target='ur').translate(original)
                tts_lang = 'ur'
            else:
                original = recognizer.recognize_google(audio, language='ur')
                translated = GoogleTranslator(source='ur', target='en').translate(original)
                tts_lang = 'en'

            # Show translation
            st.success(f"🗣 You said:\n**{original}**")
            st.success(f"🌐 Translation:\n**{translated}**")

            # Play translated audio
            tts = gTTS(translated, lang=tts_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')

            # Save to history
            st.session_state.conversation.append({
                "type": "Voice",
                "direction": mode,
                "original": original,
                "translated": translated
            })

        except sr.WaitTimeoutError:
            st.warning("⏳ No speech detected. Try again.")
        except sr.UnknownValueError:
            st.error("❌ Could not understand speech.")
        except Exception as e:
            st.error(f"❗ Error: {e}")

# ------------------------------
# 📝 Text Translation Section
# ------------------------------
st.subheader("📝 Type or Paste Text")

text_input = st.text_area("Enter sentence below:", "")

if st.button("Translate Text"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            if mode == "English to Urdu":
                translated = GoogleTranslator(source='en', target='ur').translate(text_input)
                tts_lang = 'ur'
            else:
                translated = GoogleTranslator(source='ur', target='en').translate(text_input)
                tts_lang = 'en'

            st.success(f"📝 Original:\n**{text_input}**")
            st.success(f"🌐 Translation:\n**{translated}**")

            # Play audio
            tts = gTTS(translated, lang=tts_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')

            # Save to history
            st.session_state.conversation.append({
                "type": "Text",
                "direction": mode,
                "original": text_input,
                "translated": translated
            })

        except Exception as e:
            st.error(f"❗ Error: {e}")

# ------------------------------
# 📜 Conversation History Section
# ------------------------------
st.markdown("---")
st.subheader("📜 Conversation History")

if st.button("🧹 Clear History"):
    st.session_state.conversation = []
    st.info("History cleared.")

for i, entry in enumerate(reversed(st.session_state.conversation), 1):
    entry_type = entry.get("type", "Unknown")
    direction = entry.get("direction", "Unknown")
    original = entry.get("original", "N/A")
    translated = entry.get("translated", "N/A")

    st.markdown(f"**{i}. [{entry_type}] {direction}**")
    st.markdown(f"- 🗣 Original: {original}")
    st.markdown(f"- 🌐 Translated: {translated}")
    st.markdown("---")
