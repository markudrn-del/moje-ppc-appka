import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide")

# CSS PRO BARVY, VELIKOST PÍSMA A FIXNÍ BOX
st.markdown("""<style>
div.stButton>button { background-color: #f0f2f6; border: 1px solid #d1d5db; width: 100%; }
/* Zelené tlačítko pro kopírování (aktivuje se po generování) */
.copy-ready button { background-color: #28a745!important; color: white!important; font-weight: bold; }
/* Zvětšení písma v promptu */
.custom-box { 
    background:#f9f9f9; border:1px solid #ddd; padding:12px; height:120px; 
    overflow-y:scroll; font-family: sans-serif; font-size: 16px; line-height: 1.5;
}
.stTextArea textarea { max-height: 120px!important; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- KROK 1: BRIEF ---
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Vložte brief nebo obsah stránky", height=100)
with c2: u = st.text_input("2. Vložte USPs (volitelné)")

if st.button("🚀 Vygenerovat prompt"):
    # Fixní instrukce pro nejlepšího copywritera
    st.session_state.p = f"Jsi nejlepší copywriter na PPC reklamy, které musí zvyšovat výkon a CTR. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). Brief: {b}. USPs: {u}. FORMÁT: Vypiš pouze texty, každý na nový řádek. BEZ číslování, BEZ odrážek."
    st.rerun()

if "p" in st.session_state:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', unsafe_allow_html=True)
    
    # Obalení tlačítka do zelené třídy
    st.markdown('<div class="copy-ready">', unsafe_allow_html=True)
    if st.button("📋 Zkopírovat prompt do schránky"):
        st.write(f'<script>navigator.clipboard.writeText("{st.session_state.p}")</script>', unsafe_allow_html=True)
        st.session_state.copied = True
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get("copied"):
        st.info("💡 Otevřete Gemini a vložte do ní zkopírovaný prompt.")

st.markdown("---")

# --- KROK 2: VLOŽENÍ VÝSLEDKŮ ---
url = st.text_input("3. URL cílového webu", "https://publicis.cz")
v = st.text_area("4. Vložte texty z AI sem (bez číslování)", key="ai_in")

if v.strip():
    # Zelené tlačítko pro finální generování
    st.markdown("<style>div[data-testid='column'] + div + div div.stButton>button { background-color: #28a745!important; color: white!important; }</style>", unsafe_allow_html=True)
    if st.button("✨ Vygenerovat inzeráty a náhledy"):
        ls = [x.strip() for x in st.session_state.ai_in.split('\n') if x.strip()]
        st.session_state.d = pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
        st.rerun()
else:
    st.button("✨ Vygenerovat
