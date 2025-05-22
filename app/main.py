import streamlit as st
from catalog import catalog
from ollama_client import call_ollama_deepseekcoder
from etl_generator import generate_simple_sql, generate_pyspark_code
import re

# Streamlit config
st.set_page_config(page_title="🛠️ One-Click ETL Generator", layout="wide")
st.title("🛠️ One-Click ETL Generator")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_datasets" not in st.session_state:
    st.session_state.selected_datasets = {}
if "transform_raw" not in st.session_state:
    st.session_state.transform_raw = ""
if "output_config" not in st.session_state:
    st.session_state.output_config = {}
if "genai_prompt" not in st.session_state:
    st.session_state.genai_prompt = ""

def next_step():
    if st.session_state.step < 4:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# UI Navigation bar
cols = st.columns(4)
tabs = ["1️⃣ Ingestion", "2️⃣ Transformation", "3️⃣ Output Config", "4️⃣ Final Output"]
for i, tab in enumerate(tabs):
    if cols[i].button(tab):
        st.session_state.step = i + 1

# Step 1: Ingestion
if st.session_state.step == 1:
    st.header("🔹 Ingestion Layer")
    selected = st.multiselect("Select datasets", options=list(catalog.keys()), default=list(st.session_state.selected_datasets.keys()))
    st.session_state.selected_datasets = {ds: catalog[ds] for ds in selected}
    st.json(st.session_state.selected_datasets)
    if st.button("Next ➡️"):
        if not selected:
            st.error("Please select at least one dataset")
        else:
            next_step()

# Step 2: Transformation
elif st.session_state.step == 2:
    st.header("🔹 Transformation Layer")
    st.write("Use natural language to describe transformation logic. Only use datasets from ingestion step.")
    st.warning("Auto-suggest datasets: " + ", ".join(st.session_state.selected_datasets.keys()))
    nlp = st.text_area("Describe transformation logic")
    if st.button("✨ Generate Logic"):
        used_datasets = set(re.findall(r"\b\w+\b", nlp.lower())) & set(catalog.keys())
        unauthorized = used_datasets - set(st.session_state.selected_datasets.keys())
        if unauthorized:
            st.error(f"🚫 You used unselected datasets: {', '.join(unauthorized)}")
        else:
            raw = call_ollama_deepseekcoder(st.session_state.selected_datasets, nlp)
            if raw:
                st.session_state.transform_raw = raw
                st.session_state.genai_prompt = nlp
                st.success("Transformation logic generated")
    if st.session_state.transform_raw:
        st.subheader("🧠 Raw GenAI Transformation Steps")
        st.code(st.session_state.transform_raw)
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back"):
        prev_step()
    if col2.button("Next ➡️"):
        if st.session_state.transform_raw:
            next_step()
        else:
            st.error("Generate transformation logic first")

# Step 3: Output Config
elif st.session_state.step == 3:
    st.header("🔹 Output Configuration")
    name = st.text_input("View Name", st.session_state.output_config.get("name", "final_output"))
    fmt = st.selectbox("Format", ["Table", "Parquet", "CSV"], index=0)
    st.session_state.output_config = {"name": name, "format": fmt}
    st.write("This is metadata only. Actual output handling can be implemented separately.")
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back"):
        prev_step()
    if col2.button("Next ➡️"):
        next_step()

# Step 4: Final Output
elif st.session_state.step == 4:
    st.header("🔹 Final Generated Output")

    st.subheader("🧠 Raw GenAI Transformation Steps")
    if st.session_state.transform_raw:
        st.code(st.session_state.transform_raw)
    else:
        st.info("No transformation logic generated yet.")

    st.subheader("💾 Recommended SQL Code")
    sql_code = generate_simple_sql(st.session_state.selected_datasets, st.session_state.genai_prompt)
    st.code(sql_code, language="sql")

    st.subheader("🐍 Generated PySpark Code")
    python_code = generate_pyspark_code(st.session_state.selected_datasets, st.session_state.genai_prompt)
    st.code(python_code, language="python")

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back"):
        prev_step()
