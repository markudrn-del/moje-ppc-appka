import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Konfigurace
st.set_page_config(page_title="Publicis PPC", layout="centered")

# CSS pro černá tlačítka a sjednocení
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 5px;
    }
    /* Úprava výšky okna s kódem */
    code {
        height: 200px !important;
        display: block;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    LOGO = "pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO, width=200)
    except:
        st.write("🦁 **Publicis Groupe**")
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"Autor: Martin Kudrna, {rok}")

# 3. Hlavní část
st.title("🎯 PPC generátor")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
# Výška nastavena na 200
brief = st.text_area("Vložte brief nebo obsah landing page:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        p = "Jsi PPC expert. RSA inzeraty: 15 nadpisu (30 zn) "
        p += "a 4 popisky (90 zn). Bez vykricniku. "
        p += f"Zadani: {brief}"
        
        st.write("**Prompt pro Gemini:**")
        # Pole pro prompt má nyní díky CSS výšku 200px
        st.code(p, language="text")
        
        if st.button("📋 Zkopírovat pro AI"):
            st.success("Prompt je připraven v šedém poli výše. Klikněte na ikonu kopírování v jeho pravém rohu.")
    else:
        st.warning("Zadejte text briefu.")

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Export pro Editor")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "K_01")
sestava = c2.text_input("Sestava", "S_01")

web = st.text_input("Finální URL", "https://")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h = rady[0:15] + [""] * (15 - len(rady[0:15]))
    d = rady[15:19] + [""] * (4 - len(rady[15:19]))

    data = {"Campaign": kampan, "Ad Group": seta, "Final URL": web}
    for i in range(15): data[f"Headline {i+1}"] = h[i]
    for i in range(4): data[f"Description {i+1}"] = d[i]

    df = pd.DataFrame([data])
    
    def check(v, m):
        return 'background-color: #ffcccc' if len(str(v)) > m else ''

    st.write("### Kontrola délek")
    h_cols = [f"Headline {i+1}" for i in range(15)]
    st.dataframe(df.style.applymap(lambda x: check(x, 30), subset=h_cols))

    # EXPORT: Středník a utf-8-sig pro český Excel
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    st.download_button(
        label="📥 Stáhnout CSV pro Excel",
        data=buf.getvalue(),
        file_name=f"export_{sestava}.csv",
        mime="text/csv"
    )
elif vstup:
    st.error("Chybí URL adresa.")
