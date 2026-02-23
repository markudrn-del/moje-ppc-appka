import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide", page_title="PPC Studio")
st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief (o čem je kampaň)", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs (budou povinně v inzerátech)")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" Do inzerátů povinně a organicky zakomponuj tato USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi nejlepší seniorní copywriter. Napiš RSA inzerát (15 nadpisů do 30 znaků, 4 popisky do 90 znaků). "
            f"Texty musí být úderné pro maximální CTR. "
            f"Zpracuj tento brief: {b_txt}.{u_p}"
        )
        st.info("Zkopírujte tento prompt do AI:")
        st.code(p_f)

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("Finální URL", "https://publicis.cz")
v_raw = st.text_area("Vložte texty vygenerované AI sem", height=200)

def prepocet():
    if "ppc_editor" in st.session_state and "df_data" in st.session_state:
        ed_state = st.session_state["ppc_editor"]
        df = st.session_state.df_data
        for r, h in ed_state.get("edited_rows", {}).items():
            for col, val in h.items():
                df.at[int(r), col] = val
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

    # --- 3. KROK: EXPORT PRO GOOGLE ADS EDITOR ---
    st.markdown("---")
    df_f = st.session_state.df_data
    h = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()
    
    # POUŽITÍ OFICIÁLNÍCH NÁZVŮ SLOUPCŮ
    out = {
        "Campaign": "Kampaň 1", 
        "Ad Group": "Sestava 1", 
        "Final URL": u_link
    }
    
    # Google Ads Editor preferuje "Headline 1", "Headline 2" atd.
    for i in range(1, 16):
        out[f"Headline {i}"] = h[i-1] if i-1 < len(h) else ""
    
    # A "Description 1", "Description 2" atd.
    for i in range(1, 5):
        out[f"Description {i}"] = d[i-1] if i-1 < len(d) else ""
    
    final_df = pd.DataFrame([out])

    # Export do Excelu (řeší diakritiku v záhlaví i obsahu)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='RSA_Import')
    
    st.download_button(
        label="📥 Stáhnout EXCEL pro Google Ads Editor",
        data=output.getvalue(),
        file_name="ppc_import_google.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
