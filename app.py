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
b = c1.text_area("Brief:", height=150)
c = c2.text_area("Vlastní akce/USPs:", height=150)

if st.button("✨ Vygenerovat prompt"):
    if b:
        p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {b}. Akce: {c}"
        st.code(p)
        st.write("Zkopírujte prompt výše.")
    else:
        st.warning("Zadejte brief.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Editor a Export")
col_m, col_v = st.columns([1, 2])
kamp = col_m.text_input("Kampaň", "K1")
sest = col_m.text_input("Sestava", "S1")
link = col_m.text_input("URL", "https://")
vstup = col_v.text_area("Vložte texty od AI:", height=150)

load = st.button("⚙️ Načíst do tabulky")

if (load or vstup) and link != "https://":
    lines = [l.strip() for l in vstup.split('\n') if l.strip()]
    if lines:
        # PŘÍPRAVA DAT S POČÍTADLEM
        rows = []
        for i, txt in enumerate(lines):
            typ = "Nadpis" if i < 15 else "Popis"
            limit = 30 if typ == "Nadpis" else 90
            zbyva = limit - len(txt)
            rows.append({"Typ": typ, "Text": txt, "Zbývá": zbyva})
        
        df = pd.DataFrame(rows)
        st.write("### 📝 Editujte v tabulce:")
        
        # INTERAKTIVNÍ EDITOR
        ed_df = st.data_editor(
            df, 
            use_container_width=True, 
            hide_index=True, 
            key="ed1",
            column_config={
                "Typ": st.column_config.TextColumn("Typ", disabled=True),
                "Text": st.column_config.TextColumn("Text (edit
