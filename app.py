import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")

# --- CUSTOM CSS PRO ZMENŠENÍ PROMPTU ---
st.markdown("""
    <style>
    /* Omezení výšky pro code block */
    .stCodeBlock div {
        max-height: 150px !important;
        overflow-y: auto !important;
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
        st.info("Zkopírujte prompt (pole má posuvník):")
        # Pole je nyní omezeno pomocí CSS výše
        st.code(p_f, language="text")
    else:
        st.warning("Vložte brief.")

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("URL webu", "https://publicis.cz")
v_raw = st.text_area("Vložte texty z AI sem", height=150)

def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
    if v_raw.strip():
        ls = [x.strip() for x in v_raw.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
