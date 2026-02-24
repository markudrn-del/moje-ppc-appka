import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio")

# --- CSS PRO ZELENÁ TLAČÍTKA A KOMPAKTNÍ PROMPT ---
st.markdown("""
    <style>
    /* Zelená tlačítka */
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button:hover {
        background-color: #218838 !important;
        color: white !important;
    }
    /* Omezení výšky boxu s promptem */
    .prompt-box {
        background-color: #f0f2f6; 
        border-radius: 5px; 
        padding: 10px; 
        font-family: monospace; 
        font-size: 12px; 
        height: 80px; 
        overflow-y: scroll; 
        border: 1px solid #d1d5db;
        white-space: pre-wrap;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

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
            f"Jsi špičkový copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). "
            f"Cílem je maximální CTR. Brief: {b_txt}.{u_p} "
            f"FORMÁT VÝSTUPU: Vypiš pouze texty, každý na nový řádek. "
            f"BEZ čísel, BEZ odrážek. Nejdřív 15 nadpisů, pak 4 popisky."
        )
        st.session_state.current_prompt = p_f
    else:
        st.warning("Vložte brief.")

# Zobrazení promptu a tlačítka pro kopírování
if "current_prompt" in st.session_state:
    st.info("Krok 1: Zkopírujte prompt a vložte ho do Gemini")
    st.markdown(f'<div class="prompt-box">{st.session_state.current_prompt}</div>', unsafe_allow_html=True)
    # Tlačítko pro kopírování (Streamlit nativní způsob pro schránku)
    st.copy_to_clipboard(st.session_state.current_prompt, before_text="📋 Zkopírovat prompt")

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("URL webu", "https://publicis.cz")
v_raw = st.text_area("Krok 2: Vložte texty z AI sem", height=150)

def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if st.button("✨ Vygenerovat inzeráty"):
    if v_raw.strip():
        ls = [x.strip() for x in v_raw.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

if "df_data" in st.session_state:
    st.write("### Krok 3: Upravte texty v tabulce")
    st.data_editor(st.session_state.df_data, use_container_width=True, hide_index=True, key="ppc_editor", on_change=prepocet)

    # --- 3. KROK: NÁHLEDY ---
    st.markdown("---")
    st.subheader("👀 Náhledy pro klienta (6 kombinací)")
    
    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"]=="Popis"]["Text"].tolist()

    if len(h_l) > 2 and len(d_l) > 1:
        cols = st.columns(2)
        for i in range(6):
            with cols[i % 2]:
                sh = random.sample(h_l, 3) if len(h_l)>=3 else h_l
                sd = random.sample(d_l, 2) if len(d_l)>=2 else d_l
                st.markdown(f"""
                <div style="border: 1px solid #dadce0; border-radius: 8px; padding: 12px; margin-bottom: 10px; background: white; font-family: Arial, sans-serif;">
                    <div style="color: #202124; font-size: 11px; margin-bottom: 4px;">Sponzorováno • {u_link.replace('https://','')}</div>
                    <div style="color: #1a0dab; font-size: 18px; margin-bottom: 4px; line-height: 1.2;">
                        {sh[0]} – {sh[1]} – {sh[2] if len(sh)>2 else ""}
                    </div>
                    <div style="color: #4d5156; font-size: 13px;">{sd[0]} {sd[1] if len(sd)>1 else ""}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- 4. KROK: EXPORT ---
    st.markdown("---")
    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(1, 16): out[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5): out[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        pd.DataFrame([out]).to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL pro Google Editor", buf.getvalue(), "ppc_export.xlsx")
