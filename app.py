import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")
st.title("PPC Publicis Studio")

# 1. KROK
b_txt = st.text_area("Brief")
u_txt = st.text_input("USPs")

if st.button("Generovat prompt"):
    if b_txt:
        st.code(f"RSA: 30 nadpisu, 10 popisku. {b_txt}. {u_txt}")

st.markdown("---")

# 2. KROK
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("AI texty", height=200)
load = st.button("Nacist do tabulky")

# Funkce pro barvy (Zelena / Cervena)
def get_style(row):
    color = "#ccffcc" if row["Zbyva"] >= 0 else "#ffcccc"
    return [f"background-color: {color}"] * len(row)

# Inicializace pameti
if load and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df_editor = pd.DataFrame(rows)

# Zobrazeni JEDNE tabulky
if "df_editor" in st.session_state:
    df = st.session_state.df_editor
    
    st.write("### Upravte texty (Zbyva se prepocita po potvrzeni):")
    
    # Tady je ten trik: Editoru predame ostylovany DataFrame
    # Kazdy radek bude mit barvu podle sloupce Zbyva
    styled_df = df.style.apply(get_style, axis=1)
    
    ed_out = st.data_editor(
        styled_df,
        use_container_width=True,
        hide_index=True,
        key="single_editor_v1"
    )
    
    # Okamzity prepocet hodnot (pro probehnuti pri pristim refreshu)
    ed_out["Zbyva"] = ed_out.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    st.session_state.df_editor = ed_out

    # EXPORT
    st.markdown("---")
    h = ed_out[ed_out["Typ"] == "Nadpis"]["Text"].tolist()
    d = ed_out[ed_out["Typ"] == "Popis"]["Text"].tolist()
    
    res = {"Campaign": "K1", "Ad Group": "S1", "URL": u_link}
    for i in range(15): res[f"H{i+1}"] = h[i] if i < len(h) else ""
    for i in range(4): res[f"D{i+1}"] = d[i] if i < len(d) else ""
            
    csv = pd.DataFrame([res]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("Stahnout hotove CSV", csv, "export_ppc.csv")
