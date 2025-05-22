# One-Click ETL Generator

A Streamlit app that generates ETL logic and code from natural language descriptions and selected datasets.

## Setup

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

Project Structure
app/main.py - Streamlit UI

app/etl_generator.py - ETL generation logic

app/catalog.py - Dataset catalog

app/ollama_client.py - Ollama API calls
