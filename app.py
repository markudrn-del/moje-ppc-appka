import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="PPC Publicis Studio", layout="wide")

st.markdown("""
<style>
    .stButton>button, .stDownloadButton>button {
        width: 100% !important; height: 45px !important;
        background-color: black !important; color: white !important;
        border-radius: 8px !important; border: none !important;
        font-weight: bold !important; transition: 0.3s !important;
    }
    .stButton>button:hover { background-color: #A89264 !important; }
    .stCode, pre { height: 80px !important; min-height: 80px !important; }
    /* Styl pro editor aby byl vidět */
    [data-testid="stDataEditor"] { border: 2px solid #A89264 !important; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
c1, c2 = st.columns([2, 1])
brf = c1.text_area("Brief:", height=150)
custom = c2.text_area("Akce/USPs:", height=150)

if st.button("✨ Vygenerovat prompt"):
    if brf:
        p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {brf}. Akce: {custom}"
        st.code(p)
        st.components.v1.html(f"""<button onclick="navigator.clipboard.writeText(`{p}`).then(()=>alert('Zkopírováno'))" style="width:100%;height:45px;background:black;color:white;border-radius:8px;cursor:pointer;font-weight:bold;">📋 Zkopírovat</button>""", height=50)

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Kontrola a Editace")
cm, cv = st.columns([1, 2])
k = cm.text_input("Kampaň", "K1")
s = cm.text_input("Sestava",
