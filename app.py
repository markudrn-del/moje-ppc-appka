import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Styl a Setup
st.set_page_config(page_title="PPC Studio")

st.markdown("""
<style>
.stButton>button {
    width: 100%;
    background-color: black;
    color: white;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #A89264;
}
code {
    height: 80px !important;
    display: block;
    overflow-y: auto;
}
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
    L = "pub_logo_groupe_rvb.png"
    try:
        st.image(L, width=200)
    except:
        st.write("🦁 **Publicis**")

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Zadání")
brf = st.text_area("Vložte brief:", height=200)

if st.button("✨ Prompt"):
    if brf:
        p = "RSA: 15 nadpisu, 4 popisky. "
        p += f"Zadani: {brf}"
        st.write("**Prompt:**")
        st.code(p, language="text")
    else:
        st.warning("Prázdné.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Náhledy a CSV")
c1, c2 = st.columns(2)
k = c1.text_input("Kampaň", "K1")
s = c2.text_input("Sestava", "S1")
u = st.text_input("URL", "https://")
v = st.text_area("19 řádků od AI:", height=200)

if v and u != "https://":
    r = [l.strip() for l in v.split('\n') if l]
    h = r[0:15]
    d = r[15:19]
    
    st.write("### 👁️ Náhledy")
    ht = "<h2>Nahledy</h2>"
    
    for i in range(4):
        sh = random.sample(h, 3) if len(h)>=3 else h
        sd = random.sample(d, 2) if len(d)>=2 else d
        t = " | ".join(sh)
        ds = " ".join(sd)
        
        ad = f"""
        <div class="ad-p">
            <div class="ad-title">{t}</div>
            <div class="ad-desc">{ds}</div>
        </div>"""
        st.markdown(ad, unsafe_allow_html=True)
        ht += ad

    # CSV
    data = {"Campaign": k, "Ad Group": s, "URL": u}
    for i in range(15):
        data[f"H{i+1}"] = h[i] if i<len(h) else ""
    for i in range(4):
        data[f"D{i+1}"]
