import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide", page_title="PPC Studio")

# CSS PRO DYNAMICKÉ NAVÁDĚNÍ
st.markdown("""<style>
.stTextArea textarea { background-color: white !important; border-color: #d1d5db !important; }
/* ZELENÉ POLE PRO VLOŽENÍ PO KOPII */
.target-field textarea { background-color: #f0fff4 !important; border: 2px solid #28a745 !important; }
div.stButton>button { width: 100%; font-weight: bold; }
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

# Zelené "Generovat prompt", pokud je text v briefu a prompt ještě není
b1_act = "active-btn" if (st.session_state.br.strip() and not p_exists) else ""
st.markdown(f'<div class="{b1_act}">', 1)
if st.button("🚀 Vygenerovat prompt"):
    st.session_state.p = (f"Jsi nejlepší copywriter na PPC. "
        f"Napiš RSA (15 nadpisů, 4 popisky). Brief: {b}. USPs: {u}. "
        f"Jen texty, každý na nový řádek, BEZ čísel.")
    st.session_state.cp = False
    st.rerun()
st.markdown('</div>', 1)

if p_exists:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>', 1)
    # Zelené "Zkopírovat", pokud existuje prompt a ještě se nekopírovalo
    b2_act = "active-btn" if not cp_done else ""
    st.markdown(f'<div class="{b2_act}">', 1)
    if st.button("📋 Zkopírovat prompt do schránky"):
        js = f'navigator.clipboard.writeText("{st.session_state.p}")'
        st.write(f'<script>{js}</script>', unsafe_allow_html=True)
        st.session_state.cp = True
        st.rerun()
    st.markdown('</div>', 1)

st.markdown("---")

# --- KROK 2: VLOŽENÍ VÝ
