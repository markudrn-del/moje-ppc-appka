import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Konfigurace a styl
st.set_page_config(page_title="Publicis PPC Tool", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: black; color: white; border-radius: 5px; }
    .ad-preview {
        background-color: white;
        padding: 15px;
        border: 1px solid #dfe1e5;
        border-radius: 8px;
        max-width: 600px;
        font-family: Arial, sans-serif;
    }
    .ad-url { color: #202124; font-size: 14px; margin-bottom: 4px; }
    .ad-title { color: #1a0dab; font-size: 20px; text-decoration: none; display: block; margin-bottom: 4px; cursor: pointer; }
    .ad-title:hover { text-decoration: underline; }
    .ad-desc { color: #4d5156; font-size: 14px; line-height: 1.58; }
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

st.title("🎯 PPC generátor inzerátů")

# --- KROK 1: PROMPT ---
st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief nebo obsah landing page:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        p = "Jsi PPC expert. RSA inzeraty: 15 nadpisu (30 zn) a 4 popisky (90 zn). "
        p += "Bez vykricniku. Format: 19 radku pod sebou. "
        p += f"Zadani: {brief}"
        st.code(p, language="text")
        st.info("Prompt zkopírujte ikonkou vpravo nahoře.")
    else:
        st.warning("Zadejte text briefu.")

st.markdown("---")

# --- KROK 2: EXPORT A NÁHLEDY ---
st.subheader("2. Export a Náhledy pro klienta")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "K_01")
sestava = c2.text_input("Sestava", "S_01")
web = st.text_input("Finální URL (včetně https://)", "https://www.priklad.cz")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h_list = rady[0:15]
    d_list = rady[15:19]
    
    # Naplnění pro export
    h_exp = h_list + [""] * (15 - len(h_list))
    d_exp = d_list + [""] * (4 - len(d_list))

    # --- SEKCE NÁHLEDU ---
    st.write("### 👁️ Náhodné náhledy pro klienta")
    for j in range(2): # Vygeneruje 2 náhodné varianty
        # Náhodný výběr 3 nadpisů a 2 popisků pro vizualizaci
        sample_h = random.sample(h_list, min(3, len(h_list))) if h_list else ["Nadpis 1", "Nadpis 2", "Nadpis 3"]
        sample_d = random.sample(d_list, min(2, len(d_list))) if d_list else ["Popisek inzerátu..."]
        
        display_title = " | ".join(sample_h)
        display_desc = " ".join(sample_d)
        clean_url = web.replace("https://", "").replace("http://", "")

        st.markdown(f"""
        <div class="ad-preview">
            <div class="ad-url">Sponzorováno • {clean_url}</div>
            <div class="ad-title">{display_title}</div>
            <div class="ad-desc">{display_desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    # --- EXPORTNÍ TABULKA ---
    st.write("### 📊 Exportní soubor")
    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15): data[f"Headline {i+1}"] = h_exp[i]
    for i in range(4): data[f"Description {i+1}"] = d_exp[i]

    df = pd.DataFrame([data])
    
    def check(v, m): return 'background-color: #ffcccc' if len(str(v)) > m else ''
    st.dataframe(df.style.applymap(lambda x: check(x, 30), subset=[f"Headline {i+1}" for i in range(15)]))

    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 Stáhnout CSV pro Excel", buf.getvalue(), f"export_{sestava}.csv")

elif vstup:
    st.error("Doplňte URL adresu pro zobrazení náhledů a exportu.")
