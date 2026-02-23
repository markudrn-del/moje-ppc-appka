import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="PPC generátor", page_icon="🎯", layout="centered")

# CSS styl pro černé tlačítko
st.markdown("<style>.stButton>button{width:100%;background-color:black;color:white;border-radius:5px;}</style>", unsafe_allow_html=True)

# Sidebar s informacemi
with st.sidebar:
    st.markdown("### O aplikaci")
    st.info("Nástroj pro efektivní tvorbu RSA inzerátů.")
    st.markdown("---")
    st.markdown(f"**Autor:** Martin Kudrna, {datetime.now().year}")
    st.markdown("**Update:** 23. 2. 2026")

st.title("🎯 PPC generátor inzerátů")

# 1. SEKCE: PŘÍPRAVA ZADÁNÍ
st.subheader("1. Příprava zadání")
# Větší pole pro brief
brief = st.text_area("Vložte brief nebo obsah landing page:", height=250, placeholder="Sem zkopírujte text z webu nebo zadání od klienta...")

if st.button("✨ Vygenerovat prompt pro AI"):
    if brief:
        p = f"Jsi PPC expert. Vytvoř 15 nadpisů (max 30 zn.) a 4 popisky (max 90 zn.) pro RSA. Žádné vykřičníky v nadpisech. Poctivě spočítej znaky. Formát: jen 19 řádků pod sebou (nejdřív nadpisy, pak popisky). Zadání: {brief}"
        st.markdown("---")
        st.write("**Prompt pro Gemini (zkopírujte ikonkou vpravo nahoře):**")
        # Menší zobrazení promptu pomocí st.code
        st.code(p, language="text")
    else:
        st.warning("Nejdříve vložte text briefu nebo landing page.")

st.markdown("---")

# 2. SEKCE: EXPORT PRO GOOGLE ADS
st.subheader("2. Export pro Google Editor")
c1, c2 = st.columns(2)
camp = c1.text_input("Kampaň", "Kampaň_1")
seta = c2.text_input("Sestava", "Sestava_1")
url = st.text_input("Finální URL", "https://")
raw = st.text_area("Vložte 19 řádků vygenerovaných AI:", height=200, placeholder="Nadpis 1\nNadpis 2\n...")

if raw and url != "https://":
    ls = [l.strip() for l in raw.split('\n') if l.strip()]
    h = ls[:15] + [""] * (15 - len(ls[:15]))
    d = ls[15:19] + [""] * (4 - len(ls[15:19]))
    
    data = {"Campaign": camp, "Ad Group": seta, "Final URL": url}
    for i in range(15): data[f"Headline {i+1}"] = h[i]
    for i in range(4): data[f"Description {i+1}"] = d[i]
    
    df = pd.DataFrame([data])
    
    def color_l(v, m):
        return 'background-color: #ffebee; color: #c62828' if len(str(v)) > m else ''

    st.write("### Kontrola délek (červená = příliš dlouhé)")
    st.dataframe(df.style.applymap(lambda x: color_l(x, 30), subset=[f"Headline {i+1}" for i in range(15)])
                       .applymap(lambda x: color_l(x, 90), subset=[f"Description {i+1}" for i in range(4)]))

    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button("📥 Stáhnout CSV pro Google Editor", buf.getvalue(), f"export_{seta}.csv", "text/csv")
elif raw:
    st.error("Pro stažení CSV musíte vyplnit Finální URL.")
