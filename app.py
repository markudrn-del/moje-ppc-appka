import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Konfigurace a Rebranding
st.set_page_config(page_title="PPC Publicis Studio", layout="centered")

st.markdown("""
    <style>
    /* Hlavní název a barvy */
    .main-title { color: #000000; font-weight: bold; }
    
    /* Styl tlačítek s hover efektem */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A89264; /* Publicis Gold */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* ZMENŠENÍ ŠEDÉHO POLE (PROMPT) */
    code {
        height: 100px !important; /* Fixní malá výška */
        min-height: 100px !important;
        display: block;
        overflow-y: auto;
        background-color: #f0f2f6 !important;
        border-radius: 5px;
    }

    /* Vzhled inzerátů pro náhled */
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
    .ad-title { color: #1a0dab; font-size: 20px; display: block; margin-bottom: 4px; }
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
    st.write(f"© {datetime.now().year} PPC Publicis Studio")

# 3. Hlavní obsah
st.title("🦁 PPC Publicis Studio")

# --- KROK 1 ---
st.subheader("1. Příprava zadání")
brief = st.text_area("Vložte brief:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brief:
        p = f"Jsi PPC expert. RSA inzeraty: 15 nadpisu (30 zn) a 4 popisky (90 zn). Bez vykricniku. Zadani: {brief}"
        st.write("**Prompt pro Gemini (zkopírujte):**")
        st.code(p, language="text") # Toto pole je nyní díky CSS malé
    else:
        st.warning("Zadejte zadání.")

st.markdown("---")

# --- KROK 2 ---
st.subheader("2. Export a Náhledy")
c1, c2 = st.columns(2)
kampan = c1.text_input("Kampaň", "K_01")
sestava = c2.text_input("Sestava", "S_01")
web = st.text_input("URL", "https://")
vstup = st.text_area("Vložte 19 řádků od AI:", height=200)

if vstup and web != "https://":
    rady = [r.strip() for r in vstup.split('\n') if r.strip()]
    h_list = rady[0:15]
    d_list = rady[15:19]
    
    # Náhledy pro klienta
    st.write("### 👁️ Náhledy pro klienta")
    preview_html = f"<h1>PPC Publicis Studio - Náhledy</h1>"
    
    for i in range(4):
        sh = random.sample(h_list, 3) if len(h_list) >= 3 else h_list
        sd = random.sample(d_list, 2) if len(d_list) >= 2 else d_list
        title = " | ".join(sh)
        desc = " ".join(sd)
        url_clean = web.replace("https://","")
        
        ad_code = f"""
        <div class="ad-preview">
            <div class="ad-url">Sponzorováno • {url_clean}</div>
            <div class="ad-title">{title}</div>
            <div class="ad-desc">{desc}</div>
        </div>"""
        st.markdown(ad_code, unsafe_allow_html=True)
        preview_html += ad_code

    # Export CSV
    data = {"Campaign": kampan, "Ad Group": sestava, "Final URL": web}
    for i in range(15): data[f"Headline {i+1}"] = h_list[i] if i < len(h_list) else ""
    for i in range(4): data[f"Description {i+1}"] = d_list[i] if i < len(d_list) else ""
    df = pd.DataFrame([data])
    
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    c_d1, c_d2 = st.columns(2)
    c_d1.download_button("📥 Stáhnout CSV", buf.getvalue(), f"{sestava}.csv")
    c_d2.download_button("📄 Stáhnout náhledy (PDF/HTML)", preview_html, f"nahledy.
