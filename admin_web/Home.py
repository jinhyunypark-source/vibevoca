import streamlit as st
import sys
import os

# Add backend to path so we can import shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="VibeVoca Admin",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 VibeVoca Admin Console")
st.markdown("""
Welcome to the VibeVoca Content Management System.

**Modules:**
- **User Management**: Inspect user profiles and progress.
- **Deck & Card Manager**: CRUD operations for vocabulary.
- **AI Batch Engine**: Generate contextual examples using LLMs.
""")

st.sidebar.success("Select a page from the list.")
