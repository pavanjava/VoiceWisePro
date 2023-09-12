import openai
import os
import streamlit as st


def transcribe_audio(file_path):
    openai.api_key = os.getenv("api_key")
    if file_path is not None:
        with open(file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            if transcript is not None:
                st.write(transcript)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(e.__cause__)
