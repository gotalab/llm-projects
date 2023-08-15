from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import matplotlib.pyplot as plt

import pandas as pd


def query_agent(data, query):
    df = pd.read_csv(data)
    llm = OpenAI()

    # Create a Pandas DataFrame agent.
    agent = create_pandas_dataframe_agent(llm, df, verbose=True) #, return_intermediate_steps=True
    response = agent.run(query)
    return response
