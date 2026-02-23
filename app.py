import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PPC Inzerátovač", layout="wide")

st.title("🚀 PPC Generátor pro Google Ads Editor")

# --- NOVÁ SEKCE: GENERÁTOR PROMPTU ---
st.header("1. Příprava zadání pro Gemini")
st.info("Sem vložte podklady a aplikace vám připraví prompt, který pak jen zkopírujete do Gemini.")

# Pole pro vložení briefu nebo textu z webu
user_brief = st.text_area("Vložte text briefu nebo obsah webu:", height=150, placeholder="Např. Prodáváme kurzy vaření pro začátečníky v Praze...")

if user_brief:
    # Tady je ten schovaný Master Prompt, který se spojí s tvým textem
    master_prompt = f"""Předmět: Generování responzivních inzerátů ve vyhledávání (RSA)

Jsi expert na PPC reklamu a copywriting. Tvým úkolem je vytvořit texty pro Google Ads na základě níže uvedeného zadání.

Tvé úkoly:
1. Vytvoř přesně 15 unikátních nadpisů (každý max. 30 znaků včetně mezer).
2. Vytvoř přesně 4 unikátní popisky (každý max. 90 znaků včetně mezer).
3. Nepoužívej vykřičníky v nadpisech.
4. Zaměř se na přínosy pro zákazníka, CTA a USP.

⚠️ KRITICKÝ POŽADAVEK NA KONTROLU:
Než mi odpovíš, u každého řádku si poctivě spočítej znaky. Pokud nadpis přesahuje 30 znaků nebo popisek 90 znaků, přepiš ho tak, aby se do limitu vešel.

Formát výstupu:
Vypiš výsledky jako prostý seznam řádků bez odrážek, čísel a uvozovek. Nejdřív všech 15 nadpisů, pak hned pod ně 4 popisky. Každý text na nový řádek. Žádný jiný doprovodný text.

Zadání:
{user_brief}"""

    st.subheader("Hotový prompt pro Gemini:")
    st.code(master_prompt, language="text")
    st.warning("👆 Zkopírujte celý blok výše a vložte ho do Gemini.")

st.divider()

# --- SEKCE PRO ZPRACOVÁNÍ (Zůstává stejná) ---
st.header("2. Formátování výsledků od Gemini")
st.sidebar.header("Nastavení exportu")
campaign = st.sidebar.text_input("Kampaň", "Kampaň_1")
ad_group = st.sidebar.text_input("Sestava", "Sestava_1")
final_url = st.sidebar.text_input("URL", "https://")

raw_text = st.text_area("Sem vložte 19 řádků, které vám Gemini vygeneroval:", height=250)

if raw_text:
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
    headlines = lines[:15] + [""] * (15 - len(lines[:15]))
    descriptions = lines[15:19] + [""] * (4 - len(lines[15:19]))

    data = {"Campaign": campaign, "Ad Group": ad_group, "Final URL": final_url}
    for i in range(15): data[f"Headline {i+1}"] = headlines[i]
    for i in range(4): data[f"Description {i+1}"] = descriptions[i]

    df = pd.DataFrame([data])
    st.dataframe(df) # Pro jednoduchost teď bez barev, aby to hned jelo

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Stáhnout CSV pro Google Editor", csv, "export.csv", "text/csv")
