import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")

# --- CSS PRO ZELENÁ TLAČÍTKA A KOMPAKTNÍ PROMPT ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #218838 !important;
    }
    .stCodeBlock div {
        max-height: 120px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi špičkový copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). "
            f"Cílem je maximální CTR. Brief: {b_txt}.{u_p} "
            f"FORMÁT VÝSTUPU: Vypiš pouze texty, každý na nový řádek. "
            f"BEZ čísel, BEZ odrážek. Nejdřív 15 nadpisů, pak 4 popisky."
        )
        st.session_state.current_prompt = p_f
    else:
        st.warning("Vložte brief.")

if "current_prompt" in st.session_state:
    st.success("Krok 1: Zkopírujte prompt (vpravo nahoře) a vložte ho do Gemini")
    st.code(st.session_state.current_prompt, language="text")
