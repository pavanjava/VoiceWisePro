import streamlit as st
from core.FileUploadHandler import handle_upload_files
from core.SummarizerAndTranslator import transcribe_audio

st.title("🦜 Langchain + OpenAI - Audio Transcription and Summarization")
sidebar = st.sidebar
openai_api_key = sidebar.text_input("please enter your openai_api_key", type="password", value="")
uploaded_file = st.file_uploader("Choose a [.mp3, .mp4, .wav, .webm] file", accept_multiple_files=False)
if not (openai_api_key.startswith('sk-') and len(openai_api_key) > 0):
    file = handle_upload_files(uploaded_file)
    transcribe_audio(file_path=file)
else:
    raise Exception('OpenAI API key can not be empty')




