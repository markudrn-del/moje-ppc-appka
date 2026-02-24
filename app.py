import streamlit as st
import pandas as pd
import io
import random

st.set_page_config(layout="wide")

# CSS
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #28a745 !important;
        color: white !important;
    }
    .stCodeBlock, .stCodeBlock div {
        max-height: 100px !important;
    }
    .ad-preview {
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        background: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🦁 PPC Publicis Studio")

# 1. KROK
c1, c2 = st.columns(2)
with c1:
    b_txt = st.text_area("Brief", height=100)
with c2:
    u_txt = st.text_input("USPs")

if st.button("🚀 Generovat PRO prompt"):
    if b_txt:
        p_f = (
            f"Jsi copywriter. RSA. "
            f"Brief: {b_txt}. {u_txt} "
            f"FORMÁT: Jen texty, 15 nadpisů, 4 popisky."
        )
        st.session_state.current_prompt = p_f

if "current_prompt" in st.session_state:
    st.code(st.session_state.current_prompt)

st.markdown("---")

# 2. KROK
u_link = st.text_input("URL", "https://publicis.cz")
v_raw = st.text_area("Vložte texty z AI", key="ai_input")

if st.session_state.ai_input.strip():
    if st.button("✨ Vygenerovat inzeráty"):
        raw = st.session_state.ai_input
        ls = [x.strip() for x in raw.split('\n') if x.strip()]
        rows = []
        for i, t in enumerate(ls):
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(t)})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()

# 3. KROK
if "df_data" in st.session_state:
    st.markdown("---")
    st.data_editor(
        st.session_state.df_data,
        key="ppc_editor"
    )

    st.subheader("👀 Náhledy")
    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"]=="Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"]=="Popis"]["Text"].tolist()

    if len(h_l) >= 2:
        cols = st.columns(2)
        for i in range(6):
            with cols[i % 2]:
                # BEZPEČNÉ SAMPLOVÁNÍ NA VÍCE ŘÁDCÍCH
                cnt_h = len(h_l)
                n_h = min(3, cnt_h)
                sh = random.sample(h_l, n_h)
                
                cnt_d = len(d_l)
                n_d = min(2, cnt_d)
                sd = random.sample(d_l, n_d) if d_l else [""]
                
                h_s = " – ".join(sh)
                d_s = " ".join(sd)
                
                st.markdown(
                    f'<div class="ad-preview">'
                    f'<div style="color:gray;">{u_link}</div>'
                    f'<div style="color:blue;">{h_s}</div>'
                    f'<div>{d_s}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown("---")
    # Export
    out = {"Campaign": "C1", "URL": u_link}
    for i in range(1, 16):
        out[f"Headline {i}"] = h_l[i-1] if i-1 < len(h_l) else ""
    for i in range(1, 5):
        out[f"Description {i}"] = d_l[i-1] if i-1 < len(d_l) else ""
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        pd.DataFrame([out]).to_excel(wr, index=False)
    st.download_button("📥 Excel", buf.getvalue(), "ppc.xlsx")
