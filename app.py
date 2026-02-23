import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Publicis Studio")

# 1. KROK
b_in = st.text_area("Brief")
c_in = st.text_input("USPs")

if st.button("Prompt"):
    if b_in:
        txt = f"RSA: 30 nadpisu, 10 popisku. {b_in}. {c_in}"
        st.code(txt)

st.markdown("---")

# 2. KROK
u_in = st.text_input("URL", "https://publicis.cz")
v_in = st.text_area("AI texty")

if v_in:
    lines = v_in.split('\n')
    lines = [l.strip() for l in lines if l.strip()]
    
    if lines:
        data = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rem = lim - len(str(t))
            data.append({"Typ": tp, "Text": t, "Zbyva": rem})
        
        df = pd.DataFrame(data)
        
        st.write("Upravte texty v tabulce:")
        
        # EDITOR
        ed = st.data_editor(df, use_container_width=True, key="e1")
        
        # AKTUALIZACE
        if st.button("Prepocitat"):
            # Vypocet delek
            t_col = ed["Text"].astype(str)
            ed["Zbyva"] = ed.apply(
                lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
                axis=1
            )
            st.dataframe(ed, use_container_width=True)

        # EXPORT
        st.markdown("---")
        h_f = ed[ed["Typ"] == "Nadpis"]["Text"].tolist()
        d_f = ed[ed["Typ"] == "Popis"]["Text"].tolist()
        
        res = {"Campaign": "K1", "Ad Group": "S1", "URL": u_in}
        for i in range(15):
            val = h_f[i] if i < len(h_f) else ""
            res[f"H{i+1}"] = val
        for i in range(4):
            val = d_f[i] if i < len(d_f) else ""
            res[f"D{i+1}"] = val
            
        csv_df = pd.DataFrame([res])
        csv_data = csv_df.to_csv(index=False, sep=';', encoding='utf-8-sig')
        
        # ROZDELENE TLACITKO PRO STABILITU
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="export.csv"
        )
