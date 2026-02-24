import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide")

st.markdown("""<style>
div.stButton>button { width: 100%; }
.copy-ready button { background:#28a745!important; color:white!important; }
.custom-box { background:#f9f9f9; border:1px solid #ddd; padding:10px; 
height:120px; overflow-y:scroll; font-size:16px; }
</style>""", unsafe_allow_html=True)

st.title("🦁 PPC Studio")

# KROK 1
c1, c2 = st.columns(2)
with c1: b = st.text_area("1. Brief nebo web", height=100)
with c2: u = st.text_input("2. USPs")

if st.button("🚀 Vygenerovat prompt"):
    txt = (f"Jsi nejlepší copywriter na PPC pro výkon a CTR. "
           f"Napiš RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {u}. "
           f"Jen texty, každý na nový řádek, BEZ čísel.")
    st.session_state.p = txt
    st.rerun()

if "p" in st.session_state:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    st.markdown('<div class="copy-ready">', 1)
    if st.button("📋 Zkopírovat"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = 1
    st.markdown('</div>', 1)
    if st.session_state.get("cp"):
        st.info("Vložte prompt do Gemini.")

st.markdown("---")

# KROK 2
url = st.text_input("3. URL webu", "https://publicis.cz")
v = st.text_area("4. Vložte texty z AI", key="ai_in")

if v.strip():
    st.markdown("<style>.stButton button { background:#28a745!important; color:white!important; }</style>", 1)
    if st.button("✨ Vygenerovat inzeráty"):
        ls = [x.strip() for x in v.split('\n') if x.strip()]
        rows = [{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)]
        st.session_state.d = pd.DataFrame(rows)
        st.rerun()
else:
    st.button("Vložte texty pro aktivaci", disabled=True)

# KROK 3
if "d" in st.session_state:
    st.markdown("---")
    st.data_editor(st.session_state.d, use_container_width=True, key="ed")
    h = st.session_state.d[st.session_state.d["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = st.session_state.d[st.session_state.d["Typ"]=="Popis"]["Text"].tolist()
    
    st.subheader("👀 Náhledy")
    cs = st.columns(2)
    for i in range(4):
        with cs[i%2]:
            sh = random.sample(h, min(3, len(h))) if h else ["N"]
            sd = random.sample(d_l, min(2, len(d_l))) if d_l else ["P"]
            st.markdown(f'<div style="border:1px solid #ddd;padding:10px;border-radius:8px;">'
                        f'<small>{url}</small><br><b style="color:blue">{" - ".join(sh)}</b>'
                        f'<br>{" ".join(sd)}</div>', 1)
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        st.session_state.d.to_excel(wr, index=False)
    st.download_button("📥 Excel", buf.getvalue(), "ppc.xlsx")
