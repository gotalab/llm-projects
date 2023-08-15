import os

from dotenv import load_dotenv, find_dotenv

import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain.llms import CTransformers, HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate



load_dotenv(find_dotenv())

# llm_llama2 = CTransformers(
#     model='models/llama-2-7b.bin', 
#     model_type='llama',
#     config={
#         'max_new_tokens': 256,
#         'temperature': 0.01
#     }
# )
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def chat_model(model_name, temperature=.7):
    if model_name == "gpt-3.5-turbo":
        llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
    else:
        llm = ChatOpenAI(temperature=temperature, model="gpt-4")
    return llm


def getLLMResponse(llm, content_topic, name_from, name_to, writing_style, output_language):
    system_template = """
    You are a helpful assistant that writes email.
    You should write it in {output_language}.
    """
    human_template = """
    Write a email with {style} style and include topic: {email_topic}. 
    \n\nFrom: {name_from} 
    \n\nTo: {name_to}
    \n\nEmail Text:
    """

    template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template),
    ])
  
    #Generating the response using LLM
    response=llm(template.format_messages(email_topic=content_topic,name_from=name_from,name_to=name_to,style=writing_style, output_language=output_language))

    return response.content


st.set_page_config(
    page_title="Content Generator",
    page_icon=":cooking:",
    layout="centered",
    # initial_sidebar_state="collapsed"
)
##### Define Session State #####
if "LLM_Model" not in st.session_state:
    st.session_state["LLM_Model"] = "Llama-2-7b"

##### SideBar #####
st.session_state["LLM_Model"] = st.sidebar.selectbox(label="Use LLM Model", options=("gpt-3.5-turbo", "gpt-4"), index=0)

##### UI #####
st.title("Email Generator")
content_topic = st.text_area("Enter the content topic", height=200)

col1, col2, col3 = st.columns([10, 10, 10])
with col1:
    name_from = st.text_input("Sender Name")
with col2:
    name_to = st.text_input("Recipient Name")
with col3:
    writing_style = st.selectbox("Writing Style", ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'), index=0)

st.divider()
col21, col22 = st.columns([10, 10])
with col21:
    output_language = st.selectbox("Output Language", ('Japanese', 'English'), index=0)
with col22:
    temperature = st.slider(label='Temperature', min_value=0.0, max_value=1.0, value=.7, step= 0.01)

submit = st.button("Generate")

if submit:
    with st.spinner("Generate..."):
        st.write(getLLMResponse(chat_model(st.session_state["LLM_Model"], temperature=temperature), content_topic, name_from, name_to, writing_style, output_language))