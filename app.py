import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="PPC Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi top copywriter. Napiš RSA (15 nadpisů do 30 zn., 4 popisky do 90 zn.). "
            f"Musí být úderné pro vysoké CTR. Psychologie prodeje. "
            f"Brief: {b_txt}.{u_p}"
        )
        st.info("Zkopírujte do AI:")
        st.code(p_f)

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("AI texty sem", height=200)

# Funkce přepočtu rozdělená na řádky kvůli chybám editoru
def prepocet():
    if "ppc_editor" in st.session_state:
        st_ed = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        for r, h in st_ed.get("edited_rows", {}).items():
            for col, val in h.items():
                df.at[int(r), col] = val
        
        # Bezpečný výpočet znaků
        def get_rem(row):
            limit = 30 if row["Typ"] == "Nadpis" else 90
            return limit - len(str(row["Text"]))
        
        df["Zbyva"] = df.apply(get_rem, axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
    if v_raw.strip():
        ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
        data = []
        for i, t in enumerate(ls):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            data.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(data)
        st.rerun()

if "df_data" in st.session_state:
    st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocet
    )

    # --- 3. KROK: EXPORT ---
    st.markdown("---")
    df_f = st.session_state.df_data
    h = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()
    
    out = {"Campaign": "K1", "Ad Group": "S1", "Final URL": u_link}
    for i in range(15):
        out[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4):
        out[f"Description {i+1}"] = d[i] if i < len(d) else ""
            
    csv = pd.DataFrame([out]).to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.download_button("📥 Stáhnout CSV", csv, "export.csv")
