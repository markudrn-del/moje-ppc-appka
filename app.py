import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO UX A ZÁKAZ ČERVENÉ
st.markdown("""<style>
.stTextArea textarea, .stTextInput input, 
.stTextArea textarea:focus, .stTextInput input:focus { 
    background-color: white !important; color: black !important;
    border-color: #d1d5db !important; box-shadow: none !important;
}
.br-active textarea, .br-active input { 
    background-color: #f0fff4 !important; border: 1px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; height: 3em; }
.active-btn button { background-color: #28a745 !important; color: white !important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:12px; height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# KROK 1
c1, c2 = st.columns(2)
br_val = st.session_state.get("br", "")
p_ex = "p" in st.session_state
cp_ok = st.session_state.get("cp", False)

with c1:
    # Zelené pole jen při zadávání
    cl1 = "br-active" if (br_val.strip() and not p_ex) else ""
    st.markdown(f'<div class="{cl1}">', 1)
    b = st.text_area("1. Brief nebo web", height=100, key="br")
    st.markdown('</div>', 1)
with c2:
    u = st.text_input("2. USPs (volitelné)", key="usps_in")

# Tlačítko 1
b1_cl = "active-btn" if (b.strip() and not p_ex) else ""
st.markdown(f'<div class="{b1_cl}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    prompt_txt = (f"Jsi nejlepší copywriter na PPC reklamy. "
                 f"RSA (15 nadpisů, 4 popisky). Brief: {b}. "
                 f"USPs: {st.session_state.usps_in}. "
                 f"Jen texty, každý na nový řádek.")
    st.session_state.p = prompt_txt
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

# KROK 2
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

# KROK 3
if cp_ok:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    st.success("✅ Prompt zkopírován! Vložte jej do Gemini.")
    
    ai_val = st.session_state.get("ai_in", "")
    cl_v = "br-active" if not ai_val.strip() else ""
    st.markdown(f'<div class="{cl_v}">', 1)
    v = st.text_area("3. Inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', 1)

    url_val = st.session_state.get("final_url", "")
    cl_u = "br-active" if url_val.strip() else ""
    st.markdown(f'<div class="{cl_u}">', 1)
    # Rozdělený řádek, aby ho editor neuřízl
    url = st.text_input("4. URL webu (Povinné)", 
                       placeholder="https://www.web.cz", 
                       key="final_url")
    st.markdown('</div>', 1)

    if v.strip() and url.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            st.session_state.d = pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
            st.session_state.show_results = True
            st.rerun()
        st.markdown('</div>', 1)
    else:
        st.button("Vygenerovat (vyplňte pole výše)", disabled=True)

# VÝSTUPY
if st.session_state.get("show_results") and "d" in st.session_state:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    df = st.session_state.d
    st.data_editor(df, use_container_width=True, key="ed")
    
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
                <b style="color:blue;">{" - ".join(sh)}</b><br>
                { " ".join(sd) }</div>""", 1)
    
    exp = {"Final URL": f_u}
    for i in range(1, 16): exp[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5): exp[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr: pd.DataFrame([exp]).to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL", buf.getvalue(), "ppc.xlsx")
