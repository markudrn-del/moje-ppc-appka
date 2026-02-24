import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO DESIGN A STŘEDOVÝ KURZOR
st.markdown("""<style>
.stTextArea textarea, .stTextInput input, 
.stTextArea textarea:focus, .stTextInput input:focus,
.stTextArea [data-baseweb="textarea"], .stTextInput [data-baseweb="input"] { 
    border-color: #d1d5db !important; 
    box-shadow: none !important; 
    background-color: white !important;
}
.stTextArea textarea { height: 100px !important; }
.stTextInput input { 
    height: 100px !important; 
    padding: 0 15px !important; 
    line-height: 100px !important;
}
.step-active textarea, .step-active input { 
    background-color: #e8f5e9 !important; 
    border: 2px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; height: 3.5em; }
.active-btn button { background-color: #28a745 !important; color: white !important; border: none !important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:12px; height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# KROK 1
c1, c2 = st.columns(2)
br_v = st.session_state.get("br", "")
p_ex = "p" in st.session_state
cp_ok = st.session_state.get("cp", False)

with c1:
    cl1 = "step-active" if (br_v.strip() and not p_ex) else ""
    st.markdown(f'<div class="{cl1}">', 1)
    b = st.text_area("1. Brief nebo web", key="br")
    st.markdown('</div>', 1)
with c2:
    u = st.text_input("2. USPs (volitelné)", key="usps_in")

b1_cl = "active-btn" if (b.strip() and not p_ex) else ""
st.markdown(f'<div class="{b1_cl}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi PPC copywriter. RSA (15 nadpisů, 4 popisky). "
                         f"Brief: {b}. USPs: {u}. Jen texty.")
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
    # Krátké texty, aby se neuřízly
    st.success("✅ Hotovo! Prompt je v paměti.")
    st.info("👇 Vložte text z Gemini do pole níže.")
    
    ai_v = st.session_state.get("ai_in", "")
    cl_v = "step-active" if not ai_v.strip() else ""
    st.markdown(f'<div class="{cl_v}">', 1)
    v = st.text_area("Vložte inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', 1)

    url_v = st.session_state.get("final_url", "")
    cl_u = "step-active" if (ai_v.strip() and not url_v.strip()) else ""
    st.markdown(f'<div class="{cl_u}">', 1)
    url = st.text_input("URL webu (Povinné)", placeholder="https://web.cz", key="final_url")
    st.markdown('</div>', 1)

    if v.strip() and url.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            dt = []
            for i, t in enumerate(ls):
                tp = "Nadpis" if i < 15 else "Popis"
                lim = 30 if tp == "Nadpis" else 90
                row = {"Typ": tp, "Text": t, "Zbývá": lim - len(str(t))}
                dt.append(row)
            st.session_state.d = pd.DataFrame(dt)
            st.session_state.show_results = True
            st.rerun()
        st.markdown('</div>', 1)
    else:
        st.button("Vygenerovat (vyplňte pole výše)", disabled=True)

# VÝSTUPY
if st.session_state.get("show_results") and "d" in st.session_state:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    df = st.session_state.d
    # Dynamický přepočet
    df["Zbývá"] = df.apply(lambda r: (30 if r["Typ"]=="Nadpis" else 90) - len(str(r["Text"])), axis=1)
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
            st.markdown(f'<div style="border:1px solid #ddd;padding:10px;border-radius:8px;background:white;margin-bottom:10px;"><small style="color:gray;">{f_u}</small><br><b style="color:blue;">{" - ".join(sh)}</b><br>{" ".join(sd)}</div>', 1)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        pd.DataFrame([{"Final URL": f_u, **{f"Headline {j+1}": (h_l[j] if j<len(h_l) else "") for j in range(15)}, **{f"Description {j+1}": (d_l[j] if j<len(d_l) else "") for j in range(4)}}]).to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL", buf.getvalue(), "ppc_export.xlsx")
