import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide", page_title="PPC Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi špičkový copywriter. Napiš RSA (15 nadpisů do 30 zn., 4 popisky do 90 zn.). "
            f"Musí být kreativní pro vysoké CTR. Psychologie prodeje. "
            f"Zpracuj brief: {b_txt}.{u_p}"
        )
        st.info("Zkopírujte do AI:")
        st.code(p_f)

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("Finální URL", "https://publicis.cz")
v_raw = st.text_area("Vložte texty z AI sem", height=200)

def prepocet():
    if "ppc_editor" in st.session_state and "df_data" in st.session_state:
        ed_state = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        # Propis změn
        for r, h in ed_state.get("edited_rows", {}).items():
            for col, val in h.items():
                df.at[int(r), col] = val
        # Přepočet limitů
        def get_rem(row):
            lim = 30 if row["Typ"] == "Nadpis" else 90
            return lim - len(str(row["Text"]))
        df["Zbyva"] = df.apply(get_rem, axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
    if v_raw.strip():
        ls = [l.strip() for l in v_raw.split('\n') if l.strip()]
        rows = []
        for i, t in enumerate(ls):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

if "df_data" in st.session_state:
    st.write("### Editor")
    st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocet
    )

    # --- 3. KROK: EXPORT (OPRAVA DIKRITIKY) ---
    st.markdown("---")
    df_f = st.session_state.df_data
    h = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()
    
    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(15):
        out[f"Headline {i+1}"] = h[i] if i < len(h) else ""
    for i in range(4):
        out[f"Description {i+1}"] = d[i] if i < len(d) else ""
    
    # EXCEL-FRIENDLY EXPORT: utf-16 s tabulátorem je pro Excel nejjistější
    df_final = pd.DataFrame([out])
    csv_buffer = io.StringIO()
    df_final.to_csv(csv_buffer, index=False, sep='\t', encoding='utf-16')
    
    st.download_button(
        label="📥 Stáhnout CSV pro Excel (bez chyb)",
        data=csv_buffer.getvalue(),
        file_name="ppc_export.csv",
        mime="text/csv"
    )
