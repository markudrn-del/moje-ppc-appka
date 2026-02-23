import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Zakladni nastaveni
st.set_page_config(page_title="PPC", layout="centered")

# 2. Sidebar s logem
with st.sidebar:
    url_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Publicis_Groupe_logo.svg/1200px-Publicis_Groupe_logo.svg.png"
    st.image(url_logo, width=150)
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"Autor: Martin Kudrna, {rok}")
    st.write("Update: 23. 2. 2026")

# 3. Hlavni cast
st.title("🎯 PPC generátor")

st.subheader("1. Zadani")
txt = st.text_area("Vlozte brief:", height=200)

if st.button("✨ Vygenerovat"):
    if txt:
        prompt = "Jsi PPC expert. RSA inzeraty: 15 nadpisu (30 zn) a 4 popisky (90 zn). Bez vykricniku. "
        prompt += f"Zadani: {txt}"
        st.code(prompt, language="text")
    else:
        st.warning("Prazdne zadani.")

st.markdown("---")

st.subheader("2. Export")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampan", "K1")
sestava = c2.text_input("Sestava", "S1")
web = st.text_input("URL", "https://")
vstup = st.text_area("Vlozte 19 radku od AI:", height=200)

# Bezpecne zpracovani radku
if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    
    # Rozdeleni na nadpisy a popisky (bezpecne)
    nadpisy = rady[0:15]
    popisky = rady[15:19]
    
    # Doplneni do poctu
    while len(nadpisy) < 15:
        nadpisy.append("")
    while len(popisky) < 4:
        popisky.append("")

    # Tabulka
    d = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15):
        d[f"Headline {i+1}"] = nadpisy[i]
    for i in range(4):
        d[f"Description {i+1}"] = popisky[i]

    df = pd.DataFrame([d])
    
    # Kontrola delek
    def check(v, m):
        if len(str(v)) > m:
            return 'background-color: #ffcccc'
        return ''

    st.dataframe(df.style.applymap(lambda x: check(x, 30), 
        subset=[f"Headline {i+1}" for i in range(15)]))

    # CSV s diakritikou
    buf = io.StringIO()
    df.to_csv(buf, index=False, encoding='utf-8-sig')
    st.download_button("📥 Stahnout CSV", buf.getvalue(), "export.csv")
elif vstup:
    st.error("Chybi URL.")
