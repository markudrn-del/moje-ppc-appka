import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Publicis Studio")

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

if v:
    lines = [l.strip() for l in v.split('\n') if l.strip()]
    if lines:
        # Tady vytvorime data i se sloupcem Zbyva hned na zacatku
        rows = []
        for i, t in enumerate(lines):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        
        df = pd.DataFrame(rows)
        
        st.write("Upravte texty (pro prepocet limitu kliknete na tlacitko nize):")
        
        # EDITOR - nyni vidi vsechny 3 sloupce
        ed = st.data_editor(
            df, 
            use_container_width=True, 
            key="e1", 
            hide_index=True
        )
        
        # TLACITKO PRO AKTUALIZACI
        # Streamlit editor neumi menit jine bunky v realnem case pri psani,
        # proto tlacitko "Prepocitat" vynuti prekresleni tabulky s novymi limity.
        if st.button("Aktualizovat pocty znaku"):
            ed["Zbyva"] = ed.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
            st.success("Limity prepocitany!")
            # Zobrazime vysledek pod editorem pro rychlou kontrolu
            st.dataframe(ed, use_container_width=True, hide_index=True)
        
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
        st.download_button("
