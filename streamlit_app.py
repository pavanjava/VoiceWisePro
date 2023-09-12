import streamlit as st
from core.FileUploadHandler import handle_upload_files
from core.SummarizerAndTranslator import transcribe_audio
import os

st.title("🦜 Langchain + OpenAI - Audio Transcription and Summarization")

with st.sidebar:
    st.title('🦜 OpenAI API Key')
    if 'api_key' in st.secrets and len(st.secrets['api_key']) > 0 and str(st.secrets['api_key']).startswith('sk-'):
        st.success('API key already provided!', icon='✅')
        openai_api_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        openai_api_api = st.text_input('Enter OpenAI API Key:', type='password')
        if not (openai_api_api.startswith('sk-') and len(openai_api_api) > 0):
            st.warning('Please enter your openai key!', icon='⚠️')
        else:
            st.success('Proceed to uploading your audio file!', icon='✅')
    os.environ['api_key'] = openai_api_api

uploaded_file = st.file_uploader("Choose a [.mp3, .mp4, .wav, .webm] file", accept_multiple_files=False)
file = handle_upload_files(uploaded_file)
transcribe_audio(file_path=file)





