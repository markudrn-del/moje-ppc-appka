import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Studio")

# 1. KROK - PROMPT
b = st.text_area("1. Vlozte brief")
c = st.text_input("2. Vlastni USPs")
if st.button("Generovat prompt"):
    if b:
        st.code(f"RSA: 30 nadpisu, 10 popisku. {b}. {c}")

st.markdown("---")

# 2. KROK - EDITOR
st.subheader("2. Editor")
u = st.text_input("URL webu", "https://publicis.cz")
v = st.text_area("Vlozte texty od AI sem")

# Podminka nyni kontroluje jen, jestli je v poli 'v' nejaky text
if v:
    lines = [l.strip() for l in v.split('\n') if l.strip()]
    if lines:
        # Priprava dat
        rows = [{"Typ": ("Nadpis" if i < 15 else "Popis"), "Text": t} for i, t in enumerate(lines)]
        df = pd.DataFrame(rows)
        
        st.write("Upravte texty v tabulce (Enter pro potvrzeni):")
        ed = st.data_editor(df, use_container_width=True, key="e1")
        
        # Vypocet znaku - tlacitko pro manualni prepocet pro stabilitu
        if st.button("Prepocitat znaky"):
            ed["Zbyva"] = ed.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
            st.dataframe(ed, use_container_width=True)
        
        # EXPORT
        st.markdown("---")
        h = ed[ed["Typ"] == "Nadpis"]["Text"].tolist()
        d = ed[ed["Typ"] == "Popis"]["Text"].tolist()
        
        ex = {"Campaign": "K1", "Ad Group": "S1", "Final URL": u}
        for i in range(15):
            ex[f"Headline {i+1}"] = h[i] if i < len(h) else ""
        for i in range(4):
            ex[f"Description {i+1}"] = d[i] if i < len(d) else ""
            
        csv = pd.DataFrame([ex]).to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button("Stahnout CSV", csv, "export.csv")
else:
    st.info("Cekam na vlozeni textu do pole vyse...")
