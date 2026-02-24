import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# NEJAGRESIVNĚJŠÍ CSS KTERÉ KDY BYLO NAPSÁNO
st.markdown("""<style>
/* 1. JEDNOTNÁ VÝŠKA PRO ÚPLNĚ VŠECHNA POLE */
textarea, input, div[data-baseweb="input"], div[data-baseweb="textarea"] {
    height: 90px !important;
    min-height: 90px !important;
    max-height: 90px !important;
}

/* 2. SROVNÁNÍ HORNÍCH SLOUPCŮ */
[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
}

/* 3. ZELENÁ NAVIGACE - BARVÍME PŘÍMO ELEMENTY BASWEBU */
.step-active div[data-baseweb="base-input"],
.step-active div[data-baseweb="textarea"],
.step-active textarea,
.step-active input {
    background-color: #e8f5e9 !important;
    border: 2px solid #28a745 !important;
}

/* 4. RESET A PÍSMO */
textarea, input {
    font-size: 16px !important;
    line-height: 1.5 !important;
    padding: 15px !important;
    resize: none !important;
}

/* 5. TLAČÍTKA A PROMPT */
div.stButton>button { width: 100%; font-weight: bold; height: 3.5em; border-radius: 8px; }
.active-btn button { background-color: #28a745 !important; color: white !important; border: none !important; }

.custom-box { 
    background:#f9f9f9; border:1px solid #ddd; padding:15px; 
    height:120px; overflow-y:scroll; font-weight: bold;
}

/* Schování defaultních Streamlit okrajů při focusu */
textarea:focus, input:focus { border-color: #28a745 !important; box-shadow: none !important; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# STAVOVÁ LOGIKA
br_v = st.session_state.get("br", "").strip()
p_ex = "p" in st.session_state
cp_ok = st.session_state.get("cp", False)

# --- KROK 1: BRIEF A USPs ---
c1, c2 = st.columns(2)
with c1:
    # Zelená pokud je prázdno
    cl1 = "step-active" if not br_v else ""
    st.markdown(f'<div class="{cl1}">', unsafe_allow_html=True)
    b = st.text_area("Vložte brief nebo obsah stránky", key="br")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    # USPs jsou volitelné, ale dáváme jim stejnou výšku
    st.text_input("USPs (volitelné)", key="usps_in")

b1_cl = "active-btn" if (br_v and not p_ex) else ""
st.markdown(f'<div class="{b1_cl}">', 1)
if st.button("Vygenerovat prompt"):
    st.session_state.p = (
        f"Jsi nejlepší PPC copywriter. Vytvoř RSA inzeráty (15 nadpisů, 4 popisky). "
        f"!!! STRIKTNĚ DODRŽUJ DÉLKY: Nadpis max 30 znaků, Popis max 90 znaků. !!! "
        f"Generuj pouze čisté texty bez číslování. "
        f"Brief: {b}. USPs: {st.session_state.usps_in}."
    )
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

# --- KROK 2: PROMPT ---
if p_ex:
    st.markdown('<div style="margin-top:15px;"></div>', 1)
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    
    b2_cl = "active-btn" if not cp_ok else ""
    st.markdown(f'<div class="{b2_cl}">', 1)
    if st.button("📋 Zkopírovat prompt"):
        st.write(f'<script>navigator.clipboard.writeText("{st.session_state.p.replace(chr(10), " ")}")</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

# --- KROK 3: VÝSLEDKY A URL ---
if cp_ok:
    ai_v = st.session_state.get("ai_in", "").strip()
    url_v = st.session_state.get("final_url", "").strip()
    
    st.markdown("---")
    
    # ZELENÁ 2: Inzeráty (dokud jsou prázdné)
    cl_v = "step-active" if not ai_v else ""
    st.markdown(f'<div class="{cl_v}">', unsafe_allow_html=True)
    v = st.text_area("Sem vložte vygenerované inzeráty z Gemini", key="ai_in")
    st.markdown('</div>', unsafe_allow_html=True)

    # ZELENÁ 3: URL (pouze pokud už máme inzeráty, ale URL chybí)
    cl_u = "step-active" if (ai_v and not url_v) else ""
    st.markdown(f'<div class="{cl_u}">', unsafe_allow_html=True)
    url = st.text_input("URL webu (Povinné)", placeholder="https://web.cz", key="final_url")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if ai_v and not url_v:
        st.warning("👈 Teď už jen vložte URL webu pro dokončení.")

    if ai_v and url_v:
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            dt = [{"Typ": "Nadpis" if i < 15 else "Popis", "Text": t} for i, t in enumerate(ls)]
            st.session_state.d = pd.DataFrame(dt)
            st.session_state.show_results = True
            st.rerun()
        st.markdown('</div>', 1)

# --- TABULKA ---
if st.session_state.get("show_results"):
    df = st.session_state.d
    df["Zbývá"] = df.apply(lambda r: (30 if r["Typ"]=="Nadpis" else 90) - len(str(r["Text"])), axis=1)
    st.data_editor(df, use_container_width=True, hide_index=True)
