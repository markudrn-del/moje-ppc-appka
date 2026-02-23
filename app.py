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
        # Priprava dat bez cyklu for pro jistotu
        rows = [{"Typ": ("Nadpis" if i < 15 else "Popis"), "Text": t} for i, t in enumerate(lns)]
        df = pd.DataFrame(rows)
        
        # EDITOR
        ed = st.data_editor(df, use_container_width=True, key="e1")
        
        # AKTUALIZACE POČÍTADLA - jeden radek
        ed["Zbyva"] = ed.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
        
        # Zobrazeni tabulky s prepocitanym sloupcem
        st.write("### Kontrola delek (Zaporne cislo = moc dlouhe)")
        st.dataframe(ed, use_container_width=True)
        
        # EXPORT - vytvoreni slovniku primo
        h = ed[ed["Typ"] == "Nadpis"]["Text"].tolist()
        d = ed[ed["Typ"] == "Popis"]["Text"].tolist()
        
        # Hlavni data
        ex = {"Campaign": "K1", "Ad Group": "S1", "Final URL": u}
        
        # Pridani nadpisu a popisu (bezpecny zapis)
        for i in range(15):
            ex[f"Headline {i+1}"] = h[i] if i < len(h) else ""
        for i in range(4):
            ex[f"Description {i+1}"] = d[i] if i < len(d) else ""
        
        # Finalni CSV
        out = pd.DataFrame([ex])
        buf = io.StringIO()
        out.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
        
        st.write("### Export pripraven")
        st.download_button("Stahnout CSV", buf.getvalue(), "export.csv")
