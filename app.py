import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Konfigurace a CSS
st.set_page_config(page_title="PPC", layout="centered")
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #000;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png"
    st.image(logo, width=180)
    st.markdown("---")
    st.info("PPC nástroj Publicis.")
    rok = datetime.now().year
    st.markdown(f"**Vytvořil:** Martin Kudrna, {rok}")
    st.markdown("**Update:** 23. 2. 2026")

# 3. Hlavní obsah
st.image(logo, width=120)
st.title("🎯 PPC generátor")

st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief/web:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        # Rozdělený prompt, aby se řádek neosekl
        p1 = "Jsi PPC expert. Vytvoř 15 nadpisů (max 30 zn.) "
        p2 = "a 4 popisky (max 90 zn.) pro RSA. Žádné "
        p3 = "vykřičníky. Formát: 19 řádků pod sebou. "
        p4 = f"Zadání: {brief}"
        full_p = p1 + p2 + p3 + p4
        st.write("**Prompt pro Gemini:**")
        st.code(full_p, language="text")
    else:
        st.warning("Vložte text.")

st.markdown("---")

st.subheader("2. Export pro Editor")
c1, c2 = st.columns(2)
camp = c1.text_input("Kampaň", "Kampaň_1")
seta = c2.text_input("Sestava", "Sestava_1")
url = st.text_input("URL", "https://")
raw = st.text_area("Vložte 19 řádků od AI:", height=200)

if raw and url != "https://":
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    h = lines[0:15
