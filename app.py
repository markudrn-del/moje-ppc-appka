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
        p_res = f"RSA: 30 nadpisu, 10 popisku. {b_txt}. {u_txt}"
        st.code(p_res)

st.markdown("---")

# 2. KROK
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("AI texty", height=200)

load = st.button("Nacist do tabulky")

# Logika barev
def get_color(v):
    c = "#ccffcc" if v >= 0 else "#ffcccc"
    return f"background-color: {c}"

# Inicializace pameti
if load and v_raw:
    ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
    rows = []
    for i, t in enumerate(ls):
        tp = "Nadpis" if i < 15 else "Popis"
        lim = 30 if tp == "Nadpis" else 90
        rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
    st.session_state.df_editor = pd.DataFrame(rows)

# Zobrazeni tabulek
if "df_editor" in st.session_state:
    df = st.session_state.df_editor
    
    st.write("### Editor")
    # Rozdelene parametry pro stabilitu editoru
    ed_out = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        key="editor_v1"
    )
    
    # Okamzity prepocet
    ed_out["Zbyva"] = ed_out.apply(
        lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), 
        axis=1
    )
    st.session_state.df_editor = ed_out

    st.write("### Barevny semafor")
    # Stylizace
    st.dataframe(
        ed_out.style.applymap(get_color, subset=["Zbyva"]),
        use_container_width=True,
        hide_index=True
    )

    # EXPORT
    st.markdown("---")
    h = ed_out[ed_out["Typ"] == "Nadpis"]["Text"].tolist()
    d = ed_out[ed_out["Typ"] == "Popis"]["Text"].tolist()
    
    res = {"Campaign": "K1", "Ad Group": "S1", "URL": u_link}
    for i in range(15):
        res[f"H{i+1}"] = h[i] if i < len(h) else ""
    for i in range(4):
        res[f"D{i+1}"] = d[i] if i < len(d) else ""
            
    csv = pd.DataFrame([res]).to_csv(index=False, sep=';', encoding='utf-8-sig')
