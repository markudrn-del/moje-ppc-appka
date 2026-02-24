import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")

# --- CSS DESIGN ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stCodeBlock div {
        max-height: 120px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- 1. KROK: VSTUPY A PROMPT ---
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("Vlastní USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = (
            f"Jsi špičkový copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). "
            f"Cílem je maximální CTR. Brief: {b_txt}.{u_p} "
            f"FORMÁT VÝSTUPU: Vypiš pouze texty, každý na nový řádek. "
            f"BEZ čísel, BEZ odrážek. Nejdřív 15 nadpisů, pak 4 popisky."
        )
        st.session_state.current_prompt = p_f

if "current_prompt" in st.session_state:
    st.success("Krok 1: Zkopírujte prompt a vložte ho do Gemini")
    st.code(st.session_state.current_prompt, language="text")

st.markdown("---")

# --- 2. KROK: VLOŽENÍ TEXTU ---
u_link = st.text_input("URL webu", "https://publicis.cz")

# Přidali jsme parametr key, aby Streamlit sledoval změnu v reálném čase
v_raw = st.text_area(
    "Krok 2: Vložte texty z AI sem", 
    height=150, 
    placeholder="Sem vložte vygenerovaný seznam z Gemini...",
    key="ai_input" 
)

# LOGIKA PRO TLAČÍTKO - Teď reaguje na hodnotu v session_state
if st.session_state.ai_input.strip():
    if st.button("✨ Vygenerovat inzeráty"):
        ls = [x.strip() for x in st.session_state.ai_input.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()
else:
    st.info("💡 Jakmile sem vložíte texty, objeví se zelené tlačítko.")

# --- 3. KROK: TABULKA A NÁHLEDY ---
def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if "df_data" in st.session_state:
    st.markdown("---")
    st.write("### Krok 3: Zkontrolujte a upravte texty")
    st.data_editor(st.session_state.df_data, use_container_width=True, hide_index=True, key="ppc_editor", on_change=prepocet)

    st.subheader("👀 Náhledy pro klienta")
    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"]=="Popis"]["Text"].tolist()

    if len(h_l) >= 2 and len(d_l) >= 1:
        cols = st.columns(2)
        for i in range(6):
            with cols[i % 2]:
                sh = random.sample(h_l, min(3, len(h_l)))
                sd = random.sample(d_l, min(2, len(d_l)))
                h_str = " – ".join(sh)
                d_str = " ".join(sd)
                
                st.markdown(f"""<div style="border:1px solid #dadce0;border-radius:8px;padding:12px;margin-bottom:10px;background:white;font-family:Arial;">
<div style="color:#202124;font-size:11px;margin-bottom:4px;">Sponzorováno • {u_link.replace('https://','')}</div>
<div style="color:#1a0dab;font-size:18px;margin-bottom:4px;line-height:1.2;">{h_str}</div>
<div style="color:#4d5156;font-size:13px;">{d_str}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(1, 16): 
        out[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5): 
        out[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        pd.DataFrame([out]).to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL", buf.getvalue(), "ppc_export.xlsx")
