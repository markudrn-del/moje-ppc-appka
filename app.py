import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO DYNAMICKÉ BARVY A POLA
st.markdown("""<style>
.stTextArea textarea { background-color: white !important; }
/* ZELENÉ POLE PRO VLOŽENÍ */
.green-field textarea { 
    background-color: #f0fff4 !important; 
    border: 2px solid #28a745 !important; 
}
div.stButton>button { width: 100%; font-weight: bold; }
/* AKTIVNÍ ZELENÉ TLAČÍTKO */
.active-btn button { background-color: #28a745 !important; color: white !important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:10px; height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# --- KROK 1: VSTUPY ---
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Brief nebo obsah webu", height=100, key="br")
with c2: u = st.text_input("2. USPs")

p_exists = "p" in st.session_state
cp_done = st.session_state.get("cp", False)

# Tlačítko 1: Generovat prompt
b1_style = "active-btn" if (st.session_state.br.strip() and not p_exists) else ""
st.markdown(f'<div class="{b1_style}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi nejlepší copywriter na PPC. "
        f"Napiš RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {u}. "
        f"Jen texty, každý na nový řádek, BEZ čísel.")
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

# Tlačítko 2: Zkopírovat
if p_exists:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    b2_style = "active-btn" if not cp_done else ""
    st.markdown(f'<div class="{b2_style}">', 1)
    if st.button("📋 Zkopírovat prompt do schránky"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

# --- KROK 2: VLOŽENÍ (ZOBRAZÍ SE AŽ PO KOPII) ---
if cp_done:
    st.markdown("---")
    st.success("✅ Prompt zkopírován! Nyní: **Běžte do Gemini a zkopírujte tam text.**")
    url = st.text_input("3. URL webu", "https://publicis.cz")
    
    # Zelené pole pro vložení
    st.markdown('<div class="green-field">', unsafe_allow_html=True)
    v = st.text_area("4. Sem vložte vygenerované inzeráty z Gemini", key="ai_in")
    st.markdown('</div>', unsafe_allow_html=True)

    # Tlačítko pro finální generování - objeví se až po vložení textu
    if v.strip():
        st.markdown('<div class="active-btn">', 1)
        if st.button("✨ Vygenerovat inzeráty"):
            ls = [x.strip() for x in v.split('\n') if x.strip()]
            st.session_state.d = pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
            st.rerun()
        st.markdown('</div>', 1)

# --- KROK 3: VÝSTUPY ---
if "d" in st.session_state:
    st.markdown("---")
    st.data_editor(st.session_state.d, use_container_width=True, key="ed")
    h = st.session_state.d[st.session_state.d["Typ"]=="Nadpis"]["Text"].tolist()
    dl = st.session_state.d[st.session_state.d["Typ"]=="Popis"]["Text"].tolist()
    
    st.subheader("👀 Náhledy")
    cs = st.columns(2)
    for i in range(4):
        with cs[i%2]:
            sh = random.sample(h, min(3, len(h))) if h else ["Nadpis"]
            sd = random.sample(dl, min(2, len(dl))) if dl else ["Popisek"]
