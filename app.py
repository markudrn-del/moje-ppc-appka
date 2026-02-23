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
st.subheader("2. Editor")
u_in = st.text_input("URL webu", "https://publicis.cz")
v_in = st.text_area("Vložte texty od AI sem")

if v_in:
    # Funkce pro výpočet, kterou zavoláme při každé změně
    def update_data():
        # Vezmeme aktuální stav editoru
        curr_state = st.session_state["main_editor"]
        df = st.session_state.df_editor
        
        # Zapracujeme změny (editace, přidání, smazání)
        for edit in curr_state.get("edited_rows", {}):
            for col, val in curr_state["edited_rows"][edit].items():
                df.at[int(edit), col] = val
        
        # Přepočítáme sloupce
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        st.session_state.df_editor = df

    # Inicializace dat
    if 'df_editor' not in st.session_state:
        lines = [l.strip() for l in v_in.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_editor = pd.DataFrame(data)

    # Zobrazení editoru s callbackem
    # Jakmile cokoli změníš a potvrdíš (Enter/Tab/Klik jinam), update_data se spustí
    st.data_editor(
        st.session_state.df_editor,
        use_container_width=True,
        hide_index=True,
        key="main_editor",
        on_change=update_data
    )

    # EXPORT
    st.markdown("---")
    df_f = st.session_state.df_editor
    h_f = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d_f = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()
    
    res = {"Campaign": "K1", "Ad Group": "S1", "URL": u_in}
    for i in range(15):
        res[f"H{i+1}"] = h_f[i] if i < len(h_f) else ""
    for i in range(4):
        res[f"D{i+1}"] = d_f[i] if i < len(d_f) else ""
            
    csv_data = pd.DataFrame([res]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    
    st.download_button(
        label="📥 Stáhnout hotové CSV",
        data=csv_data,
        file_name="export_ppc.csv"
    )

else:
    if 'df_editor' in st.session_state:
        del st.session_state.df_editor
    st.write("Čekám na vložení textů...")
