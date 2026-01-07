import streamlit as st
import pandas as pd
from backend.database import get_supabase_client

st.set_page_config(page_title="Context Manager", layout="wide")
st.title("🏙️ Context Metadata Manager")

st.markdown("""
Define the **Contexts** used for generating examples.
The **Prompt Description** is crucial for the AI to understand the setting.
""")

supabase = get_supabase_client()

# Fetch Contexts
# Note: Ensure the 'contexts' table exists in your Supabase DB.
# Schema: id (uuid), slug (text), label (text), icon (text), prompt_description (text)

try:
    response = supabase.table("contexts").select("*").execute()
    contexts = response.data
    
    if contexts:
        df = pd.DataFrame(contexts)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No contexts found. Please create the 'contexts' table and add data.")
        
        # Temporary Mock Data Visualizer for Demo
        st.subheader("Mock Data Preview (Frontend Sync)")
        mock_data = [
            {"slug": "place_home", "label": "Home", "prompt": "At a cozy home, relaxing."},
            {"slug": "place_cafe", "label": "Cafe", "prompt": "In a busy coffee shop with ambient noise."},
            {"slug": "emotion_excited", "label": "Excited", "prompt": "Feeling very energetic and enthusiastic."},
        ]
        st.table(mock_data)

    # Add New Context Form
    with st.expander("Add New Context Metadata"):
        with st.form("add_context"):
            c_type = st.selectbox("Type", ["place", "emotion", "environment"])
            slug = st.text_input("Slug (e.g., place_library)")
            label = st.text_input("Label (e.g., Library)")
            icon = st.text_input("Icon Key (e.g., local_library)")
            prompt = st.text_area("Prompt Description (AI Instruction)")
            
            if st.form_submit_button("Save Context"):
                if slug and label and prompt:
                    try:
                        new_context = {
                            "type": c_type,
                            "slug": slug,
                            "label": label,
                            "icon": icon,
                            "prompt_description": prompt
                        }
                        supabase.table("contexts").insert(new_context).execute()
                        st.success(f"Context '{label}' created!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error saving: {ex}")
                else:
                    st.warning("All fields are required.")

except Exception as e:
    st.error(f"Error connecting to Contexts table: {e}")
    st.caption("Did you create the `contexts` table in Supabase?")
