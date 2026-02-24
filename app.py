import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide")
# KOMPAKTNÍ CSS PRO BARVY A VELIKOSTI
st.markdown("""<style>
/* Základní barva tlačítek (šedá) */
div.stButton>button { background-color: #f0f2f6; border: 1px solid #d1d5db; color: #31333F; }
/* Zelená barva pro aktivní kroky */
.st-emotion-cache-19rxjzo.e1nzilvr4 { background-color: #28a745!important; color: white!important; }
.stTextArea textarea { max-height: 120px!important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:10px; height:100px; overflow-y:scroll; font-family:monospace; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Publicis Studio")

# --- KROK 1: BRIEF ---
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Vložte Brief", height=100)
with c2: u = st.text_input("2. Vložte USPs (volitelné)")

# Logika pro "zašednutí" tlačítka generovat
p_exists = "p" in st.session_state
gen_label = "✅ Prompt vygenerován" if p_exists else "🚀 Generovat prompt"

if st.button(gen_label):
    st.session_state.p = f"Jsi copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). Brief: {b}. USPs: {u}. FORMÁT: Vypiš pouze texty, každý na nový řádek. BEZ číslování, BEZ odrážek, BEZ uvozovek."
    st.rerun()

if p_exists:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', unsafe_allow_html=True)
    if st.button("📋 Zkopírovat prompt do schránky"):
        st.write(f'<script>navigator.clipboard.writeText("{st.session_state.p}")</script>', unsafe_allow_html=True)
        st.success("Zkopírováno!")

st.markdown("---")

# --- KROK 2: VLOŽENÍ VÝSLEDKŮ ---
url = st.text_input("3. URL cílového webu", "https://publicis.cz")
v = st.text_area("4. Vložte texty z Gemini sem", key="ai_in")

# DYNAMICKÁ BARVA TLAČÍTKA PŘES CSS
if v.strip():
    st.markdown("<style>div[data-testid='stVerticalBlock'] div:nth-child(8) button { background-color: #28a745!important; color: white!important; }</style>", unsafe_allow_html=True)
    if st.button("✨ Vygenerovat inzeráty a náhledy"):
        ls = [x.strip() for x in st.session_state.ai_in.split('\n') if x.strip()]
        st.session_state.d = pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
        st.rerun()
else:
    st.button("✨ Vygenerovat (vložte texty)", disabled=True)

# --- KROK 3: VÝSTUPY ---
if "d" in st.session_state:
    st.markdown("---")
    st.data_editor(st.session_state.d, use_container_width=True, key="ed")
    h = st.session_state.d[st.session_state.d["Typ"]=="Nadpis"]["Text"].tolist()
    d = st.session_state.d[st.session_state.d["Typ"]=="Popis"]["Text"].tolist()
    
    st.subheader("👀 Náhledy")
    cs = st.columns(2)
    for i in range(4):
        with cs[i%2]:
            sh = random.sample(h, min(3, len(h))) if h else ["Nadpis"]
            sd = random.sample(d, min(2, len(d))) if d else ["Popis"]
            st.markdown(f'<div style="border:1px solid #ddd;padding:12px;border-radius:8px;background:white;margin-bottom:10px;"><small style="color:gray;">{url}</small><br><b style="color:#1a0dab;font-size:1.1em;">{" - ".join(sh)}</b><br><span style="color:#4d5156;">{ " ".join(sd)}</span></div>', unsafe_allow_html=True)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        st.session_state.d.to_excel(wr, index=False)
    st.download_button("📥 Stáhnout EXCEL pro Google Editor", buf.getvalue(), "ppc_final.xlsx")
