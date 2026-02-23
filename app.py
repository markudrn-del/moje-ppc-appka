import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Konfigurace stránky
st.set_page_config(
    page_title="PPC generátor inzerátů", 
    page_icon="🎯", 
    layout="centered"
)

# Minimalistické CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #000000;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR S PODPISEM ---
with st.sidebar:
    st.markdown("### O aplikaci")
    st.info("Tento nástroj pomáhá PPC specialistům efektivně přetvářet briefy do formátu pro Google Ads Editor.")
    st.markdown("---")
    st.markdown(f"**Vytvořil:** Martin Kudrna, {datetime.now().year}")
    st.markdown("**Poslední update:** 23. února 2026")

# --- HLAVNÍ OBSAH ---
st.title("🎯 PPC generátor inzerátů")
st.caption("Minimalistický nástroj pro tvorbu RSA inzerátů z briefu do Google Editoru.")

# 1. SEKCE: GENERÁTOR PROMPTU
with st.container():
    st.subheader("1. Příprava zadání")
    user_brief = st.text_area(
        "Vložte brief nebo obsah webu", 
        height=150, 
        placeholder="Popište produkt, benefity a cílovou skupinu..."
    )

    if st.button("✨ Vygenerovat prompt pro Gemini"):
        if user_brief:
            master_prompt = f"""Předmět: Generování responzivních inzerátů ve vyhledávání (RSA)
Jsi expert na PPC reklamu. Vytvoř 15 nadpisů (max 30 znaků) a 4 popisky (max 90 znaků).
Bez vykřičníků v nadpisech. Poctivě spočítej znaky!
Formát: jen 19 řádků pod sebou (15 nadpisů, pak 4 popisky). Nic jiného nepiš.
Zadání: {user_brief}"""
            
            st.info("Prompt je připraven níže. Zkopírujte ho do Gemini.")
            st.code(master_prompt, language="text")
        else:
            st.warning("Před vygenerováním vložte text zadání.")

st.markdown("---")

# 2. SEKCE: EXPORT
with st.container():
    st.subheader("2. Export pro Google Editor")
    
    col1, col2 = st.columns(2)
    with col1:
        camp_input = st.text_input("Kampaň", placeholder="Kampaň_01")
    with col2:
        group_input = st.text_input("Sestava", placeholder="Sestava_01")
    
    final_url = st.text_input("Finální URL", placeholder="https://www.vasweb.cz")

    raw_text = st.text_area("Vložte 19 řádků z Gemini", height=200, placeholder="Nadpis 1\nNadpis 2\n...")

    if raw_text:
        if not final_url:
            st.error("Pro export je nutné vyplnit Finální URL.")
        else:
            lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
            headlines = lines[:15] + [""] * (15 - len(lines[:15]))
            descriptions = lines[15:19] + [""] * (4 - len(lines[15:19]))

            campaign = camp_input if camp_input else "Doplnit_Kampan"
            ad_group = group_input if group_input else "Doplnit_Sestavu"

            data = {"Campaign": campaign, "Ad Group": ad_group, "Final URL": final_url}
            for i in range(15): data[f"Headline {i+1}"] = headlines[i]
            for i in range(4): data[f"Description {
