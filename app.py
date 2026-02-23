import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="PPC Studio", layout="wide")

# 2. Design - ciste uvozovky
st.markdown("<style>.stButton>button { width: 100%; height: 45px; background-color: black !important; color: white !important; border-radius: 8px; font-weight: bold; } .stButton>button:hover { background-color: #A89264 !important; } code { height: 70px !important; display: block; }</style>", unsafe_allow_html=True)

st.title("PPC Publicis Studio")

# 3. KROK 1
st.subheader("1. Priprava promptu")
c1, c2 = st.columns([2, 1])
b_in = c1.text_area("Brief:", height=150)
c_in = c2.text_area("Akce:", height=150)

if st.button("Vygenerovat prompt"):
    if b_in:
        p = f"RSA: 30 nadpisu, 10 popisku. Zadani: {b_in}. Akce: {c_in}"
        st.code(p)
    else:
        st.warning("Zadejte brief.")

st.markdown("---")

# 4. KROK 2
st.subheader("2. Editor a Export")
cm, cv = st.columns([1, 2])
kamp = cm.text_input("Kampan", "K1")
sest = cm.text_input("Sestava", "S1")
link = cm.text_input("URL", "https://")
vstup = cv.text_area("Vlozte texty od AI:", height=150)

# Tlacitko bez emoji pro maximalni stabilitu
btn_load = st.button("Nacist do tabulky")

if (btn_load or vstup) and link != "https://":
    lines = [l.strip() for l in vstup.split('\n') if l.strip()]
    if lines:
        # DATA
        rows = []
        for i, txt in enumerate(lines):
            typ = "Nadpis" if i < 15 else "Popis"
            lim = 30 if typ == "Nadpis" else 90
            rem = lim - len(txt)
            rows.append({"Typ": typ, "Text": txt, "Zbyva": rem})
        
        df = pd.DataFrame(rows)
        st.write("### Editace")
        
        # EDITOR
        ed_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            key="e1"
        )
        
        # Prepocet zbyvajicich znaku
        ed_df["Zbyva"] = ed_df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
            axis=1
        )
        
        h_f = ed_df[ed_df["Typ"] == "Nadpis"]["Text"].tolist()
        d_f = ed_df[ed_df["Typ"] == "Popis"]["Text"].tolist()
        
        # NAHLEDY
        st.write("### Nahledy")
        n1, n2 = st.columns(2)
        cl_u = link.replace("https://", "")
        for i in range(4):
            sh = random.sample(h_f, min(3, len(h_f))) if h_f else ["..."]
            sd = random.sample(d_f, min(2, len(d_f))) if d_f else ["..."]
            t_str = " | ".join(sh)
            d_str = " ".join(sd)
            ad = f'<div style="background:white;padding:15px;border:1px solid #ddd;border-radius:8px;margin-bottom:10px;font-family:Arial;"><div style="font-size:12px;color:gray;">Sponzorovano • {cl_u}</div><div style="color:#1a0dab;font-size:18px;">{t_str}</div><div style="color:#4d5156;font-size:14px;">{d_str}</div></div>'
            if i % 2 == 0: n1.
