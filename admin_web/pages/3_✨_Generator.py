import streamlit as st
from backend.database import get_supabase_client

st.set_page_config(page_title="AI Generator", layout="wide")
st.title("✨ AI Batch Generator")

st.info("This module controls the batch generation pipeline.")

supabase = get_supabase_client()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Configuration")
    model = st.selectbox("LLM Model", ["gpt-4o", "gpt-3.5-turbo", "claude-3-opus"])
    context_type = st.selectbox("Target Context", ["Cafe", "Office", "Travel", "School"])
    
    decks = supabase.table("decks").select("title, id").execute().data
    deck_options = {d['title']: d['id'] for d in decks}
    selected_deck = st.selectbox("Target Deck", list(deck_options.keys()))

with col2:
    st.subheader("Pipeline Status")
    st.write("Ready to generate examples for:")
    st.write(f"- **Context**: {context_type}")
    st.write(f"- **Deck**: {selected_deck}")
    
    if st.button("🚀 Start Batch Generation", type="primary"):
        st.warning("Batch Engine implementation pending...")
        # TODO: Call ExampleGenerator class here
        
st.divider()
st.subheader("Generated Examples Preview")
st.write("No recent jobs.")
