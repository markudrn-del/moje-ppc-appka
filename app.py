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
        # ZESÍLENÝ PROMPT: Explicitně nařizuje použití USPs
        usp_part = f" Do inzerátů povinně zakomponuj tato USPs: {u_txt}." if u_txt else ""
        prompt_final = f"RSA: 15 nadpisů (do 30 znaků), 4 popisky (do 90 znaků). Brief: {b_txt}.{usp_part}"
        st.info("Zkopírujte tento prompt do AI:")
        st.code(prompt_final)
    else:
        st.warning("Nejdříve vložte brief.")

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("Finální URL webu", "https://publicis.cz")
v_raw = st.text_area("Vložte texty od AI sem", height=150)

# FUNKCE PRO PŘEPOČET A BARVY
def prepocitej_vse():
    if "ppc_editor" in st.session_state:
        zmeny = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        
        for radek, hodnoty in zmeny.get("edited_rows", {}).items():
            for sloupec, nova_hodnota in hodnoty.items():
                df.at[int(radek), sloupec] = nova_hodnota
        
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        # Indikátor: Smajlík pro rychlou vizuální kontrolu v tabulce
        df["Stav"] = df["Zbyva"].apply(lambda x: "✅ OK" if x >= 0 else "❌ DLOUHÉ")
        st.session_state.df_data = df

# Tlačítko pro načtení
if st.button("✅ Načíst do tabulky") and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        zb = lim - len(str(t))
        rows.append({
            "Typ": tp, 
            "Text": t, 
            "Zbyva": zb, 
            "Stav": "✅ OK" if zb >= 0 else "❌ DLOUHÉ"
        })
    st.session_state.df_data = pd.DataFrame(rows)

# ZOBRAZENÍ EDITORU
if "df_data" in st.session_state:
    st.write("### Upravte texty (Změna se projeví po kliknutí mimo buňku):")
    
    # Stylizace - barvení textu ve sloupci Zbyva
    def color_negative(val):
        color = 'red' if val < 0 else 'green'
        return f'color: {color}; font-weight: bold'

    st.data_editor(
        st.session_state.df_data.style.applymap(color_negative, subset=['Zbyva']),
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocitej_vse
    )

    # --- 3. KROK: EXPORT ---
    st.markdown("---")
    final_df = st.session_state.df_data
    h = final_df[final_df["Typ"] == "Nadpis"]["Text"].tolist()
    d = final_df[final_df["Typ"] == "Popis"]["Text"].tolist()
    
    exp = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(15): exp[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4): exp[f"Description {i+1}"] = d[i] if i < len(d) else ""
            
    csv = pd.DataFrame([exp]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 Stáhnout CSV pro Editor", csv, "ppc_export.csv")
