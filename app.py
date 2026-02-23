import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("🦁 PPC Publicis Studio")

# 1. KROK - PROMPT
b_in = st.text_area("Brief")
c_in = st.text_input("USPs")
if st.button("Generovat prompt"):
    if b_in:
        st.code(f"RSA: 30 nadpisů, 10 popisků. {b_in}. {c_in}")

st.markdown("---")

# 2. KROK - EDITOR
st.subheader("2. Editor a kontrola limitů")
u_in = st.text_input("URL webu", "https://publicis.cz")
v_in = st.text_area("Vložte texty od AI sem")

if v_in:
    # Funkce pro barvení: Zelená pro OK (0 a víc), Červená pro zápor
    def color_status(val):
        color = '#ccffcc' if val >= 0 else '#ffcccc'
        return f'background-color: {color}'

    # Logika aktualizace dat
    def update_data():
        curr_state = st.session_state["main_editor"]
        df = st.session_state.df_editor
        for edit in curr_state.get("edited_rows", {}):
            for col, val in curr_state["edited_rows"][edit].items():
                df.at[int(edit), col] = val
        
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        st.session_state.df_editor = df

    if 'df_editor' not in st.session_state:
        lines = [l.strip() for l in v_in.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_editor = pd.DataFrame(data)

    # 1.
