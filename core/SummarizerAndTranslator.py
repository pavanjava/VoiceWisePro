import openai
import os
import streamlit as st

openai.api_key = st.secrets.openai.api_key


def transcribe_audio(file_path):
    if file_path is not None:
        with open(file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            if transcript is not None:
                st.write(transcript)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(e.__cause__)
