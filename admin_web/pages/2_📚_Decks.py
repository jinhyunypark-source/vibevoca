import streamlit as st
import pandas as pd
from backend.database import get_supabase_client

st.set_page_config(page_title="Deck Manager", layout="wide")
st.title("📚 Deck & Card Manager")

supabase = get_supabase_client()

# 1. Deck List
st.subheader("Decks")

@st.cache_data
def fetch_decks():
    return supabase.table("decks").select("*").execute().data

decks = fetch_decks()

if decks:
    df_decks = pd.DataFrame(decks)
    st.dataframe(df_decks[['title', 'category_id', 'id', 'color', 'icon']], use_container_width=True)
    
    # Selection
    selected_deck_title = st.selectbox("Select Deck to Edit Cards", df_decks['title'].unique())
    selected_deck_id = df_decks[df_decks['title'] == selected_deck_title].iloc[0]['id']
    
    # 2. Cards in Deck
    if selected_deck_id:
        st.divider()
        st.subheader(f"Cards in '{selected_deck_title}'")
        
        cards_response = supabase.table("cards").select("*").eq("deck_id", selected_deck_id).execute()
        cards = cards_response.data
        
        if cards:
            df_cards = pd.DataFrame(cards)
            st.dataframe(df_cards[['front_text', 'back_text', 'id']], use_container_width=True)
            
            with st.expander("Add New Card"):
                with st.form("add_card_form"):
                    front = st.text_input("Front Text (Word)")
                    back = st.text_input("Back Text (Meaning)")
                    example_1 = st.text_input("Example 1")
                    
                    if st.form_submit_button("Add Card"):
                        if front and back:
                            new_card = {
                                "deck_id": selected_deck_id,
                                "front_text": front,
                                "back_text": back,
                                "example_sentences": [example_1] if example_1 else []
                            }
                            supabase.table("cards").insert(new_card).execute()
                            st.success(f"Added '{front}'")
                            st.rerun()
                        else:
                            st.warning("Front and Back text required.")
        else:
            st.info("No cards in this deck.")
else:
    st.info("No decks found.")
