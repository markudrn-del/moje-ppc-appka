import streamlit as st
import pandas as pd
import io
import random

st.set_page_config(layout="wide")

# AGRESIVNÍ CSS PRO OSTATNÍ PRVKY
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
    }
    /* Omezení pole pro vkládání (Krok 2) */
    .stTextArea textarea {
        max-height: 150px !important;
    }
    /* Styl pro náš vlastní prompt box */
    .custom-prompt-box {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 10px;
        font-family: monospace;
        font-size: 14px;
        height: 100px;
        overflow-y: scroll;
        white-space: pre-wrap;
        color: #31333F;
    }
    .ad-preview {
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        background: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🦁 PPC Publicis Studio")

# 1. KROK
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        p_f = (
            f"Jsi copywriter. RSA. Brief: {b_txt}. {u_txt} "
            f"FORMÁT: Jen texty, 15 nadpisů, 4 popisky."
        )
        st.session_state.current_prompt = p_f

if "current_prompt" in st.session_state:
    st.info("Krok 1: Zkopírujte prompt níže (box má fixní výšku):")
    # VLASTNÍ HTML BOX MÍSTO st.code
    st.markdown(
        f'<div class="custom-prompt-box">{st.session_state.current_prompt}</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# 2. KROK
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("Krok 2: Vložte texty z AI", key="ai_input")

if st.session_state.ai_input.strip():
    if st.button("✨ Vygenerovat inzeráty"):
        raw = st.session_state.ai_input
        ls = [x.strip() for x in raw.split('\n') if x.strip()]
        rows = []
        for i, t in enumerate(ls):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(t)})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

# 3. KROK
if "df_data" in st.session_state:
    st.markdown("---")
    st.data_editor(st.session_state.df_data, key="ppc_editor")

    st.subheader("👀 Náhledy")
    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"]=="Popis"]["Text"].tolist()

    if len(h_l) >= 2:
        cols = st.columns(2)
        for i in range(6):
            with cols[i % 2]:
                n_h = min(3, len(h_l))
                sh = random.sample(h_l, n_h)
                n_d = min(2, len(d_l))
                sd = random.sample(d_l, n_d) if d_l else [""]
                h_s = " – ".join(sh)
                d_s = " ".join(sd)
                st.markdown(
                    f'<div class="ad-preview">'
                    f'<div style="color:gray;">{u_link}</div>'
                    f'<div style="color:blue;font-size:18px;">{h_s}</div>'
                    f'<div>{d_s}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown("---")
    out = {"Campaign": "C1", "URL": u_link}
    for i in range(1, 16):
        out[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5):
