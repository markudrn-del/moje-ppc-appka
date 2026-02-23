import streamlit as st
import pandas as pd
import io
import random

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
        res = []
        for i, t in enumerate(lns):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rem = lim - len(t)
            res.append({"Typ": tp, "Text": t, "Zbyva": rem})
        
        df = pd.DataFrame(res)
        
        # JEDNODUCHY EDITOR
        ed = st.data_editor(df, use_container_width=True, key="e1")
        
        # EXPORT
        h = ed[ed["Typ"] == "Nadpis"]["Text"].tolist()
        d = ed[ed["Typ"] == "Popis"]["Text"].tolist()
        
        ex = {"Campaign": "K1", "Ad Group": "S1", "Final URL": u}
        for i in range(15):
            val = h[i] if i < len(h) else ""
            ex[f"Headline {i+1}"] = val
        for i in range(4):
            val = d[i] if i < len(d) else ""
            ex[f"Description {i+1}"] = val
        
        out = pd.DataFrame([ex])
        buf = io.StringIO()
        out.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
        st.download_button("Stahnout CSV", buf.getvalue(), "export.csv")
