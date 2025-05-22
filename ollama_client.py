from ollama import Client
import streamlit as st

def call_ollama_deepseekcoder(selected_datasets, nlp_input):
    client = Client()
    prompt = f"""
You are a Big Data ETL expert. Given the following natural language transformation:

User has selected the following datasets:
"{list(selected_datasets.keys())}"

User provided logic and ensure that the logic uses only the above datasets. If any other dataset is used return an error message.

User logic input in natural language:
"{nlp_input}"

Return a sequential list of transformation steps in plain text, describing joins, filters, selects, and so on.
DO NOT return JSON or code, just clear human-readable transformation steps.
"""
    try:
        response = client.chat(
            model='deepseek-coder',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        st.error(f"Ollama Error: {e}")
        return ""
