import streamlit as st
import pandas as pd
import io, random

st.set_page_config(layout="wide", page_title="PPC Studio", page_icon="🦁")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Figtree', -apple-system, BlinkMacSystemFont, sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 4rem 5rem;
    max-width: 1100px;
}

/* ── Background — soft warm white like macOS */
.stApp {
    background: #f5f5f7;
    color: #1d1d1f;
}

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
.ap-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 3rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0,0,0,0.08);
}
.ap-wordmark {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #1d1d1f;
}
.ap-wordmark span { color: #0071e3; }
.ap-pill {
    background: rgba(0,113,227,0.08);
    color: #0071e3;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 100px;
}

/* ══════════════════════════════════════
   INPUTS — Apple-style text fields
══════════════════════════════════════ */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(0,0,0,0.12) !important;
    border-radius: 12px !important;
    color: #1d1d1f !important;
    font-family: 'Figtree', -apple-system, sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    padding: 0.6rem 0.85rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.15), 0 1px 3px rgba(0,0,0,0.04) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label {
    color: #6e6e73 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 6px !important;
}

/* ══════════════════════════════════════
   BUTTONS
══════════════════════════════════════ */
.stButton button {
    background: #0071e3 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 980px !important;
    padding: 0.55rem 1.5rem !important;
    font-family: 'Figtree', -apple-system, sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: -0.01em !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(0,113,227,0.3) !important;
    transition: background 0.15s, transform 0.1s, box-shadow 0.15s !important;
}
.stButton button:hover {
    background: #0077ed !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,113,227,0.35) !important;
}
.stButton button:active {
    transform: translateY(0) !important;
    background: #006bda !important;
}

/* Download — secondary style */
.stDownloadButton button {
    background: rgba(0,0,0,0.05) !important;
    color: #1d1d1f !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    border-radius: 980px !important;
    font-family: 'Figtree', -apple-system, sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: none !important;
}
.stDownloadButton button:hover {
    background: rgba(0,0,0,0.09) !important;
    transform: translateY(-1px) !important;
}

/* ══════════════════════════════════════
   CODE BLOCK
══════════════════════════════════════ */
.stCodeBlock {
    border-radius: 14px !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    overflow: hidden;
}
.stCodeBlock code {
    font-size: 0.82rem !important;
}

/* ══════════════════════════════════════
   DATA EDITOR
══════════════════════════════════════ */
[data-testid="stDataFrameResizable"] {
    border-radius: 14px !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}

/* ══════════════════════════════════════
   AD PREVIEW CARDS
══════════════════════════════════════ */
.ad-wrap {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 12px;
    font-family: Arial, sans-serif;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.2s;
}
.ad-wrap:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}
.ad-top {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 5px;
}
.ad-favicon {
    width: 16px;
    height: 16px;
    background: #34a853;
    border-radius: 4px;
    flex-shrink: 0;
}
.ad-url { font-size: 12px; color: #202124; }
.ad-sponsored { font-size: 11px; color: #70757a; margin-left: auto; }
.ad-headline {
    color: #1a0dab;
    font-size: 17px;
    font-weight: 400;
    line-height: 1.3;
    margin-bottom: 5px;
}
.ad-desc { color: #4d5156; font-size: 13px; line-height: 1.5; }

/* ══════════════════════════════════════
   STEP INDICATOR
══════════════════════════════════════ */
.ap-step-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.2rem;
}
.ap-step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #0071e3;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.ap-step-label {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #1d1d1f;
}

/* Divider */
.ap-divider {
    border: none;
    border-top: 1px solid rgba(0,0,0,0.07);
    margin: 2.5rem 0;
}

/* Warnings */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
}

h1,h2,h3,h4 {
    font-family: 'Figtree', -apple-system, sans-serif !important;
    letter-spacing: -0.02em !important;
}
</style>
""", unsafe_allow_html=True)


# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ap-header">
    <div class="ap-wordmark">🦁 PPC <span>Studio</span></div>
    <div class="ap-pill">Publicis</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# KROK 1 — Brief & prompt
# ═══════════════════════════════════════════════════
st.markdown("""
<div class="ap-step-row">
    <div class="ap-step-num">1</div>
    <div class="ap-step-label">Brief &amp; prompt generátor</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2], gap="large")
