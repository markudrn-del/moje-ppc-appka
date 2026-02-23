import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup a styl
st.set_page_config(page_title="PPC Publicis Studio")

st.markdown("""
<style>
    /* Styl tlačítek */
    .stButton>button {
        width: 100%;
        background-color: black;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #A89264;
    }

    /* !!! KLÍČOVÁ ZMĚNA: FYZICKÉ ZMENŠENÍ CELÉHO POLE !!! */
    .stCode {
        height: 100px !important;
        overflow-y: auto !important;
    }
    pre {
        height: 100px !important;
        padding: 10px !important;
    }
    code {
        white-space: pre !important;
    }

    /* Náhledy inzerátů */
    .ad-p {
        background: white;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar a Název
with st.sidebar:
    try:
        st.image("pub_logo_groupe_rvb.png", width=200)
    except:
        st.write("🦁 **Publicis**")

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1: PROMPT
st.subheader("1. Zadání")
brf = st.text_area("Vložte brief:", height=200)

if st.button("✨ Vygenerovat prompt"):
    if brf:
        p = "Jsi PPC expert. RSA inzeráty: 15 nadpisů (30 zn) a 4 popisky (90 zn). "
        p += f"Zadání: {brf}"
        st.write("**Prompt (zkopírujte ikonkou vpravo):**")
        # Toto pole bude nyní fyzicky malé (100px)
        st.code(p, language="text")
    else:
        st.warning("Zadejte text briefu.")

st.markdown("---")

# 4. KROK 2: NÁHLEDY A CSV
st.subheader("2. Náhledy a Export")
c1, c2 = st.columns(2)
k = c1.text_input("Kampaň", "K1")
s = c2.text_input("Sestava", "S1")
u = st.text_input("URL", "https://")
v = st.text_area("Vložte 19 řádků od AI:", height=200)

if v and u != "https://":
    r = [line.strip() for line in v.split('\n') if line.strip()]
    h = r[0:15]
    d = r[15:19]
    
    st.write("### 👁️ Náhledy pro klienta")
    html_p = "<h2>Náhledy inzerátů</h2>"
    
    for i in range(4):
        sh = random.sample(h, 3) if len(h) >= 3 else h
        sd = random.sample(d, 2) if len(d) >= 2 else d
        t = " | ".join(sh)
        ds = " ".join(sd)
        
        ad = f"""
        <div class="ad-p">
            <div style="font-size:12px; color:gray;">Sponzorováno • {u.replace("https://","")}</div>
            <div style="color:#1a0dab; font-size:18px; font-family:arial;">{t}</div>
            <div style="color:#4d5156; font-size:14px; font-family:arial;">{ds}</div>
        </div>"""
        st.markdown(ad, unsafe_allow_html=True)
        html_p += ad

    # CSV Data
    data = {"Campaign": k, "Ad Group": s, "Final URL": u}
    for i in range(15):
        data[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4):
        data[f"Description {i+1}"] = d[i] if i < len(d) else ""
    
    df = pd.DataFrame([data])
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    st.write("### 📊 Stažení")
    st.download_button("📥 Stáhnout CSV pro Editor", buf.getvalue(), f"{s}.csv")
    st.download_button("📄 Stáhnout náhledy (PDF/HTML)", html_p, "nahledy.html", "text/html")

elif v:
    st.error("Doplňte URL adresu.")
