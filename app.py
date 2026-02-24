import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO DOKONALÝ DESIGN A STŘEDOVÝ KURZOR
st.markdown("""<style>
/* 1. ZÁKAZ ČERVENÉ A STÍNŮ VŠUDE */
.stTextArea textarea, .stTextInput input, 
.stTextArea textarea:focus, .stTextInput input:focus,
.stTextArea [data-baseweb="textarea"], .stTextInput [data-baseweb="input"] { 
    border-color: #d1d5db !important; 
    box-shadow: none !important; 
    background-color: white !important;
}

/* 2. SROVNÁNÍ POLÍ A KURZOR NA STŘED */
.stTextArea textarea { height: 100px !important; }
.stTextInput input { 
    height: 100px !important; 
    padding: 0 15px !important; 
    display: flex !important;
    align-items: center !important;
}

/* 3. ZELENÁ NAVIGACE (AKTIVNÍ KROK) */
.step-active textarea, .step-active input { 
    background-color: #e8f5e9 !important; 
    border: 2px solid #28a745 !important; 
}

/* 4. TLAČÍTKA */
div.stButton>button { width: 100%; font-weight: bold; height: 3.5em; }
.active-btn button { background-color: #28a745 !important; color: white !important; border: none !important; }

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
    b = st.text_area("1. Brief nebo web", key="br")
    st.markdown('</div>', 1)
with c2:
    u = st.text_input("2. USPs (volitelné)", key="usps_in")

# Tlačítko 1
b1_cl = "active-btn" if (b.strip() and not p_ex) else ""
st.markdown(f'<div class="{b1_cl}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi PPC copywriter. RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). "
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
    st.success("✅ Prompt zkopírován!")
    st.info("👇 **Nyní vložte inzeráty vygenerované v Gemini do zeleného pole níže.**")
    
    ai_v = st.session_state.get("ai_in", "")
    # Pole pro inzeráty zezelená po kopii promptu, dokud se nevyplní
    cl_v = "step-active" if not ai_v.strip() else ""
    st.markdown(f'<div class="{cl_v}">', 1)
    v = st.text_area("Sem vložte vygenerované inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', 1)

    url_v = st.session_state.get("final_url", "")
    # URL pole zezelená, když už jsou vložené inzeráty, ale chybí URL
    cl_u = "step-active" if (ai_v.strip() and not url_v.strip()) else ""
    st.markdown(f'<div class="{cl_u}">', 1)
    url = st.text_input("URL webu (Povinné)", placeholder="https://www.web.cz", key="final_url")
    st.markdown('</div>', 1)

    if v.strip() and url.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            data = []
            for i, t in enumerate(ls):
                typ = "Nadpis" if i < 15 else "Popis"
                limit = 30 if typ == "Nadpis" else 90
                data.append({"Typ": typ, "Text": t, "Zbývá": limit -
