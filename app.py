import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Společný design pro všechna tlačítka
st.set_page_config(page_title="PPC Publicis Studio")

st.markdown("""
<style>
    /* Styl pro Streamlit tlačítka (Vygenerovat, CSV, atd.) */
    .stButton>button, .stDownloadButton>button {
        width: 100%;
        background-color: black !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        height: 3em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #A89264 !important;
        transform: translateY(-2px);
    }
    
    /* Zmenšené pole pro prompt */
    .stCode, pre {
        height: 80px !important;
        min-height: 80px !important;
    }
    
    /* Vzhled inzerátů */
    .ad-p {
        background: white;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar
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
        p_text = "Jsi PPC expert. RSA inzeráty: 15 nadpisů (30 zn) a 4 popisky (90 zn). "
        p_text += f"Zadání: {brf}"
        
        st.write("**Prompt pro Gemini:**")
        st.code(p_text, language="text")
        
        # HTML/JS Tlačítko se stejným designem
        st.components.v1.html(f"""
            <style>
                button {{
                    width: 100%;
                    height: 45px;
                    background-color: black;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    font-family: sans-serif;
                    transition: 0.3s;
                }}
                button:hover {{
                    background-color: #A89264;
                }}
            </style>
            <button onclick="copyPrompt()">📋 Zkopírovat prompt</button>
            <script>
            function copyPrompt() {{
                const text = `{p_text}`;
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Prompt byl zkopírován do schránky!');
                }});
            }}
            </script>
        """, height=60)
    else:
        st.warning("Zadejte text briefu.")

st.markdown("---")

# 4. KROK 2: EXPORTY
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
    html_p = "<h2>Náhledy</h2>"
    
    for i in range(4):
        sh = random.sample(h, min(3, len(h))) if h else []
        sd = random.sample(d, min(2, len(d))) if d else []
        
        ad = f"""
        <div class="ad-p">
            <div style="font-size:12px; color:gray;">Sponzorováno • {u.replace("https://","")}</div>
            <div style="color:#1a0dab; font-size:18px; font-family:Arial;">{" | ".join(sh)}</div>
            <div style="color:#4d5156; font-size:14px; font-family:Arial;">{" ".join(sd)}</div>
        </div>"""
        st.markdown(ad, unsafe_allow_html=True)
        html_p += ad

    # CSV
    data = {"Campaign": k, "Ad Group": s, "Final URL": u}
    for i in range(15): data[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4): data[f"Description {i+1}"] = d[i] if i < len(d) else ""
    
    df = pd.DataFrame([data])
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
    
    st.write("### 📊 Stažení")
    st.download_button("📥 Stáhnout CSV", buf.getvalue(), f"{s}.csv")
    st.download_button("📄 Stáhnout náhledy", html_p, "nahledy.html", "text/html")

elif v:
    st.error("Doplňte URL adresu.")
