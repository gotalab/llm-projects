import os

import streamlit as st
from dotenv import load_dotenv, find_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage




load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Function to return the response
def load_answer(question):
    chat = ChatOpenAI(temperature=0)
    messages = [
    SystemMessage(
        content="You are a helpful assistant that answer the question."
    ),
    HumanMessage(
        content=question
    )
    ]
    answer=chat(messages)
    return answer.content


#App UI starts here
st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("LangChain Demo")

#Gets the user input
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input=get_text()
response = load_answer(user_input)

submit = st.button('Generate')  

#If generate button is clicked
if submit:
    st.subheader("Answer:")
    st.write(response)

