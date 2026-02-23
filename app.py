import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="PPC Studio", layout="wide")

# 2. Design
st.markdown("<style>.stButton>button { width: 100%; height: 45px; background-color: black !important; color: white !important; border-radius: 8px; font-weight: bold; } .stButton>button:hover { background-color: #A89264 !important; } code { height: 70px !important; display: block; }</style>", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Příprava promptu")
c1, c2 = st.columns([2, 1])
b_in = c1.text_area("Brief:", height=150)
c_in = c2.text_area("Akce:", height=150)

if st.button("✨ Vygenerovat prompt"):
    if b_in:
        p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {b_in}. Akce: {c_in}"
        st.code(p)
    else:
        st.warning("Zadejte brief.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Editor a Export")
cm, cv = st.columns([1, 2])
kamp = cm.text_input("Kampaň", "K1")
sest = cm.text_input("Sestava", "S1")
link = cm.text_input("URL", "https://")
vstup = cv.text_area("Vložte texty:", height=150)

if (st.button("⚙
