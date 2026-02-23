import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="PPC Studio", layout="wide")

# 2. CSS styl bez víceřádkových bloků
st.markdown("<style>.stButton>button { width: 100%; height: 45px; background-color: black !important; color: white !important; border-radius: 8px; font-weight: bold; } .stButton>button:hover { background-color: #A89264 !important; } code { height: 70px !important; display: block; }</style>", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Příprava promptu")
b = st.text_area("Brief:", height=150)
c = st.text_input("Vlastní akce/USPs:")

if st.button("✨ Vygenerovat"):
    if b:
        p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {b}. Akce: {c}"
        st.code(p)
        st.write("Zkopírujte prompt výše.")
    else:
        st.warning("Zadejte brief.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Editor a Export")
col_m, col_v = st.columns([1, 2])
kamp = col_m.text_input("Kampaň", "K1")
sest = col_m.text_input("Sestava", "S1")
link = col_m.text_input("URL", "https://")
vstup = col_v.text_area("Vložte texty od AI:", height=150)

load = st.button("⚙️ Načíst do tabulky")

if (load or vstup) and link != "https://":
    lines = [l.strip() for l in vstup.split('\n') if l.strip()]
    if lines:
        rows = []
        for i, txt in enumerate(lines):
            t = "Nadpis" if i < 15 else "Popis"
            rows.append({"Typ": t, "Text": txt})
        
        df = pd.DataFrame(rows)
        st.write("### 📝 Editujte v tabulce:")
        
        # INTERAKTIVNÍ EDITOR
        ed_df = st.data_editor(df, use_container_width=True, hide_index=True, key="ed1")
        
        h_f = ed_df[ed_df["Typ"] == "Nadpis"]["Text"].tolist()
        d_f = ed_df[ed_df["Typ"] == "Popis"]["Text"].tolist()
        
        # Náhledy - upraveno na jeden řádek pro stabilitu
        st.write("### 👁️ Náhledy")
        n1, n2 = st.columns(2)
        h_all = ""
        cl_u = link.replace("https://", "")
        
        for i in range(4):
            sh = random.sample(h_f, min(3, len(h_f))) if h_f else ["..."]
            sd = random.sample(d_f, min(2, len(d_f))) if d_f else ["..."]
            title = " | ".join(sh)
            desc = " ".join(sd)
            
            # HTML kód na jednom řádku, aby ho editor neuřízl
            ad = f'<div style="background:white;padding:15px;border:1px solid #ddd;border-radius:8px;margin-bottom:10px;font-family:Arial;"><div style="font-size:12px;color:gray;">Sponzorováno • {cl_u}</div><div style="color:#1a0dab;font-size:18px;">{title}</div><div style="color:#4d5156;font-size:14px;">{desc}</div></div>'
            
            if i % 2 == 0: n1.markdown(ad, unsafe_allow_html=True)
            else: n2.markdown(ad, unsafe_allow_html=True)
            h_all += ad
            
        # Export
        st.write("### 📊 Export")
        exp = {"Campaign": kamp, "Ad Group": sest, "Final URL": link}
        for i in range(15): exp[f"Headline {i+1}"] = h_f[i] if i < len(h_f) else ""
        for i in range(4): exp[f"Description {i+1}"] = d_f[i] if i < len(d_f) else ""
        
        buf = io.StringIO()
        pd.DataFrame([exp]).to_csv(buf, index=False, sep=';', encoding='utf-8-sig')
        st.download_button("📥 Stáhnout CSV", buf.getvalue(), f"{sest}.csv")

elif vstup:
    st.warning("Zadejte URL (jinou než https://) pro aktivaci tabulky.")
