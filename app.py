import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="PPC Publicis Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY PRO AI ---
col1, col2 = st.columns(2)
with col1:
    b_txt = st.text_area("Vložte brief (o čem je kampaň)", height=100, key="input_brief")
with col2:
    u_txt = st.text_input("Vlastní USPs (budou povinně v inzerátech)", key="input_usps")

if st.button("🚀 Generovat PRO copywrite prompt"):
    if b_txt:
        usp_part = f" Do inzerátů povinně a organicky zakomponuj tato USPs: {u_txt}." if u_txt else ""
        prompt_final = (
            f"Jsi nejlepší seniorní copywriter na světě se specializací na výkonnostní PPC. "
            f"Napiš RSA inzerát (15 nadpisů do 30 znaků a 4 popisky do 90 znaků). "
            f"Texty musí být naprosto skvělé, úderné a neodolatelné, aby na ně lidé co nejvíce klikali (vysoké CTR). "
            f"Používej psychologii prodeje, emoce a silná akční slova. "
            f"Každý nadpis a popisek dej na nový řádek bez čísel. "
            f"Brief: {b_txt}.{usp_part}"
        )
        st.info("Zkopírujte tento prompt do AI:")
        st.code(prompt_final)
    else:
        st.warning("Nejdříve vložte aspoň krátký brief.")

st.markdown("---")

# --- 2. KROK: EDITOR ---
st.subheader("2. Kontrola a úprava inzerátů")
u_link = st.text_input("Finální URL", "https://publicis.cz", key="input_url")

# TEXTOVÉ POLE PRO AI VÝSTUP
v_raw = st.text_area("Vložte texty vygenerované AI sem", height=200, key="ai_input_area")

# Funkce pro výpočet (on_change)
def prepocitej_limity():
    if "ppc_editor" in st.session_state and "df_data" in st.session_state:
        zmeny = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        for radek, hodnoty in zchanges.get("edited_rows", {}).items():
            for sloupec, nova_val in hodnoty.items():
                df.at[int(radek), sloupec] = nova_val
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) -
