import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Globální design
st.set_page_config(page_title="PPC Publicis Studio", layout="wide")

st.markdown("""
<style>
    .stButton>button, .stDownloadButton>button {
        width: 100% !important; height: 45px !important;
        background-color: black !important; color: white !important;
        border-radius: 8px !important; border: none !important;
        font-weight: bold !important; font-size: 16px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #A89264 !important; transform: translateY(-1px);
    }
    .stCode, pre { height: 80px !important; min-height: 80px !important; }
    .ad-p {
        background: white; padding: 15px; border: 1px solid #ddd;
        border-radius: 8px; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    try:
        st.image("pub_logo_groupe_rvb.png", width=200)
    except:
        st.write("🦁 **Publicis**")
    st.write(f"© {datetime.now().year}")

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1: PROMPT S REZERVOU
st.subheader("1. Příprava zadání")
c_brf, c_custom = st.columns([2, 1])

with c_brf:
    brf = st.text_area("Vložte brief nebo obsah webu:", height=150)
with c_custom:
    custom_info = st.text_area("Vlastní texty / Akce / USPs:", height=150)

if st.button("✨ Vygenerovat prompt (30 nadpisů + 10 popisků)"):
    if brf:
        p_text = "Jsi PPC expert. Vygeneruj RSA inzeráty: 30 nadpisů (do 30 zn) a 10 popisků (do 90 zn). Bez vykřičníků. "
        if custom_info:
            p_text += f"DŮLEŽITÉ: Povinně zakomponuj tyto informace: {custom_info}. "
        p_text += f"Zadání pro zbytek: {brf}"
        
        st.write("**Prompt pro Gemini:**")
        st.code(p_text, language="text")
        
        st.components.v1.html(f"""
            <style>
                button {{ width: 100%; height: 45px; background-color: black; color: white;
                border: none; border-radius: 8px; cursor: pointer; font-weight: bold;
                font-size: 16px; font-family: sans-serif; transition: 0.3s; }}
                button:hover {{ background-color: #A89264; }}
            </style>
            <button onclick="navigator.clipboard.writeText(`{p_text}`).then(()=>alert('Zkopírováno!'))">
                📋 Zkopírovat prompt
            </button>
        """, height=55)
    else:
        st.warning("Zadejte text briefu.")

st.markdown("---")

# 4. KROK 2: NÁHLEDY A VERTIKÁLNÍ PŘEHLED
st.subheader("2. Výběr a Export")
col_meta, col_vstup = st.columns([1, 2])

with col_meta:
    k = st.text_input("Kampaň", "K1")
    s = st.text_input("Sestava", "S1")
    u = st.text_input("URL", "https://")

with col_vstup:
    v = st.text_area("Vložte vybrané řádky od AI (každý na nový řádek):", height=150, 
                     help="Vložte sem ty, které se vám líbí. Prvních 15 budou nadpisy, zbytek popisky.")

if v and u != "https://":
    rady = [line.strip() for line in v.split('\n') if line.strip()]
    
    # Rozdělení (automaticky detekujeme co je co, nebo bereme 15/4)
    h_list = rady[0:15]
    d_list = rady[15:19]
    
    # --- VIZUÁLNÍ KONTROLA (POD SEBOU) ---
    st.write("### 🔍 Kontrola textů pro export")
    preview_df = pd.DataFrame({
        "Typ": ["Nadpis"] * len(h_list) + ["Popis"] * len(d_list),
        "Text": h_list + d_list,
        "Délka": [len(t) for t in (h_list + d_list)]
    })
    
    def color_len(val, limit):
        return 'color: red; font-weight: bold' if val > limit else 'color: green'

    st.table(preview_df) # Tabulka pod sebou pro lepší vizuální pohled

    # --- NÁHLEDY ---
    st.write("### 👁️ Náhledy pro klienta")
    html_p = f"<h2>Nahledy - {s}</h2>"
    cols = st.columns(2)
    for i in range(4):
        sh = random.sample(h_list, min(3, len(h_list))) if h_list else ["Nadpis"]
        sd = random.sample(d_list, min(2, len(d_list))) if d_list else ["Popis"]
        ad_ui = f"""
        <div class="ad-p">
            <div style="font-size:12px; color:gray;">Sponzorováno • {u.replace("https://","")}</div>
            <div style="color:#1a0dab; font-size:18px;">{" | ".join(sh)}</div>
            <div style="color:#4d5156; font-size:14px;">{" ".join(sd)}</div>
        </div>"""
        cols[i % 2].markdown(ad_ui, unsafe_allow_html=True)
        html_p += ad_ui

    # --- CSV EXPORT (Vodorovně pro Editor) ---
    export_data = {"Campaign": k, "Ad Group": s, "Final URL": u}
    for i in range(15): export_data[f"Headline {i+1}"] = h_list[i] if i < len(h_list) else ""
    for i in range(4): export_data[f"Description {i+1}"] = d_list[i] if i < len(d_list) else ""
    
    df_csv = pd.DataFrame([export_data])
    buf = io.StringIO()
    df_csv.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    st.write("### 📊 Stažení")
    c_d1, c_d2 = st.columns(2)
    c_d1.download_button("📥 Stáhnout CSV pro Editor", buf.getvalue(), f"{s}.csv")
    c_d2.download_button("📄 Stáhnout náhledy", html_p, "nahledy.html", "text/html")

elif v:
    st.error("Doplňte URL adresu.")
