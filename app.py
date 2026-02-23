Zdá se, že editor GitHubu má stále tendenci ořezávat řádky na určitém počtu znaků, což způsobuje chybu v syntaxi Pythonu (nedokončený textový řetězec).

Abychom tomu předešli, připravil jsem verzi, kde jsou všechny kritické texty extrémně krátké. Rozdělil jsem i informační hlášky tak, aby žádný řádek v celém kódu nepřesáhl bezpečnou délku.

🎯 Super-odolný kód pro app.py
Smažte prosím v GitHubu celý obsah souboru a vložte tam tento kód. Před potvrzením (Commit) se ujistěte, že vidíte i poslední řádek st.error.

Python
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Zakladni nastaveni
st.set_page_config(page_title="Publicis PPC", layout="centered")

# CSS pro vzhled tlacitek
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar s logem
with st.sidebar:
    LOGO = "pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO, width=200)
    except:
        st.write("🦁 **Publicis**")
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"Autor: Martin Kudrna, {rok}")

# 3. Hlavni cast
st.title("🎯 PPC generátor")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        # Rozdeleni promptu na velmi kratke kusy
        p = "Jsi PPC expert. RSA inzeraty: "
        p += "15 nadpisu (30 zn) a 4 popisky (90 zn). "
        p += "Bez vykricniku. "
        p += f"Zadani: {brief}"
        
        st.write("**Prompt pro Gemini:**")
        st.code(p, language="text")
        # Velmi kratky radek pro info
        st.info("Kopirujte ikonkou vpravo nahore.")
    else:
        st.warning("Zadejte text.")

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Export pro Editor")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "K_01")
sestava = c2.text_input("Sestava", "S_01")

web = st.text_input("URL", "https://")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if (vstup and web != "https://"):
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h = rady[0:15] + [""] * (15 - len(rady[0:15]))
    d = rady[15:19] + [""] * (4 - len(rady[15:19]))

    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15):
        data[f"Headline {i+1}"] = h[i]
    for i in range(4):
        data[f"Description {i+1}"] = d[i]

    df = pd.DataFrame([data])
    
    def check(v, m):
        return 'background-color: #ffcccc' if len(str(v)) > m else ''

    st.write("### Kontrola a stažení")
    h_cols = [f"Headline {i+1}" for i in range(15)]
    st.dataframe(df.style.applymap(lambda x: check(x, 30), subset=h_cols))

    # Export pro cesky Excel (strednik + BOM)
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    st.download_button(
        label="📥 Stáhnout CSV",
        data=buf.getvalue(),
        file_name=f"export_{sestava}.csv",
        mime="text/csv"
    )
elif vstup:
    st.error("Chybí URL adresa.")
