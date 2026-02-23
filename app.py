import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Globální design
st.set_page_config(page_title="PPC Publicis Studio", layout="wide")

st.markdown("""
<style>
    .stButton>button, .stDownloadButton>button {
        width: 100% !important; height: 45px !important;
        background-color: black !important; color: white !important;
        border-radius: 8px !important; border: none !important;
        font-weight: bold !important; font-size: 16px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #A89264 !important; transform: translateY(-1px);
    }
    .stCode, pre { height: 80px !important; min-height: 80px !important; }
    .ad-p {
        background: white; padding: 15px; border: 1px solid #ddd;
        border-radius: 8px; margin-bottom: 20px; font-family: Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    try:
        st.image("pub_logo_groupe_rvb.png", width=200)
    except:
        st.write("🦁 **Publicis**")

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1: PROMPT
st.subheader("1. Příprava zadání")
c_brf, c_custom = st.columns([2, 1])

with c_brf:
    brf = st.text_area("Vložte brief:", height=150)
with c_custom:
    custom_info = st.text_area("Vlastní texty / Akce:", height=150)

if st.button("✨ Vygenerovat prompt"):
    if brf:
        p_text = f"RSA inzeráty: 30 nadpisů (30 zn) a 10 popisků (90 zn). Zadání: {brf}. Akce: {custom_info}"
        st.write("**Prompt pro Gemini:**")
        st.code(p_text, language="text")
        st.components.v1.html(f"""
            <button onclick="navigator.clipboard.writeText(`{p_text}`).then(()=>alert('Zkopírováno!'))" 
            style="width:100%;height:45px;background:black;color:white;border-radius:8px;cursor:pointer;font-weight:bold;">
            📋 Zkopírovat prompt</button>""", height=55)
    else:
        st.warning("Zadejte text.")

st.markdown("---")

# 4. KROK 2: INTERAKTIVNÍ EDITOR A NÁHLEDY
st.subheader("2. Kontrola, Editace a Export")
col_meta, col_vstup = st.columns([1, 2])

with col_meta:
    k = st.text_input("Kampaň", "K1")
    s = st.text_input("Sestava", "S1")
    u = st.text_input("URL", "https://")

with col_vstup:
    v = st.text_area("Vložte texty od AI (každý na nový řádek):", height=150)

if v and u != "https://":
    # Zpracování vstupu
    rady = [line.strip() for line in v.split('\n') if line.strip()]
