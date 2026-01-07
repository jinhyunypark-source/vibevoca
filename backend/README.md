# VibeVoca AI Backend 🧠

This is the Python-based AI engine for VibeVoca, built with **FastAPI**.
It handles complex logic such as context-aware example generation using LLMs.

## Setup

1.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Run Admin Console

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Streamlit**:
    ```bash
    streamlit run admin_web/Home.py
    ```

## Run API Server (Legacy/Optional)
    ```bash
    uvicorn main:app --reload --port 8000
    ```

