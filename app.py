import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("PPC Studio")

# 1. KROK - VSTUP
v_raw = st.text_area("Vlozte AI texty sem", height=150)
load = st.button("Vytvorit editor")

# Inicializace session state
if load and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df = pd.DataFrame(rows)

# JEDNA TABULKA - EDITOR
if "df" in st.session_state:
    st.write("### Editor (Zbyva se prepocita hned po Enteru):")
    
    # Zobrazeni editoru
    # Poznamka: Klicem k uspechu je, ze vysledek ukladame primo do df a hned ho prepocitame
    edited_df = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor_final"
    )

    # OKAMZITY PREPOCET (Vzdy, kdyz se stranka obnovi po zmene v editoru)
    edited_df["Zbyva"] = edited_df.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    
    # Ulozeni aktualniho stavu, aby se cisla nevracela zpet
    st.session_state.df = edited_df

    # EXPORT
    st.markdown("---")
    csv = edited_df.to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("Stahnout CSV", csv, "export.csv")
