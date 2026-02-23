import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = f"Jsi senior copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). CTR. Brief: {b_txt}.{u_p}"
        st.code(p_f)

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("AI texty sem", height=150)

def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        # Jednoduchý výpočet bez složitých závorek
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
    if v_raw.strip():
        ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
        rows = []
        for i, t in enumerate(ls
