import openai
import os
import faiss
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQAWithSourcesChain


@st.cache_resource()
class Globals:
    transcribed_audio_response = None


@st.cache_resource()
def transcribe_audio(file_path):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if file_path is not None:
        print("Calling OpenAI Whisper")
        with open(file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            if transcript is not None:
                # st.write(transcript)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(e.__cause__)
                return transcript


def qa_retrieval(prompt, transcript):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Splitting the text
    textsplitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)

    texts = textsplitter.split_text(transcript.text)

    print("Calling OpenAI Embeddings")

    store = FAISS.from_texts(
        texts, OpenAIEmbeddings(), metadatas=[{"source": f"Text chunk {i} of {len(texts)}"} for i in range(len(texts))]
    )

    faiss.write_index(store.index, "docs.faiss")

    llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm, chain_type="stuff", retriever=store.as_retriever()
    )

    answer = chain({"question": prompt}, return_only_outputs=True)

    return answer["answer"]

