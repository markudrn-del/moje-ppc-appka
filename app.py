import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. Konfigurace a design
st.set_page_config(page_title="Publicis PPC", layout="centered")

# CSS pro sjednocení vzhledu a černá tlačítka
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    LOGO = "https://raw.githubusercontent.com/MartinKudrna/moje-ppc-appka/main/pub_logo_groupe_rvb.png"
    try:
        st.image(LOGO, width=200)
    except:
        st.write("🦁 **Publicis Groupe**")
    st.markdown("---")
    rok = datetime.now().year
    st.write(f"Autor: Martin Kudrna, {rok}")
    st.write("Update: 23. 2. 2026")

# 3. Hlavní část
st.title("🎯 PPC generátor inzerátů")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
# Nastavená výška 200 pro brief
brief = st.text_area("Vložte brief nebo obsah landing page:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        prompt_text = f"Jsi PPC expert. RSA inzeráty: 15 nadpisů (30 zn) a 4 popisky (max 90 zn). Žádné vykřičníky. Zadání: {brief}"
        
        st.write("**Prompt pro Gemini (zkopírujte níže):**")
        # Okno se stejnou výškou (st.code se přizpůsobuje obsahu, ale ohraničíme ho)
        st.code(prompt_text, language="text")
        
        # Tlačítko pro kopírování (Streamlit nemá nativní clipboard write na jedno kliknutí bez JS, 
        # ale st.code má ikonu vpravo nahoře. Přidáme instrukci pro uživatele.)
        st.success("⬆️ Prompt připraven! Klikněte na ikonu kopírování v pravém horním rohu šedého pole.")
    else:
        st.warning("Nejdříve zadejte text briefu.")

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Export pro Google Editor")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "Kampaň_1")
sestava = c2.text_input("Sestava", "Sestava_1")
web = st.text_input("Finální URL", "https://")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h = rady[0:15] + [""] * (15 - len(rady[0:15]))
    d = rady[15:19] + [""] * (4 - len(rady[15:19]))

    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15): data[f"Headline {i+1}"] = h[i]
    for i in range(4): data[f"Description {i+1}"] = d[i]

    df = pd.DataFrame([data])
    
    def color_l(v, m):
        return 'background-color: #ffcccc' if len(str(v)) > m else ''

    st.write("### Kontrola délek")
    st.dataframe(df.style.applymap(lambda x: color_l(x, 30), subset=[f"Headline {i+1}" for i in range(15)]))

    # EXPORT PRO ČESKÝ EXCEL
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
