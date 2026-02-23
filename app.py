import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("🦁 PPC Publicis Studio")

# 1. KROK - PROMPT (Zjednodušeno pro stabilitu)
b_in = st.text_area("Brief")
c_in = st.text_input("USPs")
if st.button("Generovat prompt"):
    if b_in:
        st.code(f"RSA: 30 nadpisů, 10 popisků. {b_in}. {c_in}")

st.markdown("---")

# 2. KROK - EDITOR S OKAMŽITÝM PŘEPOČTEM
u_in = st.text_input("URL", "https://publicis.cz")
v_in = st.text_area("Vložte texty od AI sem")

if v_in:
    # Funkce pro přepočet limitů
    def prepocitej_limity(df):
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        return df

    # Načtení dat do paměti (session state), aby se změny neztrácely
    if 'df_editor' not in st.session_state or st.button("Resetovat tabulku"):
        lines = [l.strip() for l in v_in.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            data.append({"Typ": tp, "Text": t})
        st.session_state.df_editor = pd.DataFrame(data)

    # Zobrazení editoru
    st.write("### Upravte texty (Změna se projeví po kliknutí mimo buňku):")
    
    # Důležité: Tady bereme data ze session_state a výsledek ukládáme zpět
    edited_data = st.data_editor(
        st.session_state.df_editor,
        use_container_width=True,
        hide_index=True,
        key="main_editor"
    )

    # OKAMŽITÝ PŘEPOČET: Streamlit spustí tento kód při každé interakci
    # Výsledek přepočtu zobrazíme v reálném čase
    st.session_state.df_editor = prepocitej_limity(edited_data)

    # Vizuální kontrola - tabulka s aktuálními limity
    st.dataframe(
        st.session_state.df_editor, 
        use_container_width=True, 
        hide_index=True
    )

    # EXPORT
    st.markdown("---")
    df_final = st.session_state.df_editor
    h_f = df_final[df_final["Typ"] == "Nadpis"]["Text"].tolist()
    d_f = df_final[df_final["Typ"] == "Popis"]["Text"].tolist()
    
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
