import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Publicis Studio")

# 1. KROK - PROMPT
b_in = st.text_area("Brief")
c_in = st.text_input("USPs")
if st.button("Prompt"):
    if b_in:
        st.code(f"RSA: 30 nadpisu, 10 popisku. {b_in}. {c_in}")

st.markdown("---")

# 2. KROK - EDITOR
u_in = st.text_input("URL", "https://publicis.cz")
v_in = st.text_area("AI texty")

if v_in:
    # Rozdeleni textu na radky
    lines = [l.strip() for l in v_in.split('\n') if l.strip()]
    
    if lines:
        # Vytvoreni zakladniho DataFrame, pokud jeste neexistuje v pameti
        if 'df_editor' not in st.session_state:
            data = []
            for i, t in enumerate(lines):
                tp = "Nadpis" if i < 15 else "Popis"
                lim = 30 if tp == "Nadpis" else 90
                data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
            st.session_state.df_editor = pd.DataFrame(data)

        st.write("Upravte texty (Zbyva se aktualizuje po potvrzeni bunky):")
        
        # EDITOR - napojeny na session_state
        edited_df = st.data_editor(
            st.session_state.df_editor,
            use_container_width=True,
            hide_index=True,
            key="my_editor"
        )

        # TRIGGER PREPOCTU: Vzdy prepocitame Zbyva z aktualnich dat v editoru
        edited_df["Zbyva"] = edited_df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        
        # Ulozeni zmen zpet
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
            label="Download CSV",
            data=csv_data,
            file_name="export.csv"
        )
