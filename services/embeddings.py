import streamlit as st
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(texts):
    model = load_embedding_model()
    return model.encode(texts)