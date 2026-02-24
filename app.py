import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO DYNAMICKÉ BARVY A POLA
st.markdown("""<style>
.stTextArea textarea { background-color: white !important; }
.green-field textarea { 
    background-color: #f0fff4 !important; 
    border: 2px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; }
/* TŘÍDA PRO ZELENÉ TLAČÍTKO */
.active-btn button { background-color: #28a745 !important; color: white !important; border: none !important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:10px; height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# --- 1. KROK: BRIEF A PROMPT ---
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Vložte brief nebo obsah stránky", height=100, key="br")
with c2: u = st.text_input("2. Vložte USPs (volitelné)")

p_exists = "p" in st.session_state
cp_done = st.session_state.get("cp", False)

# TLAČÍTKO 1: Zelené jen pokud prompt JEŠTĚ NEEXISTUJE a brief NENÍ PRÁZDNÝ
b1_class = "active-btn" if (st.session_state.br.strip() and not p_exists) else ""
st.markdown(f'<div class="{b1_class}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi nejlepší copywriter na PPC reklamy pro výkon a CTR. "
        f"RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {u}. "
        f"FORMÁT: Jen texty, každý na nový řádek. BEZ číslování.")
    st.session_state.cp = False # Reset kopírování při novém promptu
    st.rerun()
st.markdown('</div>', 1)

if p_exists:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    # TLAČÍTKO 2: Zelené jen pokud prompt EXISTUJE, ale JEŠTĚ SE NEKOPÍROVALO
    b2_class = "active-btn" if not cp_done else ""
    st.markdown(f'<div class="{b2_class}">', 1)
    if st.button("📋 Zkopírovat prompt do schránky"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

# --- 2. KROK: VLOŽENÍ VÝSLEDKŮ A URL ---
if cp_done:
    st.markdown("---")
    st.success("✅ Prompt zkopírován! Nyní: Běžte do Gemini a zkopírujte tam text.")
    
    # Zelené pole pro vložení (jen pokud je prázdné)
    field_class = "green-field" if not st.session_state.get("ai_in") else ""
    st.markdown(f'<div class="{field_class}">', unsafe_allow_html=True)
    v = st.text_area("3. Sem vložte vygenerované inzeráty z Gemini", key="ai_in", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

    url = st.text_input("4. URL webu (Povinné)", placeholder="https://www.priklad.cz", key="final_url")

    # FINÁLNÍ TLAČÍTKO: Zelené jen když je vše vyplněno
    if v.strip() and url.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            st.session_state.d = pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
            st.session_state.show_results = True
            st.rerun()
        st.markdown('</div>', 1)
    else:
        st.button("Vložte inzeráty a URL pro pokračování", disabled=True)

# --- 3. KROK: VÝSTUPY ---
if st.session_state.get("show_results") and "d" in st.session_state:
    st.markdown("---")
    df = st.session_state.d
    st.data_editor(df, use_container_width=True, key="ed")
    
    h_list = df[df["Typ"]=="Nadpis"]["Text"].tolist()
