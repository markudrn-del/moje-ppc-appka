import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO ODSTRANĚNÍ ČERVENÉ A UX NAVIGACI
st.markdown("""<style>
/* ABSOLUTNÍ ZÁKAZ ČERVENÉ BARVY A STÍNŮ PŘI FOCUSU */
.stTextArea textarea, .stTextInput input, 
.stTextArea textarea:focus, .stTextInput input:focus { 
    background-color: white !important; 
    color: black !important;
    border-color: #d1d5db !important;
    box-shadow: none !important;
    outline: none !important;
}
/* Zelené podbarvení polí, pokud jsou vyplněná a aktivní */
.brief-active textarea, .brief-active input { 
    background-color: #f0fff4 !important; 
    border: 1px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; height: 3em; }
/* AKTIVNÍ ZELENÉ TLAČÍTKO */
.active-btn button { 
    background-color: #28a745 !important; 
    color: white !important; 
    border: none !important; 
}
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:12px; height:120px; overflow-y:scroll; font-size:16px; margin-bottom:15px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# --- KROK 1: BRIEF ---
c1, c2 = st.columns(2)
brief_text = st.session_state.get("br", "")
p_exists = "p" in st.session_state
cp_done = st.session_state.get("cp", False)

with c1:
    # Pole briefu zezelená jen pokud je v něm text a ještě se nevygeneroval prompt
    b_class = "brief-active" if (brief_text.strip() and not p_exists) else ""
    st.markdown(f'<div class="{b_class}">', unsafe_allow_html=True)
    b = st.text_area("1. Vložte brief nebo obsah stránky", height=100, key="br")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.text_input("2. Vložte USPs (volitelné)", key="usps_in")

# Tlačítko 1: Generovat
b1_class = "active-btn" if (b.strip() and not p_exists) else ""
st.markdown(f'<div class="{b1_class}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi nejlepší copywriter na PPC reklamy pro výkon a CTR. "
        f"RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {st.session_state.usps_in}. "
        f"FORMÁT: Jen texty, každý na nový řádek. BEZ číslování.")
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

# --- KROK 2: PROMPT A KOPIE ---
if p_exists:
    st.markdown('<div style="margin-top:20px;"></div>', 1)
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    
    b2_class = "active-btn" if not cp_done else ""
    st.markdown(f'<div class="{b2_class}">', 1)
    if st.button("📋 Zkopírovat prompt do schránky"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

# --- KROK 3: VLOŽENÍ VÝSLEDKŮ ---
if cp_done:
    st.markdown('<div style="margin-top:30px;"></div>', 1)
    st.success("✅ Prompt zkopírován! Nyní: Běžte do Gemini a zkopírujte tam text.")
    
    # Zelené pole pro inzeráty
    v_text = st.session_state.get("ai_in", "")
    v_class = "brief-active" if not v_text.strip() else ""
    st.markdown(f'<div class="{v_class}">', unsafe_allow_html=True)
    v = st.text_area("3. Sem vložte vygenerované inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

    # URL pole - odstraněna červená barva při kliku
    url_val = st.session_state.get("final_url", "")
    url_class = "brief-active" if url_val.strip() else ""
    st.markdown(f'<div class="{url_class}">', unsafe_allow_html=True)
    url = st.text_input("4. URL
