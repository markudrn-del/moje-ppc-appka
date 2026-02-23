import streamlit as st
import pandas as pd
import io
import random

st.set_page_config(layout="wide", page_title="PPC Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief (o čem je kampaň)", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" Do inzerátů povinně zakomponuj tato USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi nejlepší copywriter. Napiš RSA inzerát (15 nadpisů do 30 zn., 4 popisky do 90 zn.). "
            f"Vysoké CTR, psychologie prodeje. Každý text na nový řádek. "
            f"Brief: {b_txt}.{u_p}"
        )
        st.code(p_f)

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("Finální URL", "https://publicis.cz")
v_raw = st.text_area("Vložte texty od AI sem", height=150)

def prepocet():
    if "ppc_editor" in st.session_state:
        ed_state = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        for r, h in ed_state.get("edited_rows", {}).items():
            for col, val in h.items():
                df.at[int(r), col] = val
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
    if v_raw.strip():
        ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
        rows = []
        for i, t in enumerate(ls):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

if "df_data" in st.session_state:
    st.data_editor(st.session_state.df_data, use_container_width=True, hide_index=True, key="ppc_editor", on_change=prepocet)

    # --- 3. KROK: NÁHLEDY PRO KLIENTA ---
    st.markdown("---")
    st.subheader("👀 Náhledy inzerátů (6 náhodných kombinací)")
    
    df_f = st.session_state.df_data
    h_list =
