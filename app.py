import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
col1, col2 = st.columns(2)
with col1:
    b_txt = st.text_area("Vložte brief", height=100)
with col2:
    u_txt = st.text_input("Vlastní USPs (nepovinné)")

if st.button("Generovat prompt pro AI"):
    if b_txt:
        st.code(f"RSA: 30 nadpisů, 10 popisků. {b_txt}. {u_txt}")

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("Finální URL webu", "https://publicis.cz")
v_raw = st.text_area("Vložte texty od AI sem", height=150)

# FUNKCE PRO OKAMŽITÝ PŘEPOČET
def prepocitej_vse():
    # Načteme to, co uživatel právě dopsal do editoru
    if "ppc_editor" in st.session_state:
        zmeny = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        
        # Propíšeme změny do naší tabulky
        for radek, hodnoty in zmeny.get("edited_rows", {}).items():
            for sloupec, nova_hodnota in hodnoty.items():
                df.at[int(radek), sloupec] = nova_hodnota
        
        # Přepočítáme zbývající znaky (i do záporu)
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        st.session_state.df_data = df

# Tlačítko pro první načtení
if st.button("✅ Načíst do tabulky") and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df_data = pd.DataFrame(rows)

# ZOBRAZENÍ EDITORU
if "df_data" in st.session_state:
    st.info("💡 Upravte text a klikněte jinam nebo dejte Enter. Počet znaků se ihned aktualizuje.")
    
    # Editor s funkcí on_change
    st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocitej_vse  # TADY JE TA OPRAVA
    )

    # EXPORT
    st.markdown("---")
    final_df = st.session_state.df_data
    h = final_df[final_df["Typ"] == "Nadpis"]["Text"].tolist()
    d = final_df[final_df["Typ"] == "Popis"]["Text"].tolist()
    
    exp = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(15): exp[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4): exp[f"Description {i+1}"] = d[i] if i < len(d) else ""
            
    csv = pd.DataFrame([exp]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 Stáhnout CSV", csv, "ppc_export.csv")
