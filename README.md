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


# Project Details

# Brief Project Description

The One-Click ETL Generator is a streamlined, AI-assisted tool designed to simplify the creation of ETL pipelines. By selecting datasets, describing transformations in natural language, and configuring output options, users can automatically generate transformation logic, SQL code, and PySpark scripts — all within an interactive web UI. This tool aims to accelerate data engineering workflows and reduce manual coding errors, making ETL creation accessible even to users with limited programming experience.

# One-Pager PDF

a. Problem Statement
Data engineers and analysts often face significant challenges in rapidly designing and implementing ETL pipelines. These processes are usually manual, error-prone, and require deep expertise in SQL or Spark. Organizations need a simplified, intuitive way to accelerate ETL development, reduce time-to-insight, and lower the barrier to entry for less technical users.

b. Preliminary Solution
Our solution leverages natural language inputs and AI-driven logic generation to automate the creation of ETL pipelines. Users select datasets, describe the transformation logic in simple language, and configure output formats via a user-friendly web app. The backend calls an AI model (via Ollama) to generate human-readable transformation steps and produces recommended SQL and PySpark code snippets, streamlining the entire ETL design process.

c. GitHub Copilot Usage Scenario
GitHub Copilot was used extensively throughout development to assist in writing boilerplate Streamlit UI components, Python functions for SQL and PySpark code generation, regex for input validation, and structuring the project with modular Python packages. Copilot’s suggestions accelerated coding by providing context-aware code completions and helped maintain consistent style and functionality.

d. Roles and Responsibilities among Team Members
Team Lead & Architect: Designed the overall solution architecture, managed GitHub repository, and integrated AI model calls.

Backend Developer: Implemented the Python logic for transformation generation, SQL and PySpark code creation.

Frontend Developer: Developed the Streamlit UI, including navigation, session management, and user interaction workflows.

QA Engineer: Created test cases for UI flows and transformation logic, ensuring error handling and validation worked correctly.

Documentation Specialist: Compiled user guides, project summaries, and prepared the one-pager PDF and PPT deck.

# GitHub Repository Link

https://github.com/P7rox/one-click-etl-generator.git
