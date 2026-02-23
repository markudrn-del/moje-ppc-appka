import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Konfigurace a design aplikace
st.set_page_config(page_title="Publicis PPC Generator", layout="centered")

# CSS pro sjednocení barev a tlačítek
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar s logem Publicis Groupe
with st.sidebar:
    # Odkazujeme na logo, které jsi nahrál do repozitáře
    LOGO_PATH = "pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO_PATH, width=200)
    except:
        st.write("🦁 **Publicis Groupe**")
    
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"**Autor:** Martin Kudrna, {rok}")
    st.write("**Poslední update:** 23. 2. 2026")

# 3. Hlavní část aplikace
st.title("🎯 PPC generátor inzerátů")

# --- KROK 1: ZADÁNÍ ---
st.subheader("1. Příprava zadání")
# Pole pro brief s výškou 200
brief = st.text_area("Vložte brief nebo obsah landing page:", height=200, placeholder="Sem zkopírujte text...")

if st.button("✨ Vygenerovat prompt pro Gemini"):
    if brief:
        prompt_text = f"Jsi PPC expert. RSA inzeráty: 15 nadpisů (30 zn) a 4 popisky (max 90 zn). Žádné vykřičníky v nadpisech. Zadání: {brief}"
        
        st.markdown("---")
        st.write("**Prompt pro Gemini (zkopírujte ikonkou vpravo nahoře):**")
        
        # Zobrazení promptu v okně (st.code má vestavěné tlačítko Copy)
        st.code(prompt_text, language="text")
        
        # Dodatečné instrukční tlačítko pro uživatele
        st.info("⬆️ Prompt je připraven. Klikněte na ikonu kopí
