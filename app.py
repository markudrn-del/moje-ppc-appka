import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio", page_icon="🦁")

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Background */
.stApp {
    background: #0d0e14;
    color: #e8e9f0;
}

/* ── Header */
.pp-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.pp-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ff6b35 0%, #f7c59f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.pp-badge {
    background: rgba(255,107,53,0.12);
    border: 1px solid rgba(255,107,53,0.25);
    color: #ff8c5a;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 100px;
}

/* ── Step label */
.pp-step {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ff6b35;
    margin-bottom: 0.5rem;
}
.pp-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e9f0;
    margin-bottom: 1.2rem;
}

/* ── Card */
.pp-card {
    background: #16181f;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* ── Divider */
.pp-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2rem 0;
}

/* ── Text inputs */
.stTextInput input, .stTextArea textarea {
    background: #1e2029 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8e9f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(255,107,53,0.4) !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.08) !important;
}

/* Labels */
.stTextInput label, .stTextArea label {
    color: #9294a0 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
}

/* ── Buttons */
.stButton button {
    background: linear-gradient(135deg, #ff6b35, #ff4500) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s;
}
.stButton button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px);
}

/* Download button */
.stDownloadButton button {
    background: #1e2029 !important;
    color: #e8e9f0 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
.stDownloadButton button:hover {
    border-color: rgba(255,107,53,0.4) !important;
    color: #ff8c5a !important;
}

/* ── Code block */
.stCodeBlock {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Data editor */
.stDataEditor {
    border-radius: 12px !important;
    overflow: hidden;
}
[data-testid="stDataFrameResizable"] {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Ad preview card */
.ad-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.ad-card:hover { transform: translateY(-2px); }
.ad-sponsored {
    font-size: 11px;
    color: #70757a;
    margin-bottom: 3px;
}
.ad-headline {
    color: #1a0dab;
    font-size: 17px;
    font-weight: 400;
    line-height: 1.3;
    margin-bottom: 5px;
}
.ad-desc {
    color: #4d5156;
    font-size: 13px;
    line-height: 1.45;
}

/* subheader override */
h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #e8e9f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pp-header">
    <div class="pp-logo">🦁 PPC Studio</div>
    <div class="pp-badge">Publicis</div>
</div>
""", unsafe_allow_html=True)

# ─── KROK 1: VSTUPY ───────────────────────────────────────────────────────────
st.markdown('<div class="pp-step">Krok 1</div>', unsafe_allow_html=True)
st.markdown('<div class="pp-section-title">Brief & prompt generátor</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3, 2], gap="large")
with c1:
    b_txt = st.text_area("Brief kampaně", height=110, placeholder="Popiš produkt, cílovou skupinu, cíle…")
with c2:
    u_txt = st.text_input("Vlastní USPs", placeholder="Rychlá doprava, česká výroba…")
    st.write("")
    gen_btn = st.button("🚀  Generovat PRO prompt")

if gen_btn:
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = f"Jsi senior copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). CTR. Brief: {b_txt}.{u_p}"
        st.code(p_f, language="text")
    else:
        st.warning("Nejdřív vyplň brief.")

st.markdown('<hr class="pp-divider">', unsafe_allow_html=True)

# ─── KROK 2: EDITOR ───────────────────────────────────────────────────────────
st.markdown('<div class="pp-step">Krok 2</div>', unsafe_allow_html=True)
st.markdown('<div class="pp-section-title">Editor textů</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([2, 3], gap="large")
with col_a:
    u_link = st.text_input("URL webu", "https://publicis.cz")

with col_b:
    v_raw = st.text_area("AI texty vložte sem", height=130, placeholder="Vložte nadpisy a popisky – každý na nový řádek…")

load_btn = st.button("✅  Načíst do tabulky")

def prepocet():
    if "ppc_editor" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1)
        st.session_state.df_data = df

if load_btn:
    if v_raw.strip():
        ls = [x.strip() for x in v_raw.split('\n') if x.strip()]
        rows = []
        for i in range(len(ls)):
            t = ls[i]
            tp = "Nadpis" if i < 15 else "Popis"
            lim = 30 if tp == "Nadpis" else 90
            rows.append({"Typ": tp, "Text": t, "Zbyva": lim - len(str(t))})
        st.session_state.df_data = pd.DataFrame(rows)
        st.rerun()
    else:
        st.warning("Vložte texty do pole výše.")

if "df_data" in st.session_state:
    st.data_editor(
        st.session_state.df_data,
        use_container_width=True,
        hide_index=True,
        key="ppc_editor",
        on_change=prepocet,
        column_config={
            "Typ":   st.column_config.TextColumn("Typ", width="small"),
            "Text":  st.column_config.TextColumn("Text", width="large"),
            "Zbyva": st.column_config.NumberColumn("Zbývá znaků", width="small"),
        }
    )

    st.markdown('<hr class="pp-divider">', unsafe_allow_html=True)

    # ─── KROK 3: NÁHLEDY ──────────────────────────────────────────────────────
    st.markdown('<div class="pp-step">Krok 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="pp-section-title">Náhledy inzerátů — 6 kombinací</div>', unsafe_allow_html=True)

    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()

    if len(h_l) > 2 and len(d_l) > 1:
        cols = st.columns(2, gap="medium")
        domain = u_link.replace("https://", "").replace("http://", "")
        for i in range(6):
            with cols[i % 2]:
                sh = random.sample(h_l, 3) if len(h_l) >= 3 else h_l
                sd = random.sample(d_l, 2) if len(d_l) >= 2 else d_l
                h3 = sh[2] if len(sh) > 2 else ""
                d2 = sd[1] if len(sd) > 1 else ""
                st.markdown(f"""
                <div class="ad-card">
                    <div class="ad-sponsored">Sponzorováno &nbsp;·&nbsp; {domain}</div>
                    <div class="ad-headline">{sh[0]} – {sh[1]}{' – ' + h3 if h3 else ''}</div>
                    <div class="ad-desc">{sd[0]} {d2}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Pro náhledy potřebuješ alespoň 3 nadpisy a 2 popisky.")

    st.markdown('<hr class="pp-divider">', unsafe_allow_html=True)

    # ─── KROK 4: EXPORT ───────────────────────────────────────────────────────
    st.markdown('<div class="pp-step">Krok 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="pp-section-title">Export pro Google Ads Editor</div>', unsafe_allow_html=True)

    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(1, 16):
        out[f"Headline {i}"] = h_l[i - 1] if i - 1 < len(h_l) else ""
    for i in range(1, 5):
        out[f"Description {i}"] = d_l[i - 1] if i - 1 < len(d_l) else ""

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        pd.DataFrame([out]).to_excel(wr, index=False)

    st.download_button(
        label="📥  Stáhnout XLSX pro Google Ads Editor",
        data=buf.getvalue(),
        file_name="ppc_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
