import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide")

st.markdown("""<style>
/* Reset červené barvy a základ tlačítek */
.stTextArea textarea { background-color: white !important; }
div.stButton>button { width: 100%; font-weight: bold; }
/* Zelená pro aktivní akci */
.active-btn button { background:#28a745!important; color:white!important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:10px; 
height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# --- KROK 1 ---
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Brief nebo obsah webu", height=100, key="br")
with c2: u = st.text_input("2. USPs")

# Logika barev pro první dvě tlačítka
p_ready = "p" in st.session_state
c1_class = "" if p_ready else "active-btn"
c2_class = "active-btn" if p_ready else ""

st.markdown(f'<div class="{c1_class}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi nejlepší copywriter na PPC. "
        f"Napiš RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {u}. "
        f"Jen texty, každý na nový řádek, BEZ čísel.")
    st.session_state.cp = False # Reset kopírování
    st.rerun()
st.markdown('</div>', 1)

if p_ready:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    st.markdown(f'<div class="{c2_class}">', 1)
    if st.button("📋 Zkopírovat prompt do schránky"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
    st.markdown('</div>', 1)
    if st.session_state.get("cp"):
        st.success("✅ Zkopírováno! Nyní tento prompt vložte do Gemini.")

st.markdown("---")

# --- KROK 2 ---
url = st.text_input("3. URL webu", "https://publicis.cz")
v = st.text_area("4. Vložte texty z AI sem", key="ai_in")

if v.strip():
    st.markdown("<style>div[data-testid='stVerticalBlock'] div.stButton>button { background:#28a745!important; color:white!important; }</style>", 1)
    if st.button("✨ Vygenerovat inzeráty"):
        ls = [x.strip() for x in v.split('\n') if x.strip()]
        rows = [{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)]
        st.session_state.d = pd.DataFrame(rows)
        st.rerun()
else:
    st.button("Vložte texty (Krok 4)", disabled=True)

# --- KROK 3 ---
if "d" in st.session_state:
    st.markdown("---")
    st.data_editor(st.session_state.d, use_container_width=True, key="ed")
    h = st.session_state.d[st.session_state.d["Typ"]=="Nadpis"]["Text"].tolist()
    dl = st.session_state.d[st.session_state.d["Typ"]=="Popis"]["Text"].tolist()
    
    st.subheader("👀 Náhledy")
    cs = st.columns(2)
    for i in range(4):
        with cs[i%2]:
            sh = random.sample(h, min(3, len(h))) if h else ["N"]
            sd = random.sample(dl, min(2, len(dl))) if dl else ["P"]
            st.markdown(f'<div style="border:1px solid #ddd;padding:10px;border-radius:8px;background:white;">'
                f'<small>{url}</small><br><b style="color:blue">{" - ".join(sh)}</b>'
                f'<br>{" ".join(sd)}</div>', 1)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        st.session_state.d.to_excel(wr, index=False)
    st.download_button("📥 Excel", buf.getvalue(), "ppc.xlsx")
