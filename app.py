import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PPC Inzerátovač", layout="wide")

st.title("🚀 PPC Generátor pro Google Ads Editor")

# --- SEKCE 1: GENERÁTOR PROMPTU ---
st.header("1. Příprava zadání pro Gemini")
st.markdown("Zde si připravte text, který vložíte do svého placeného Gemini.")

user_brief = st.text_area("Vložte text z webu nebo brief:", placeholder="Např. Prodáváme ekologické láhve na vodu...")

master_prompt_template = """Předmět: Generování responzivních inzerátů ve vyhledávání (RSA)

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
"""

if user_brief:
    full_prompt = master_prompt_template + user_brief
    st.text_area("Hotový prompt (zkopírujte do Gemini):", full_prompt, height=200)
    st.info("👆 Zkopírujte text výše, vložte ho do Gemini a pak se vraťte sem s výsledkem.")

st.divider()

# --- SEKCE 2: ZPRACOVÁNÍ VÝSLEDKŮ ---
st.header("2. Formátování pro Google Editor")

# Boční panel s nastavením
st.sidebar.header("Nastavení kampaně")
campaign = st.sidebar.text_input("Název kampaně", "Kampaň_1")
ad_group = st.sidebar.text_input("Název sestavy", "Sestava_1")
final_url = st.sidebar.text_input("Finální URL", "https://www.priklad.cz")

raw_text = st.text_area("Sem vložte 19 řádků od Gemini:", 
                        height=250, 
                        placeholder="Nadpis 1\nNadpis 2\n...")

if raw_text:
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    headlines = lines[:15]
    descriptions = lines[15:19]
    
    headlines += [""] * (15 - len(headlines))
    descriptions += [""] * (4 - len(descriptions))

    data = {"Campaign": campaign, "Ad Group": ad_group, "Final URL": final_url}
    for i in range(15): data[f"Headline {i+1}"] = headlines[i]
    for i in range(4): data[f"Description {i+1}"] = descriptions[i]

    df = pd.DataFrame([data])

    def color_length(val, max_len):
        return 'background-color: #ff4b4b; color: white' if len(str(val)) > max_len else ''

    styled_df = df.style.applymap(lambda x: color_length(x, 30), subset=[f"Headline {i+1}" for i in range(15)])\
                       .applymap(lambda x: color_length(x, 90), subset=[f"Description {i+1}" for i in range(4)])

    st.dataframe(styled_df)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    st.download_button("📥 Stáhnout CSV pro Google Editor", csv_buffer.getvalue(), f"export_{ad_group}.csv", "text/csv")
