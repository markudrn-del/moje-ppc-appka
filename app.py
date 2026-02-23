import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Studio")

# 1. KROK
b = st.text_area("Brief")
c = st.text_input("USPs")

if st.button("Generovat"):
    p = f"RSA: 30 nadpisu, 10 popisku. {b}. {c}"
    st.code(p)

st.markdown("---")

# 2. KROK
u = st.text_input("URL", "https://")
v = st.text_area("Texty od AI")

if v and u != "https://":
    lns = [l.strip() for l in v.split('\n') if l.strip()]
    if lns:
        # Pocatecni data
        res = []
        for i, t in enumerate(lns):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            res.append({"Typ": tp, "Text": t, "Zbyva": lim - len(t)})
        
        df = pd.DataFrame(res)
        
        # EDITOR
        ed = st.data_editor(df, use_container_width=True, key="e1")
        
        # FYZICKY PREPOCET po editaci
        # Tento radek zajisti, ze se sloupec Zbyva prepise novou delkou
        ed["Zbyva"] = ed.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
        
        # EXPORT
        h = ed[ed["Typ"] == "Nadpis"]["Text"].tolist()
        d = ed[ed["Typ"] == "Popis"]["Text"].tolist()
        
        ex = {"Campaign": "K1", "Ad Group": "S1", "Final URL": u}
        for i in range(15):
            ex[f"Headline {i+1}"] = h[i] if i < len(h) else ""
        for i in
