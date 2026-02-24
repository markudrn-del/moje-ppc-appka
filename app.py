import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")

# --- TRVALÉ CSS JIŠTĚNÍ PRO VELIKOST PROMPTU ---
st.markdown("""
    <style>
    /* 1. Zelená tlačítka */
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    /* 2. Absolutní omezení výšky pole s promptem */
    .stCodeBlock, .stCodeBlock div {
        max-height: 100px !important;
    }
    /* 3. Estetika náhledů */
    .ad-preview {
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        background: white;
        font-family: Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY A PROMPT ---
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

if "current_prompt" in st.session_state:
    st.success("Krok 1: Zkopírujte prompt (vpravo nahoře) a vložte ho do Gemini")
    # Zde je pole s promptem, které je nyní CSS stylem nahoře omezeno na 100px
    st.code(st.session_state.current_prompt, language="text")

st.markdown("---")

# --- 2. KROK: VLOŽENÍ TEXTU ---
u_link = st.text_input("URL webu", "https://publicis.cz")

# Key ai_input zajišťuje okamžitou reakci bez mezikliku
v_raw = st.text_area(
    "Krok 2: Vložte texty z AI sem", 
    height=150, 
    placeholder="Sem vložte vygenerovaný seznam z Gemini...",
    key="ai_input" 
)

if st.session_state.ai_input.strip():
    if st.button("✨ Vygenerovat inzeráty"):
        ls = [x.strip() for x in st.session_state.ai_input.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()
else:
    st.info("💡 Jakmile sem vložíte texty, objeví se zelené tlačítko.")

# --- 3. KROK: TABULKA A NÁHLEDY ---
def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if "df_data" in st.session_state:
    st.markdown("---")
    st.write("### Krok 3: Zkontrolujte a upravte texty")
    st.data_editor(st
