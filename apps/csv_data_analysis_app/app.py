from dotenv import load_dotenv, find_dotenv
import streamlit as st

from utils import query_agent

load_dotenv(find_dotenv())


st.set_page_config(page_title="CSV Analysis", page_icon=":mag:")
st.title("CSV Analyzer")
st.markdown("""
**How to**
1. Upload a csv file
2. Enter the question about input file
3. Click button
""")

data = st.file_uploader("Upload csv file", type=["csv"])


query = st.text_area("Enter your query")
button = st.button("Generate Response")

if button:
    # Response
    answer = query_agent(data, query)
    st.write(answer)


