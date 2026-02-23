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
    # Načtení dat do session_state, aby se tabulka neresetovala při každém kliku
    if 'df_editor' not in st.session_state:
        lines = [l.strip() for l in v_in.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            # Výpočet hned při startu
            data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_editor = pd.DataFrame(data)

    st.info("💡 Po úpravě textu klikněte mimo buňku nebo stiskněte Enter – hodnoty 'Zbyva' se okamžitě přepočítají (i do mínusu).")

    # Zobrazení editoru – výsledek ukládáme do edited_df
    # Streamlit po každé změně v ed_df spustí kód znovu odshora
    edited_df = st.data_editor(
        st.session_state.df_editor,
        use_container_width=True,
        hide_index=True,
        key="main_editor"
    )

    # KLÍČOVÁ ČÁST: Přepočet sloupce Zbyva z aktuálně rozpracovaných dat
    # Tento výpočet proběhne hned, jakmile změníte buňku v editoru
    edited_df["Zbyva"] = edited_df.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    
    # Uložíme aktualizovaná data zpět do paměti aplikace
    st.session_state.df_editor = edited_df

    # EXPORT
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
    # Pokud uživatel smaže textové pole, vymažeme i paměť tabulky
    if 'df_editor' in st.session_state:
        del st.session_state.df_editor
    st.write("Čekám na vložení textů...")
