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
u_in = st.text_input("URL", "https://publicis.cz")
v_in = st.text_area("Vložte texty od AI sem")

if v_in:
    # 1. Zpracování vstupních textů do DataFrame (pokud ještě není v session_state)
    if 'df_editor' not in st.session_state:
        lines = [l.strip() for l in v_in.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            # Přidáme Zbyva hned při startu
            lim = 30 if tp == "Nadpis" else 90
            data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_editor = pd.DataFrame(data)

    st.write("### Upravte texty v tabulce:")

    # 2. Zobrazení JEDNÉ tabulky
    # Výsledek editoru ukládáme přímo do proměnné
    edited_df = st.data_editor(
        st.session_state.df_editor,
        use_container_width=True,
        hide_index=True,
        key="main_editor"
    )

    # 3. REÁLNÝ PŘEPOČET: Tato část kódu se spustí při každém "pohnutí" v tabulce
    # Přepočítáme sloupec Zbyva na základě aktuálního obsahu sloupce Text
    edited_df["Zbyva"] = edited_df.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    
    # Synchronizujeme změny zpět do session_state
    st.session_state.df_editor = edited_df

    # 4. EXPORT (bere data z té jediné upravené tabulky)
    st.markdown("---")
    h_f = edited_df[edited_df["Typ"] == "Nadpis"]["Text"].tolist()
    d_f = edited_df[edited_df["Typ"] == "Popis"]["Text"].tolist()
    
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
    # Pokud uživatel smaže text, vyčistíme i paměť tabulky
    if 'df_editor' in st.session_state:
        del st.session_state.df_editor
    st.info("Čekám na vložení textů...")
