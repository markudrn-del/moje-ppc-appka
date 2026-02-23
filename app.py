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

# Minimalistické CSS pro design
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

# --- SIDEBAR S LOGEM ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png", width=200)
    st.markdown("---")
    st.markdown("### O aplikaci")
    st.info("Nástroj Publicis pro tvorbu RSA inzerátů.")
    st.markdown(f"**Vytvořil:** Martin Kudrna, {datetime.now().year}")
    st.markdown("**Poslední update:** 23. února 2026")

# --- HLAVNÍ OBSAH ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png", width=150)
st.title("🎯 PPC generátor inzerátů")

# 1. SEKCE: PŘÍPRAVA ZADÁNÍ
st.subheader("1. Příprava zadání")
brief = st.text_area(
    "Vložte brief nebo obsah landing page:", 
    height=250, 
    placeholder="Sem vložte text..."
)

if st.button("✨ Vygenerovat prompt pro AI"):
    if brief:
        master_prompt = f"Předmět: RSA Inzeráty\nJsi expert na PPC. Vytvoř 15 nadpisů (max 30 znaků) a 4 popisky (max 90 znaků). Bez
