import streamlit as st, pandas as pd, io, random
st.set_page_config(layout="wide")
st.markdown("<style>div.stButton>button{background-color:#28a745!important;color:white!important;}.stTextArea textarea{max-height:150px!important;}.custom-box{background:#f0f2f6;border:1px solid #ddd;padding:10px;height:100px;overflow-y:scroll;font-family:monospace;}</style>",unsafe_allow_html=True)
st.title("🦁 PPC Publicis Studio")
c1,c2=st.columns(2)
with c1: b=st.text_area("Brief",height=100)
with c2: u=st.text_input("USPs")
if st.button("🚀 Generovat prompt"):
    st.session_state.p=f"RSA. Brief: {b}. USPs: {u}. Jen texty, 15 nadpisů, 4 popisky."
if "p" in st.session_state:
    st.markdown(f'<div class="custom-box">{st.session_state.p}</div>',unsafe_allow_html=True)
st.markdown("---")
url=st.text_input("URL","https://publicis.cz")
v=st.text_area("Krok 2: Vložit texty",key="ai_in")
if st.button("✨ Vygenerovat") and st.session_state.ai_in.strip():
    ls=[x.strip() for x in st.session_state.ai_in.split('\n') if x.strip()]
    st.session_state.d=pd.DataFrame([{"Typ":"Nadpis" if i<15 else "Popis","Text":t} for i,t in enumerate(ls)])
    st.rerun()
if "d" in st.session_state:
    st.data_editor(st.session_state.d,key="ed")
    h=st.session_state.d[st.session_state.d["Typ"]=="Nadpis"]["Text"].tolist()
    d=st.session_state.d[st.session_state.d["Typ"]=="Popis"]["Text"].tolist()
    st.subheader("👀 Náhledy")
    cs=st.columns(2)
    for i in range(4):
        with cs[i%2]:
            sh=random.sample(h,min(3,len(h))) if len(h)>0 else ["Nadpis"]
            sd=random.sample(d,min(2,len(d))) if len(d)>0 else ["Popis"]
            st.markdown(f'<div style="border:1px solid #ddd;padding:10px;margin-bottom:5px"><b>{" - ".join(sh)}</b><br>{ " ".join(sd)}</div>',unsafe_allow_html=True)
    buf=io.BytesIO()
    with pd.ExcelWriter(buf) as wr:
        st.session_state.d.to_excel(wr,index=False)
    st.download_button("📥 Excel",buf.getvalue(),"ppc.xlsx")
