import streamlit as st
import pandas as pd
import io
import random

st.set_page_config(layout="wide")

st.markdown("""
<style>
div.stButton > button { background-color: #28a745 !important; color: white !important; }
.stTextArea textarea { max-height: 150px !important; }
.custom-prompt-box {
    background-color: #f0f2f6; border: 1px solid #d1d5db; border-radius: 4px;
    padding: 10px; font-family: monospace; height: 100px; overflow-y: scroll;
    white-space: pre-wrap; color: #31333F;
}
.ad-preview { border: 1px solid #dadce0; border-radius: 8px; padding: 12px; margin-bottom: 10px; background: white; }
</style>
""", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

c1, c2 = st.columns(2)
with c1: b_txt = st.text_area("Brief", height=100)
with c2: u_txt = st.text_input("USPs")

if st.button("🚀 Generovat PRO prompt"):
    p_f = f"Jsi copywriter. RSA. Brief: {b_txt}. {u_txt} FORMÁT: Jen texty, 15 nadpisů, 4 popisky."
    st.session_state.current_prompt = p_f

if "current_prompt" in st.session_state:
    st.markdown(f'<div class="custom-prompt-box">{st.session_state.current_prompt}</div>', unsafe_allow_html=True)

st.markdown("---")
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("Krok 2: Vložte texty z AI", key="ai_input")

if st.button("✨ Vygenerovat inzeráty") and st.session_state.ai_input.strip():
    ls = [x.strip() for x in st.session_state.ai_input.split('\n') if x.strip()]
    rows = [{"Typ": "Nadpis" if i < 15 else "Popis", "Text": t, "Zbyva": (30 if i < 15 else 90) - len(t)} for i, t in enumerate(ls)]
    st.session_state.df_data = pd.DataFrame(rows)
    st.rerun()

if "df_data" in st.session_state:
    st.data_editor(st.session_state.df_data, key="ppc_editor")
    h_l = st.session_state.df_data[st.session_state.df_data["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = st.session_state.df_data[st.session_state.df_data["Typ"]=="Popis"]["Text"].tolist()
    
    st.subheader("👀 Náhledy")
    cols = st.columns(2)
    # Ruční výpis náhledů bez cyklu pro maximální stabilitu
    for i in range(4):
        with cols[i % 2]:
            sh = random.sample(h_l, min(3, len(h_l))) if len(h_l) > 1 else ["Nadpis"]
            sd = random.sample(d_l, min(2, len(d_l))) if len(d_l) > 0 else ["Popis"]
            st.markdown(f'<div class="ad-preview"><small>{u_link}</small><br><b style="color:blue">{" - ".join(sh)}</b><br>{ " ".join(sd)}</div>', unsafe_allow_html=True)

    st.markdown("---")
    # EXPORT BEZ CYKLŮ - EXTRÉMNĚ BEZPEČNÝ ZÁPIS
    exp_data = {"URL": u_link}
    # Naplníme data napřímo, žádné odsazené for-cykly na konci
    h1 = h_l[0] if len(h_l) > 0 else ""
    h2 =
