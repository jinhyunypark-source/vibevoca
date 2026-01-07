import streamlit as st
import pandas as pd
from backend.database import get_supabase_client

st.set_page_config(page_title="User Management", layout="wide")
st.title("👥 User Management")

supabase = get_supabase_client()

# Fetch Users
try:
    response = supabase.table("users").select("*").execute()
    users = response.data
    
    if not users:
        st.info("No users found in public.users table.")
    else:
        df = pd.DataFrame(users)
        
        # Display Stats
        col1, col2 = st.columns(2)
        col1.metric("Total Users", len(users))
        
        # Display Table
        st.dataframe(df, use_container_width=True)
        
        # Inspector
        st.subheader("User Inspector")
        selected_user_id = st.selectbox("Select User ID", df['id'].tolist())
        
        if selected_user_id:
            user_data = df[df['id'] == selected_user_id].iloc[0]
            st.json(user_data.to_dict())
            
            # Show Progress (If implemented)
            # st.write("Progress Data...")

except Exception as e:
    st.error(f"Error fetching users: {e}")
