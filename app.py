import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Konfigurace stránky
st.set_page_config(
    page_title="PPC generátor inzerátů", 
    page_icon="🎯", 
    layout="centered"
)

# Minimalistické CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #000000;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR S PODPISEM ---
with st.sidebar:
    st.markdown("### O aplikaci")
    st.info("Pomocník pro PPC specialisty při tvorbě RSA inzerátů.")
    st.markdown("---")
    st.markdown(f"**Vytvořil:** Martin Kudrna, {datetime.now().year}")
    st.markdown("**Poslední update:** 23. února 2026")

# --- HLAVNÍ OBSAH ---
st.title("🎯 PPC generátor inzerátů")
st.caption("Minimalistický nástroj pro tvorbu RSA inzerátů z briefu do Google Editoru.")

# 1. SEKCE: GENERÁTOR PROMPTU
with st.container():
    st.subheader("1. Příprava zadání")
    user_brief = st.text_area(
        "Vložte brief nebo obsah webu", 
        height=150, 
        placeholder="Popište produkt, benefity..."
    )

    if st.button("✨ Vygenerovat prompt pro Gemini"):
        if user_brief:
            master_prompt = f"Předmět: RSA Inzeráty\nJsi expert na PPC. Vytvoř 15 nadpisů (max 30 znaků) a 4 popisky (max 90 znaků). Bez vykřičníků v nadpisech. Formát: 19 řádků pod sebou. Zadání: {user_brief}"
            st.info("Zkopírujte prompt do Gemini:")
            st.code(master_prompt, language="text")
        else:
            st.warning("Před vygenerováním vložte text zadání.")

st.markdown("---")

# 2. SEKCE: EXPORT
with st.container():
    st.subheader("2. Export pro Google Editor")
    
    col1, col2 = st.columns(2)
    with col1:
        camp_input = st.text_input("Kampaň", placeholder="Kampaň_01")
    with col2:
        group_input = st.text_input("Sestava", placeholder="Sestava_01")
    
    final_
