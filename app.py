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

# Minimalistické CSS pro design a černé tlačítko
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
    .main-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # Přidání loga Publicis do sidebaru
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png", width=200)
    st.markdown("---")
    st.markdown("### O aplikaci")
    st.info("Nástroj pro Publicis týmy k efektivní tvorbě RSA inzerátů.")
    st.markdown(f"**Vytvořil:** Martin Kudrna, {datetime.now().year}")
    st.markdown("**Poslední update:** 23. února 2026")

# --- HLAVNÍ OBSAH ---
# Horní logo pro mobilní/středový pohled
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png", width=150)
st.title("🎯 PPC generátor inzerátů")
st.caption("Profesionální nástroj pro tvorbu RSA inzerátů z podkladů pro Google Ads Editor.")

# 1. SEKCE: PŘÍPRAVA ZADÁNÍ
st.subheader("1. Příprava zadání")
brief = st.text_area(
    "Vložte brief nebo obsah landing page:", 
    height=250, 
    placeholder="Sem zkopírujte text z webu nebo zadání od klienta..."
)

if st.button("✨ Vygenerovat prompt pro AI"):
    if brief:
        master_prompt = f"""Předmět: RSA Inzeráty
Jsi expert na PPC reklamu. Vytvoř 15 nadpisů (max 30 znaků) a 4 popisky (max 90 znaků).
Bez vykřičníků v nadpisech. Poctivě spočítej znaky!
Formát: jen 19 řádků pod sebou (15 nadpisů, pak 4 popisky). Nic jiného nepiš.
Zadání: {brief}"""
        
        st.write("**Zkopírujte tento prompt do Gemini:**")
        st.code(master_prompt, language="text")
    else:
        st.warning("Nejdříve vložte text zadání.")

st.markdown("---")

# 2. SEKCE: EXPORT PRO GOOGLE ADS
st.subheader("2. Export pro Google Editor")

col1, col2 = st.columns(2)
with col1:
    camp_input = st.text_input("Kampaň", placeholder="Kampaň_01")
with col2:
    group_input = st.text_input("Sestava", placeholder="Sestava_01")

final_url = st.text_input("Finální URL", placeholder="https://www.klient.cz")
raw_text = st.text_area("Vložte 19 řádků vygenerovaných AI:", height=200)

if raw_text:
    if not final_url or final_url == "https://":
        st.error("Pro export musíte vyplnit Finální URL.")
    else:
        # Zpracování textu
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        headlines = lines[:15] + [""] * (15 - len(lines[:15]))
        descriptions = lines[15:19
