import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PPC Inzerátovač", layout="wide")

st.title("🚀 PPC Generátor pro Google Ads Editor")
st.markdown("Vložte texty vygenerované AI a stáhněte si hotový soubor pro import.")

# Boční panel s nastavením
st.sidebar.header("Nastavení kampaně")
campaign = st.sidebar.text_input("Název kampaně", "Kampaň_1")
ad_group = st.sidebar.text_input("Název sestavy", "Sestava_1")
final_url = st.sidebar.text_input("Finální URL", "https://www.priklad.cz")

# Hlavní vstup textu
st.subheader("1. Vložte texty od AI")
raw_text = st.text_area("Vložte nadpisy (každý na nový řádek) a pod ně popisky:", 
                        height=300, 
                        placeholder="Nadpis 1\nNadpis 2\n...\nPopisek 1\nPopisek 2...")

if raw_text:
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    # Rozdělení na nadpisy (prvních 15) a popisky (další 4)
    headlines = lines[:15]
    descriptions = lines[15:19]
    
    # Doplnění prázdných hodnot, pokud jich je méně
    headlines += [""] * (15 - len(headlines))
    descriptions += [""] * (4 - len(descriptions))

    # Vytvoření dat pro tabulku
    data = {
        "Campaign": campaign,
        "Ad Group": ad_group,
        "Final URL": final_url
    }
    
    for i in range(15):
        data[f"Headline {i+1}"] = headlines[i]
    for i in range(4):
        data[f"Description {i+1}"] = descriptions[i]

    df = pd.DataFrame([data])

    # Funkce pro barvení buněk podle délky
    def color_length(val, max_len):
        if len(str(val)) > max_len:
            return 'background-color: #ff4b4b; color: white'
        return ''

    st.subheader("2. Kontrola délky a náhled")
    
    # Aplikace stylu (st.dataframe nepodporuje barvy tak snadno, použijeme styler)
    styled_df = df.style.applymap(lambda x: color_length(x, 30), subset=[f"Headline {i+1}" for i in range(15)])\
                       .applymap(lambda x: color_length(x, 90), subset=[f"Description {i+1}" for i in range(4)])

    st.dataframe(styled_df)

    # Validace délek pro varování
    over_limit = any(len(h) > 30 for h in headlines) or any(len(d) > 90 for d in descriptions)
    if over_limit:
        st.error("⚠️ Pozor! Některé texty jsou příliš dlouhé (červené buňky). Google Editor je nepřijme.")

    # Export do CSV
    st.subheader("3. Export")
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_output = csv_buffer.getvalue()

    st.download_button(
        label="📥 Stáhnout CSV pro Google Editor",
        data=csv_output,
        file_name=f"export_ads_{ad_group}.csv",
        mime="text/csv",
    )
