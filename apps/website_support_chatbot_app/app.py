import os

from dotenv import load_dotenv, find_dotenv
import streamlit as st

from utils import get_website_data_from_sitemap, split_data, get_embeddings, push_to_pinecone, pull_from_pinecone, get_similar_docs
import constants

load_dotenv(find_dotenv())

if 'HUGGINGFACEHUB_API_TOKEN' not in st.session_state:
    st.session_state['HUGGINGFACEHUB_API_TOKEN'] = os.getenv("HUGGINGFACEHUB_API_TOKEN") # 一旦バックエンドで入力させて挙動を見る
if 'PINECONE_API_KEY' not in st.session_state:
    st.session_state['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY") # 一旦バックエンドで入力させて挙動を見る
if 'PINECONE_ENVIRONMENT' not in st.session_state:
    st.session_state['PINECONE_ENVIRONMENT'] = os.getenv("PINECONE_ENVIRONMENT") # 一旦バックエンドで入力させて挙動を見る
if 'PINECONE_INDEX_NAME' not in st.session_state:
    st.session_state['PINECONE_INDEX_NAME'] = os.getenv("PINECONE_INDEX_NAME") # 一旦バックエンドで入力させて挙動を見る

st.title("AI Chatbot For Website")

###### Sidebar ######
st.sidebar.image("https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=25)
st.sidebar.text_input("Enter your HuggingFace API Token", type="password")
st.sidebar.text_input("Enter your Pinecone API Token", type="password")

load_button = st.sidebar.button("Load data to Pinecone", key="load_button")

# load_button
if load_button:
    if st.session_state["HUGGINGFACEHUB_API_TOKEN"] != "" and st.session_state["PINECONE_API_KEY"] != "":
        with st.spinner('Crawl Website data...'):
            sitemap_data = get_website_data_from_sitemap(constants.SITEMAP_URL)
        st.write("Data pull done...")

        with st.spinner('Split data...'):
            chunks_data = split_data(sitemap_data)
        st.write("Splitting data done...")


        with st.spinner('Push to Pinecone...'):
            embeddings = get_embeddings()
            chunks_data = push_to_pinecone(
                pinecone_api_token=st.session_state['PINECONE_API_KEY'], 
                pinecone_environment=st.session_state['PINECONE_ENVIRONMENT'], 
                pinecone_index_name=st.session_state['PINECONE_INDEX_NAME'], 
                embeddings=embeddings, 
                docs=chunks_data
                )
        st.write("Pushing data to Pinecone done...")


        st.sidebar.success("Successfully insert data to Pinecone!", icon="✅")
    else:
        st.sidebar.warning("Please provide API Key", icon="🔑")

###### Main ######
prompt = st.text_input("How can I help you??")
document_count = st.slider("Number of the relevant links to return", 1, 5, 1)
submit = st.button("Search")

if submit:
    with st.spinner('Search...'):
        # Creating embedding instance
        embeddings = get_embeddings()
        # Pull index data from Pinecone
        index = pull_from_pinecone(
            pinecone_api_token=st.session_state['PINECONE_API_KEY'], 
            pinecone_environment=st.session_state['PINECONE_ENVIRONMENT'], 
            pinecone_index_name=st.session_state['PINECONE_INDEX_NAME'], 
            embeddings=embeddings, 
        )
        similar_docs = get_similar_docs(index, prompt, document_count)
        # st.write(similar_docs)
        # Fetch relavant documents from Pinecone
        for document in similar_docs:
            st.write("**:white_check_mark: Result: "+str(similar_docs.index(document)+1)+"**")
            st.write("**Info**: " + document.page_content)
            st.write("**Info**: " + document.metadata["source"])

    st.success("Please find the search results: ")



