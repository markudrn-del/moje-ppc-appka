import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: BRIEF A PROMPT ---
st.subheader("1. Brief a generování promptu")
col1, col2 = st.columns(2)

with col1:
    b_txt = st.text_area("Vložte brief", height=100)
with col2:
    u_txt = st.text_input("Vlastní USPs (nepovinné)")

if st.button("Generovat prompt pro AI"):
    if b_txt:
        prompt_final = f"RSA: 30 nadpisů, 10 popisků. {b_txt}. {u_txt}"
        st.info("Zkopírujte tento prompt do ChatGPT/Gemini:")
        st.code(prompt_final)
    else:
        st.warning("Nejdříve vložte brief.")

st.markdown("---")

# --- 2. KROK: EDITOR ---
st.subheader("2. Editor inzerátů")

u_link = st.text_input("Finální URL webu", "https://publicis.cz")
v_raw = st.text_area("Vložte vygenerované texty od AI sem (každý na nový řádek)", height=200)

load = st.button("✅ Načíst texty do tabulky")

# Inicializace session state pro tabulku
if load and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df = pd.DataFrame(rows)

# Samotný editor
if "df" in st.session_state:
    st.write("### Upravte texty v tabulce:")
    st.caption("Tip: Po úpravě textu stiskněte Enter nebo klikněte jinam. Počet znaků se ihned aktualizuje.")
    
    # Zobrazení editoru
    # Výsledek editoru ukládáme a hned přepočítáváme
    ed_df = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor_v14"
    )

    # OKAMŽITÝ PŘEPOČET ZNAKŮ (I DO MÍNUSU)
    ed_df["Zbyva"] = ed_df.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    
    # Synchronizace stavu
    st.session_state.df = ed_df

    # --- 3. KROK: EXPORT ---
    st.markdown("---")
    
    # Příprava dat pro Google Ads formát
    h = ed_df[ed_df["Typ"] == "Nadpis"]["Text"].tolist()
    d = ed_df[ed_df["Typ"] == "Popis"]["Text"].tolist()
    
    export_dict = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(15):
        export_dict[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4):
        export_dict[f"Description {i+1}"] = d[i] if i < len(d) else ""
            
    csv_final = pd.DataFrame([export_dict]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    
    st.download_button(
        label="📥 Stáhnout CSV pro Google Ads Editor",
        data=csv_final,
        file_name="ppc_export.csv",
        mime="text/csv"
    )
else:
    st.info("Čekám na načtení textů přes tlačítko výše.")