with c1:
    b_txt = st.text_area("Brief kampaně", height=115, placeholder="Popiš produkt, cílovou skupinu, cíle kampaně…")
with c2:
    u_txt = st.text_input("Vlastní USPs", placeholder="Rychlá doprava, česká výroba…")
    st.write("")
    gen_btn = st.button("Generovat PRO prompt  →")

if gen_btn:
    if b_txt:
        u_p = f" USPs: {u_txt}." if u_txt else ""
        p_f = f"Jsi senior copywriter. Napiš RSA (15 nadpisů do 30 zn, 4 popisky do 90 zn). CTR. Brief: {b_txt}.{u_p}"
        st.code(p_f, language="text")
    else:
        st.warning("Nejdřív vyplň brief.")

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# KROK 2 — Editor textů
# ═══════════════════════════════════════════════════
st.markdown("""
<div class="ap-step-row">
    <div class="ap-step-num">2</div>
    <div class="ap-step-label">Editor textů</div>
</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([2, 3], gap="large")
with col_a:
    u_link = st.text_input("URL webu", "https://publicis.cz")
with col_b:
    v_raw = st.text_area("AI texty vložte sem", height=120,
                         placeholder="Vložte nadpisy a popisky — každý na nový řádek…")

load_btn = st.button("Načíst do tabulky  →")


def prepocet():
    if "ppc_editor" in st.session_state and "df_data" in st.session_state:
        df = st.session_state.df_data
        ed = st.session_state["ppc_editor"]
        for r, h in ed.get("edited_rows", {}).items():
            for c, v in h.items():
                df.at[int(r), c] = v
        df["Zbyva"] = df.apply(
            lambda x: (30 if x["Typ"] == "Nadpis" else 90) - len(str(x["Text"])), axis=1
        )
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

    st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # KROK 3 — Náhledy
    # ═══════════════════════════════════════════════════
    st.markdown("""
    <div class="ap-step-row">
        <div class="ap-step-num">3</div>
        <div class="ap-step-label">Náhledy inzerátů</div>
    </div>
    """, unsafe_allow_html=True)

    df_f = st.session_state.df_data
    h_l = df_f[df_f["Typ"] == "Nadpis"]["Text"].tolist()
    d_l = df_f[df_f["Typ"] == "Popis"]["Text"].tolist()
    domain = u_link.replace("https://", "").replace("http://", "").rstrip("/")

    if len(h_l) > 2 and len(d_l) > 1:
        cols = st.columns(2, gap="medium")
        for i in range(6):
            with cols[i % 2]:
                sh = random.sample(h_l, 3) if len(h_l) >= 3 else h_l
                sd = random.sample(d_l, 2) if len(d_l) >= 2 else d_l
                h3 = sh[2] if len(sh) > 2 else ""
                d2 = sd[1] if len(sd) > 1 else ""
                headline = f"{sh[0]} – {sh[1]}" + (f" – {h3}" if h3 else "")
                st.markdown(f"""
                <div class="ad-wrap">
                    <div class="ad-top">
                        <div class="ad-favicon"></div>
                        <div class="ad-url">{domain}</div>
                        <div class="ad-sponsored">Sponzorováno</div>
                    </div>
                    <div class="ad-headline">{headline}</div>
                    <div class="ad-desc">{sd[0]} {d2}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Pro náhledy potřebuješ alespoň 3 nadpisy a 2 popisky.")

    st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # KROK 4 — Export
    # ═══════════════════════════════════════════════════
    st.markdown("""
    <div class="ap-step-row">
        <div class="ap-step-num">4</div>
        <div class="ap-step-label">Export pro Google Ads Editor</div>
    </div>
    """, unsafe_allow_html=True)

    out = {"Campaign": "Kampaň 1", "Ad Group": "Sestava 1", "Final URL": u_link}
    for i in range(1, 16):
        out[f"Headline {i}"] = h_l[i - 1] if i - 1 < len(h_l) else ""
    for i in range(1, 5):
        out[f"Description {i}"] = d_l[i - 1] if i - 1 < len(d_l) else ""

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        pd.DataFrame([out]).to_excel(wr, index=False)

    st.download_button(
        label="Stáhnout XLSX  ↓",
        data=buf.getvalue(),
        file_name="ppc_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
