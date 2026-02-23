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
v_in = st.text_area("Vložte texty od AI sem", height=200)

# PŘIDÁNO: Tlačítko pro explicitní načtení
load_data = st.button("✅ Načíst texty do tabulky")

# Funkce pro barvení
def color_status(val):
    return f'background-color: {"#ccffcc" if val >= 0 else "#ffcccc"}'

# Funkce pro aktualizaci
def update_data():
    if "main_editor" in st.session_state and "df_editor" in st.session_state:
        curr_state = st.session_state["main_editor"]
        df = st.session_state.df_editor.copy()
        for edit in curr_state.get("edited_rows", {}):
            for col, val in curr_state["edited_rows"][edit].items():
                df.at[int(edit), col] = val
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_editor = df

# LOGIKA NAČTENÍ
if load_data and v_in:
    lines = [l.strip() for l in v_in.split('\n') if l.strip()]
    data = []
    for i, t in enumerate(lines):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df_editor = pd.DataFrame(data)
    st.rerun() # Vynutí překreslení, aby se tabulka hned objevila

# ZOBRAZENÍ TABULEK (pokud už jsou data načtená)
if 'df_editor' in st.session_state:
    st.write("### 1. Upravte texty zde:")
    st.data_editor(
        st.session_state.df_editor,
        use_container_width=True,
        hide_index=True,
        key="main
