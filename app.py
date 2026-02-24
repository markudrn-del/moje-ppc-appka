import streamlit as st
import pandas as pd
import io, random

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
            f"Jsi špičkový copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). "
            f"Cílem je maximální CTR. Brief: {b_txt}.{u_p} "
            f"FORMÁT VÝSTUPU: Vypiš pouze texty, každý na nový řádek. "
            f"BEZ čísel, BEZ odrážek, BEZ uvozovek. Prvních 15 řádků budou nadpisy, "
            f"následující 4 řádky budou popisky."
        )
        st.info("Zkopírujte tento prompt do Gemini:")
        # ZMENŠENÉ POLE S POSUVNÍKEM (height=150 zajistí kompaktnost)
        st.code(p_f, language="text", wrap_lines=True)
        # Poznámka: st.code v novějších verzích Streamlitu automaticky přidává posuvník, 
        # pokud je text dlouhý, ale pro jistotu jsem zkrátil instrukce.
    else:
        st.warning("Nejdříve vložte brief.")

st.markdown("---")

# --- 2. KROK: EDITOR ---
u_link = st.text_input("URL webu", "https://publicis.cz")
v_raw = st.text_area("Vložte texty z AI sem (čistý seznam)", height=150)

def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"]=="Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if st.button("✅ Načíst do tabulky"):
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
    st.data_editor(st.session_state.df_data, use_container_width=True, hide_index=True, key="ppc_editor", on_change=prepocet)

    # --- 3. KROK: NÁHLEDY ---
    st.markdown("---")
    st.subheader("👀 Náhledy inzerátů (6 kombinací)")
    
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
                    <div style="color: #202124; font-size: 12px; margin-bottom: 4px;">Sponzorováno • {u_link.replace('https://','')}</div>
                    <div style="color: #1a0dab; font-size: 18px; margin-bottom: 4px; line-height: 1.2;">
                        {sh[0]} – {sh[1]} – {sh[2] if len(sh)>2 else ""}
                    </div>
                    <div style="color: #4d5156; font-size: 13px; line-height: 1.4;">
                        {sd[0]} {sd[1] if len(sd)>1 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- 4. KROK: EXPORT ---
    st.markdown("---")
    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(1, 16):
        out[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5):
        out[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    
    buf = io.BytesIO
