import os
import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title="ElevenLabs Text to Speech", page_icon="🔊")
st.title("🔊 ElevenLabs Text-to-Speech")

# Check API Key
if not api_key:
    st.error("ELEVENLABS_API_KEY not found in .env file.")
    st.stop()

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# User input
text = st.text_area("Enter text", height=180)

voice_id = st.text_input(
    "Voice ID",
    value="JBFqnCBsd6RMkjVDRZzb"
)

# Generate speech
if st.button("Generate Speech"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text
        )

        # Create output folder if it doesn't exist
        os.makedirs("output", exist_ok=True)

        out_path = "output/output.mp3"

        # Save audio
        with open(out_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)

        st.success("Speech generated successfully!")
        st.audio(out_path)

        with open(out_path, "rb") as f:
            st.download_button(
                label="Download MP3",
                data=f,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )