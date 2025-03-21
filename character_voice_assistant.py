import os
import time
import tempfile
import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai  # Google Gemini AI API

genai.configure(api_key="AIzaSyAVADR9Ye6Q19Qztbc3kQ8kIQJvh507t2Y")  

# ✅ Set Streamlit Page Config
st.set_page_config(page_title="AI Character Voice Assistant", page_icon="🎭", layout="wide")

# ✅ Character Definitions
CHARACTERS = {
    "Karen": {
        "name": "Ken the Karen",
        "backstory": "He is a rude and entitled customer, who is all about himself.",
        "voice_properties": {"rate": 190, "volume": 2.0},
        "emoji": "🤷🏻‍♂️😡"
    },
    "butler": {
        "name": "James the Butler",
        "backstory": "A sophisticated, formal British butler with impeccable manners.",
        "voice_properties": {"rate": 150, "volume": 2.0},
        "emoji": "🤵🏻🛎️"
    },
    "comedian": {
        "name": "Flin the funny guy",
        "backstory": "A stand-up comedian who turns everything into a joke.",
        "voice_properties": {"rate": 175, "volume": 0.9},
        "emoji": "👦🏼😂"
    },
    "grandpa": {
        "name": "Gary the grandpa",
        "backstory": "A knowledgable, caring grandfather who loves to give advice and tell stories.He is a very intellectual person.",
        "voice_properties": {"rate": 150, "volume": 0.7},
        "emoji": "👴🏻📖"
    }
}

# ✅ Initialize session state
if "character" not in st.session_state:
    st.session_state.character = "karen"
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""

# ✅ Function: Convert text to speech
def text_to_speech(text, voice_properties):
    engine = pyttsx3.init()
    engine.setProperty("rate", voice_properties["rate"])
    engine.setProperty("volume", voice_properties["volume"])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        temp_filename = tmp_file.name
    engine.save_to_file(text, temp_filename)
    engine.runAndWait()
    with open(temp_filename, "rb") as audio_file:
        audio_bytes = audio_file.read()
    os.remove(temp_filename)
    return audio_bytes

# ✅ Function: Recognize speech from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.listening = True
        time.sleep(0.2)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)
        st.session_state.listening = False
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I couldn't understand what you said."
    except sr.RequestError:
        return "Speech recognition service error."

# ✅ Function: Generate AI-powered responses using Google's Gemini API
def generate_response(prompt):
    character = st.session_state.character
    system_prompt = f"You are {CHARACTERS[character]['name']}. Reply in their personality style."

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(f"{system_prompt}\nUser: {prompt}")
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ **LEFT PANEL: Character Selection**
with st.sidebar:
    st.header("🎭 Select Your Character")
    selected_character = st.selectbox(
        "Choose a character",
        list(CHARACTERS.keys()),
        format_func=lambda x: f"{CHARACTERS[x]['emoji']} {CHARACTERS[x]['name']}"
    )
    
    # Show Character Backstory
    st.markdown(f"""
    <div style="background-color:#ffcccc; padding:20px; border-radius:20px;">
        <h3 style="color:black;">{CHARACTERS[selected_character]['emoji']} {CHARACTERS[selected_character]['name']}</h3>
        <p style="color:black;">{CHARACTERS[selected_character]['backstory']}</p>
    </div>
    """, unsafe_allow_html=True)

    if selected_character != st.session_state.character:
        st.session_state.character = selected_character
        st.session_state.conversation = []

    if st.button("🔄 Reset Conversation"):
        st.session_state.conversation = []
        st.rerun()

# ✅ **RIGHT PANEL: Conversation Area**
st.markdown("<h2 style='text-align: center;'>💬 Conversation</h2>", unsafe_allow_html=True)

# Display Conversation
for msg in st.session_state.conversation:
    if msg["type"] == "user":
        st.markdown(f"🧑‍💻 **You:** {msg['content']}")
    else:
        st.markdown(f"{CHARACTERS[msg['character']]['emoji']} **{CHARACTERS[msg['character']]['name']}:** {msg['content']}")
        if "audio" in msg:
            st.audio(msg["audio"], format="audio/wav")

# ✅ **User Input Section**
st.markdown("<h3>🎙️ Your Message</h3>", unsafe_allow_html=True)
text_input = st.text_input("Type your message here", value=st.session_state.voice_input, key="user_input")

col_mic, col_send = st.columns([1, 5])

# ✅ Microphone Button
if col_mic.button("🎤 Speak"):
    try:
        voice_text = recognize_speech()
        st.session_state.voice_input = voice_text
        st.rerun()
    except Exception as e:
        st.error(f"Microphone Error: {str(e)}")

# ✅ Send Button
if col_send.button("🚀 Send") and text_input:
    st.session_state.conversation.append({"type": "user", "content": text_input})

    response = generate_response(text_input)
    audio_bytes = text_to_speech(response, CHARACTERS[st.session_state.character]["voice_properties"])

    st.session_state.conversation.append({
        "type": "assistant",
        "character": st.session_state.character,
        "content": response,
        "audio": audio_bytes
    })

    st.session_state.voice_input = ""
    st.rerun()
