import streamlit as st

from model import getLLMResponse

#UI
st.set_page_config(page_title="Marketing Assistant Tool",
                    page_icon=':shark:',
                    layout='centered',
                    initial_sidebar_state='collapsed')
st.header("Hey, How can I help you?")

form_input = st.text_area('Enter text', height=275)

tasktype_option = st.selectbox(
    'Please select the action to be performed?',
    ('Write a sales copy', 'Create a tweet', 'Write a product description'),key=1)

age_option= st.selectbox(
    'For which age group?',
    ('Kid', 'Adult', 'senior Citizen'), key=2)


numberOfWords= st.slider('Words limit', 1, 200, 25)

submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input,age_option,tasktype_option))