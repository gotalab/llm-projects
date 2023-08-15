import os

from dotenv import load_dotenv, find_dotenv

from langchain import OpenAI
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import (ConversationBufferMemory,
                              ConversationSummaryMemory,
                              ConversationBufferWindowMemory
                              )

import streamlit as st



# Page config and header
st.set_page_config(page_title="ChatGPT Clone", page_icon=":robot_face:")
st.markdown("## How can I assist you?")

def reset_sessionstate():
    if "conversation" in st.session_state:
        st.session_state["conversation"] = None
    if "messages" in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Sidebar
# st.sidebar.title("clone")

if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''


st.session_state['openai_api_key'] = st.sidebar.text_input("Enter OpenAI API KEY", type="password")
set_llm_model = st.sidebar.selectbox(label="Select LLM model.(If changed, chat history is reset.)", options=("gpt-3.5-turbo", "gpt-4"), index=0, key="llm_model", on_change=reset_sessionstate)
summarize_button = st.sidebar.button("Summarize the conversation", key="summarize")

if summarize_button:
    summarize_text = st.sidebar.write(st.session_state["conversation"].memory.buffer)

# Model


def get_response(user_input: str, openai_api_key):

    if not st.session_state["conversation"]:
        llm = OpenAI(
            temperature=0,
            model_name=set_llm_model,
            openai_api_key=openai_api_key
        )
        # llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)

        st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        st.session_state["conversation"] = ConversationChain(
            llm=llm, verbose=True, memory=ConversationSummaryMemory(llm=llm), callbacks=[st_callback]
        )

    # conversation.predict(input="おはようございます！")
    # conversation("私はgotaです")
    # conversation.predict(input="私は東京に住んでいます。")
    # print(conversation.memory.buffer)
    # conversation.predict(input="私の名前は？")

    response = st.session_state["conversation"].predict(input=user_input)
    return response

# Body(Main UI)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if "conversation" not in st.session_state:
    st.session_state["conversation"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Send a Message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not st.session_state['openai_api_key']:
        st.warning("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        response = get_response(user_input=st.session_state.messages[-1]["content"], openai_api_key=st.session_state['openai_api_key'])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)