import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Globální Setup
st.set_page_config(
    page_title="PPC Studio",
    layout="wide"
)

# 2. Design
st.markdown("""
<style>
    .stButton>button, .stDownloadButton>button {
        width: 100%;
        height: 45px;
        background-color: black !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #A89264 !important;
    }
    code {
        height: 70px !important;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Příprava promptu")
b = st.text_area("Brief:", height=150)
c = st.text_input("Vlastní akce/USPs:")

if st.button("✨ Vygenerovat"):
    p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {b}. Akce: {c}"
    st.code(p)
    st.write("Zkopírujte prompt výše.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Editor a Export")
col_m, col_v = st.columns([1, 2])

# Krátké řádky pro bezpečný zápis v editoru
kamp = col_m.text_input("Kampaň", "K1")
sest = col_m.text_input("Sestava", "S1")
link = col_m.text_input("URL", "https://")
vstup = col_v.text_area("Vložte texty od AI:", height=150)

# Tlačítko pro probuzení editoru
load = st.button("⚙️ Načíst do tabulky")

if (load or vstup) and link != "https://":
    lines = [l.strip() for l in vstup.split('\n') if l.strip()]
    
    if lines:
        # Tvorba tabulky
        rows = []
        for i, txt in enumerate(lines):
            t = "Nadpis" if i < 15 else "Popis"
            rows.append({"Typ": t, "Text": txt})
        
        df = pd.DataFrame(rows)
        
        st.write("### 📝 Upravte texty v tabulce:")
        
        # INTERAKTIVNÍ EDITOR
        ed_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            key="ed1"
        )
        
        h_f = ed_df[ed_df["Typ"] == "Nadpis"]["Text"].tolist()
        d_f = ed_df[ed_df["Typ"] == "Popis"]["Text"].tolist()
        
        # Náhledy
        st.write("### 👁️ Náhledy")
        n1, n2 = st.columns(2)
        h_all = ""
        for i in range(4):
            sh = random.sample(h_f, min(3, len(h_f))) if h_f else ["..."]
            sd = random.sample(d_f, min(2, len(d_f))) if d_f else ["..."]
            
            clean_u = link.replace("https://", "")
            ad = f"""<div style="background:white;padding:15px;border:1px solid #ddd;border-radius:8px;margin-bottom:10px;font-family:Arial;">
                <div style="font-size:12px;color:gray;">Sponzorováno • {clean_u}</div>
                <div style="color:#1a0dab;font-size:18px;">{" | ".join(sh)}</div>
