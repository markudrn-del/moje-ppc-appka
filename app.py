import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO SROVNÁNÍ VÝŠKY, ZÁKAZ ČERVENÉ A POČÍTADLO
st.markdown("""<style>
/* Zákaz červené barvy při kliknutí/focusu pro všechna pole */
.stTextArea textarea:focus, .stTextInput input:focus,
.stTextArea textarea, .stTextInput input { 
    border-color: #d1d5db !important; box-shadow: none !important; 
    background-color: white !important; color: black !important;
}
/* Srovnání výšky USPs pole s Briefem */
div[data-testid="stTextInput"] input { height: 100px !important; }
/* Zelené podbarvení aktivního kroku */
.step-active textarea, .step-active input { 
    background-color: #f0fff4 !important; border: 1px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; height: 3em; }
.active-btn button { background-color: #28a745 !important; color: white !important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:12px; height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# KROK 1: VSTUPY
c1, c2 = st.columns(2)
br_v = st.session_state.get("br", "")
p_ex = "p" in st.session_state
cp_ok = st.session_state.get("cp", False)

with c1:
    cl1 = "step-active" if (br_v.strip() and not p_ex) else ""
    st.markdown(f'<div class="{cl1}">', 1)
    b = st.text_area("1. Brief nebo web", height=100, key="br")
    st.markdown('</div>', 1)
with c2:
    # USPs s vynucenou výškou přes CSS výše
    u = st.text_input("2. USPs (volitelné)", key="usps_in")

# Tlačítko 1
b1_cl = "active-btn" if (b.strip() and not p_ex) else ""
st.markdown(f'<div class="{b1_cl}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi PPC copywriter. RSA (15 nadpisů, 4 popisky). "
                         f"Brief: {b}. USPs: {u}. Jen texty, každý nový řádek.")
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

# KROK 2: PROMPT
if p_ex:
    st.markdown('<div style="margin-top:20px;"></div>', 1)
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    b2_cl = "active-btn" if not cp_ok else ""
    st.markdown(f'<div class="{b2_cl}">', 1)
    if st.button("📋 Zkopírovat prompt"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

# KROK 3: VLOŽENÍ VÝSLEDKŮ
if cp_ok:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    st.success("✅ Prompt zkopírován! Vložte jej do Gemini.")
    
    ai_v = st.session_state.get("ai_in", "")
    cl_v = "step-active" if not ai_v.strip() else ""
    st.markdown(f'<div class="{cl_v}">', 1)
    v = st.text_area("3. Inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', 1)

    url_v = st.session_state.get("final_url", "")
    cl_u = "step-active" if url_v.strip() else ""
    st.markdown(f'<div class="{cl_u}">', 1)
    url = st.text_input("4. URL webu (Povinné)", placeholder="https://www.web.cz", key="final_url")
    st.markdown('</div>', 1)

    if v.strip() and url.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            data = []
            for i, t in enumerate(ls):
                typ = "Nadpis" if i < 15 else "Popis"
                data.append({"Typ": typ, "Text": t, "Znaků": len(t)})
            st.session_state.d = pd.DataFrame(data)
            st.session_state.show_results = True
            st.rerun()
        st.markdown('</div>', 1)
    else:
        st.button("Vygenerovat (vyplňte pole výše)", disabled=True)

# KROK 4: VÝSTUPY S POČÍTAČEM
if st.session_state.get("show_results") and "d" in st.session_state:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    # Přidání výpočtu znaků při editaci
    df = st.session_state.d
    df["Znaků"] = df["Text"].apply(len)
    st.data_editor(df, use_container_width=True, key="ed", hide_index=True)
    
    h_l = df[df["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df[df["Typ"]=="Popis"]["Text"].tolist()
    f_u = st.session_state.get("final_url", "")

    st.subheader("👀 Náhledy")
    cols = st.columns(2)
    for i in range(4):
        with cols[i%2]:
            sh = random.sample(h_l, min(3, len(h_l))) if h_l else ["N"]
            sd = random.sample(d_l, min(2, len(d_l))) if d_l else ["P"]
            st.markdown(f"""<div style="border:1px solid #ddd;padding:10px;border-radius:8px;background:white;margin-bottom:10px;">
                <small style="color:gray;">{f_u}</small><br>
                <b style="color:blue;">{" - ".join(sh)}</b><br>{ " ".join(sd) }</div>""", 1)
    
    exp = {"Final URL": f_u}
    for i in range(1, 16): exp[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5): exp[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr: pd.DataFrame([exp]).to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL", buf.getvalue(), "ppc.xlsx")
