import streamlit as st
import pandas as pd
import io
import random

st.set_page_config(
    layout="wide",
    page_title="PPC Studio"
)

# --- CSS STYLY ---
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
    }
    .stCodeBlock, .stCodeBlock div {
        max-height: 100px !important;
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

# --- 1. KROK ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi copywriter. RSA (15 nadpisů, 4 popisky). "
            f"Brief: {b_txt}.{u_p} "
            f"FORMÁT: Jen texty, každý na nový řádek. "
            f"BEZ čísel. 15 nadpisů, pak 4 popisky."
        )
        st.session_state.current_prompt = p_f

if "current_prompt" in st.session_state:
    st.info("Krok 1: Zkopírujte prompt:")
    st.code(
        st.session_state.current_prompt,
        language="text"
    )

st.markdown("---")

# --- 2. KROK ---
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area(
    "Krok 2: Vložte texty z AI",
    height=150,
    key="ai_input"
)

if st.session_state.ai_input.strip():
    if st.button("✨ Vygenerovat inzeráty"):
        raw = st.session_state.ai_input
        ls = [x.strip() for x in raw.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append(
                {"Typ": tp, "Text": t, "Zbyva": lim - len(t)}
            )
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

# --- 3. KROK ---
def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        # Bezpečný výpočet
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])),
            axis=1
        )
        st.session_state.df_data = df

if "df_data" in st.session_state:
    st.markdown("---")
    st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocet
    )

    st.subheader("👀 Náhledy")
    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"]=="Popis"]["Text"].tolist()

    if len(h_l) >= 2:
        cols = st.columns(2)
        for i in range(6):
            with cols[i % 2]:
                sh = random.sample(h_l, min(3, len(h_l)))
                sd = random.sample(d_l, min(2,
