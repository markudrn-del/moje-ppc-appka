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
        margin-bottom: 20px;
    }
    .ad-url { color: #202124; font-size: 14px; margin-bottom: 4px; }
    .ad-title { color: #1a0dab; font-size: 20px; display: block; margin-bottom: 4px; font-weight: 400; }
    .ad-desc { color: #4d5156; font-size: 14px; line-height: 1.58; }
    .preview-header { font-weight: bold; margin-bottom: 10px; color: #5f6368; font-size: 12px; }
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
web = st.text_input("Finální URL", "https://www.priklad.cz")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h_list = rady[0:15]
    d_list = rady[15:19]
    
    # --- SEKCE NÁHLEDU (4 VARIANTY) ---
    st.write("### 👁️ Náhledy pro klienta (4 varianty)")
    
    preview_html = f"<h2>Náhledy inzerátů - {sestava}</h2>"
    
    cols = st.columns(1)
    for j in range(4):
        # Výběr 3 nadpisů a 2 popisků
        s_h = random.sample(h_list, min(3, len(h_list))) if len(h_list) >= 3 else h_list
        s_d = random.sample(d_list, min(2, len(d_list))) if len(d_list) >= 2 else d_list
        
        d_title = " | ".join(s_h)
        d_desc = " ".join(s_d)
        c_url = web.replace("https://", "").replace("http://", "")

        ad_html = f"""
        <div class="ad-preview">
            <div class="preview-header">Varianta náhledu {j+1}</div>
            <div class="ad-url">Sponzorováno • {c_url}</div>
            <div class="ad-title">{d_title}</div>
            <div class="ad-desc">{d_desc}</div>
        </div>
        """
        st.markdown(ad_html, unsafe_allow_html=True)
        preview_html += ad_html

    # --- EXPORTY ---
    st.write("### 📊 Exporty")
    
    # 1. Export CSV
    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15): data[f"Headline {i+1}"] = h_list[i] if i < len(h_list) else ""
    for i in range(4): data[f"Description {i+1}"] = d_list[i] if i < len(d_list) else ""
    df = pd.DataFrame([data])
    
    buf_csv = io.StringIO()
    df.to_csv(buf_csv, index=False, sep=';', encoding='utf-8-sig')
    
    c_down1, c_down2 = st.columns(2)
    c_down1.download_button("📥 Stáhnout CSV pro Editor", buf_csv.getvalue(), f"export_{sestava}.csv")
    
    # 2. "PDF" Export (jako HTML soubor, který se v prohlížeči uloží jako PDF přes Tisk)
    st.caption("Tip: Pro PDF klikněte na tlačítko níže, stiskněte Ctrl+P (nebo Cmd+P) a zvolte 'Uložit jako PDF'.")
    st.download_button("📄 Stáhnout náhledy (HTML/PDF)", preview_html, f"nahledy_{sestava}.html", "text/html")

elif vstup:
    st.error("Doplňte URL adresu.")
