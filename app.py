import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Zakladni nastaveni
st.set_page_config(page_title="Publicis PPC", layout="centered")

# CSS pro vzhled tlacitek
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar s logem
with st.sidebar:
    LOGO = "pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO, width=200)
    except:
        st.write("🦁 **Publicis**")
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"Autor: Martin Kudrna, {rok}")

# 3. Hlavni cast
st.title("🎯 PPC generátor")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        # Rozdeleni promptu na velmi kratke kusy
        p = "Jsi PPC expert. RSA inzeraty: "
        p += "15 nadpisu (30 zn) a 4 popisky (90 zn). "
        p += "Bez vykricniku. "
        p += f"Zadani: {brief}"
        
        st.write("**Prompt pro Gemini:**")
        st.code(p, language="text")
        st.info("Kopirujte ikonkou vpravo nahore.")
    else:
        st.warning("Zadejte text.")

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Export pro Editor")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "K_01")
sestava = c2.text_input("Sestava", "S_01")

web = st.text_input("URL", "https://")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if (vstup and web != "https://"):
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h = rady[0:15] + [""] * (15 - len(rady[0:15]))
    d = rady[15:19] + [""] * (4 - len(rady[15:19]))

    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15):
        data[f"Headline {i+1}"] = h[i]
