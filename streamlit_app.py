import streamlit as st
from core.FileUploadHandler import handle_upload_files
from core.SummarizerAndTranslator import transcribe_audio, qa_retrieval, Globals
import os

st.title("🦜 Langchain + OpenAI - Audio Transcription, Question and Answer Application")

with st.sidebar:
    st.title('🦜 OpenAI API Key')
    if 'api_key' in st.secrets and len(st.secrets['api_key']) > 0 and str(st.secrets['api_key']).startswith('sk-'):
        st.success('API key already provided!', icon='✅')
        openai_api_key = st.secrets['api_key']
    else:
        openai_api_key = st.text_input('Enter OpenAI API Key:', type='password')
        if not (openai_api_key.startswith('sk-') and len(openai_api_key) > 0):
            st.warning('Please enter your openai key!', icon='⚠️')
        else:
            st.success('Proceed to uploading your audio file!', icon='✅')
        os.environ['OPENAI_API_KEY'] = openai_api_key

uploaded_file = st.sidebar.file_uploader("Choose a [.mp3, .mp4, .wav, .webm] file", accept_multiple_files=False)

file = handle_upload_files(uploaded_file)

if Globals.transcribed_audio_response is None:
    print(Globals.transcribed_audio_response)
    transcript = transcribe_audio(file_path=file)
    Globals.transcribed_audio_response = transcript
    if transcript is not None:
        st.sidebar.success("Audio transcribed successfully, please ask your questions now")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating OpenAI response
def question_and_answer_routine(prompt_input):
    return qa_retrieval(prompt=prompt_input, transcript=Globals.transcribed_audio_response)


# User-provided prompt
if prompt := st.chat_input(disabled=not openai_api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = question_and_answer_routine(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)





