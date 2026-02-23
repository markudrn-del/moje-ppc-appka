import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup a styl
st.set_page_config(page_title="Publicis Studio", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #A89264;
    }
    code {
        height: 80px !important;
        display: block;
        overflow-y: auto;
    }
    .ad-preview {
        background-color: white;
        padding: 15px;
        border: 1px solid #dfe1e5;
        border-radius: 8px;
        margin-bottom: 20px;
        font-family: Arial, sans-serif;
    }
    .ad-title { color: #1a0dab; font-size: 20px; }
    .ad-desc { color: #4d5156; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    LOGO = "pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO, width=200)
    except:
        st.write("🦁 **Publicis**")
    st.write(f"© {datetime.now().year}")

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        p = "Jsi PPC expert. RSA: 15 nadpisu (30) a 4 popisky (90). "
        p += f"Zadani: {brief}"
        st.write("**Prompt
