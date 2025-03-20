# hackathon-code
Character voice assistant

AI Character Voice Assistant
Overview
A Streamlit web app to interact with AI-powered characters using voice or text. Each character has a unique personality and responds with text and audio.

**Features**

1.Characters: Karen, James the Butler, Chuckles, Grandma Willow.

2.Voice & Text Input: Speak or type your messages.

3.Text-to-Speech: Characters respond with audio.

4.Conversation History: View and reset chat.

**Installation**

1.Clone the repo:
git clone https://github.com/your-username/ai-character-voice-assistant.git
cd ai-character-voice-assistant

2.Install dependencies:
pip install -r requirements.txt
Add your Google Gemini API key in character_voice_assistant.py.

3.Run the app:
streamlit run character_voice_assistant.py

**Usage**

1.Select a character from the sidebar.

2.Speak or type your message.

3.Click "Send" to get a response.

4.Use "Reset Conversation" to start fresh.

**Dependencies**
-->streamlit, speechrecognition, pyttsx3, google-generativeai
