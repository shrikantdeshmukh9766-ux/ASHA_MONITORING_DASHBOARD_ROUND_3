import streamlit as st
from koboextractor import KoboExtractor
import pandas as pd
import io

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="आशा मॉनिटरिंग डॅशबोर्ड",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# CUSTOM CSS  — Light Blue Theme, Faint Month Colors
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif;
}

/* ── App Background — soft light blue ── */
.stApp {
    background: #eaf4fb;
    min-height: 100vh;
}

/* subtle dot-grid texture */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, #b8d9f0 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}

/* ── Block container ── */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    position: relative;
    z-index: 1;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1b4f72 0%, #1a6fa6 50%, #2e86c1 100%);
    border-radius: 22px;
    padding: 34px 40px;
    margin-bottom: 26px;
    box-shadow: 0 8px 32px rgba(27,79,114,0.18), inset 0 1px 0 rgba(255,255,255,0.12);
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '🌸';
    position: absolute;
    right: 44px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 72px;
    opacity: 0.12;
}

.hero-banner::after {
    content: '';
    position: absolute;
    top: -60%;
    left: -10%;
    width: 50%;
    height: 220%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
    transform: rotate(12deg);
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 7px 0;
    line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.18);
}

.hero-subtitle {
    color: rgba(255,255,255,0.72);
    font-size: 13.5px;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.4px;
}

/* ── Metric Cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 26px;
}

.metric-card {
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(27,79,114,0.10);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid rgba(255,255,255,0.7);
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(27,79,114,0.15);
}

/* soft pastel card tones */
.metric-card-1 { background: linear-gradient(135deg, #dbeeff, #c2dcf7); }
.metric-card-2 { background: linear-gradient(135deg, #dff5ec, #c2ead8); }
.metric-card-3 { background: linear-gradient(135deg, #e8e4ff, #d3ccf9); }
.metric-card-4 { background: linear-gradient(135deg, #fef3dc, #fde5b4); }

.metric-card::after {
    content: '';
    position: absolute;
    top: -20%;
    right: -8%;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: rgba(255,255,255,0.35);
}

.metric-icon  { font-size: 26px; margin-bottom: 9px; display: block; }

.metric-value-1 { font-size: 32px; font-weight: 800; color: #1a6fa6; line-height:1; margin-bottom:3px; }
.metric-value-2 { font-size: 32px; font-weight: 800; color: #1a8a5a; line-height:1; margin-bottom:3px; }
.metric-value-3 { font-size: 32px; font-weight: 800; color: #5a44cc; line-height:1; margin-bottom:3px; }
.metric-value-4 { font-size: 32px; font-weight: 800; color: #b5770a; line-height:1; margin-bottom:3px; }

.metric-label {
    font-size: 11.5px;
    color: #4a6070;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

/* ── Section Cards ── */
.section-card {
    background: rgba(255,255,255,0.96);
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 22px;
    box-shadow: 0 4px 20px rgba(27,79,114,0.08);
    border: 1px solid #d6eaf8;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #eaf4fb;
}

.section-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    flex-shrink: 0;
}

.icon-blue1  { background: #d6eaf8; }
.icon-blue2  { background: #d1f0e8; }
.icon-blue3  { background: #e2dcff; }
.icon-green  { background: #d4f5e2; }

.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #1b4f72;
    margin: 0;
}

.section-desc {
    font-size: 12.5px;
    color: #7f9aaa;
    margin: 2px 0 0 0;
}

/* ── Refresh Button ── */
.stButton > button {
    background: linear-gradient(135deg, #1a6fa6, #2e86c1) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 9px 26px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-size: 14.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 14px rgba(26,111,166,0.28) !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(26,111,166,0.36) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    border-radius: 11px !important;
    padding: 9px 22px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    border-radius: 11px !important;
    border: 2px solid #a9cfe8 !important;
    font-family: 'Baloo 2', sans-serif !important;
    background: white !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 14px rgba(27,79,114,0.07) !important;
}

/* ── Alerts ── */
.stSuccess {
    border-radius: 11px !important;
    background: #eafaf1 !important;
    border-left: 4px solid #27ae60 !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #1a6fa6 !important; }

/* ── Divider ── */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, #a9cfe8, #b8e8d4, #c4b8f0) !important;
    border-radius: 2px !important;
    margin: 22px 0 !important;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.4px;
}

.badge-warning {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffc10744;
}

.badge-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #28a74544;
}

/* ── Hide Streamlit Defaults ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =====================
# CONSTANTS
# =====================
TOKEN     = "23801d339dd6d16509a79250731f126401d5f7a3"
BASE_URL  = "https://kobo.humanitarianresponse.info/api/v2"
asset_uid = "afik3gA9vpxDC2C5jbSY8C"

# =====================
# LOAD DATA
# =====================
def load_kobo_data():
    kobo = KoboExtractor(TOKEN, BASE_URL)
    start, limit, all_records = 0, 1000, []
    while True:
        data    = kobo.get_data(asset_uid, start=start, limit=limit)
        records = data["results"]
        if not records:
            break
        all_records.extend(records)
        start += limit

    df = pd.json_normalize(all_records)

    df = df.rename(columns={
        'group_og9hq60/asha':       'asha',
        'group_og9hq60/Paticipant': 'Paticipant'
    })
    df.columns = [
        col if col in ['asha', 'Paticipant']
        else col.split('/')[-1]
        for col in df.columns
    ]
    return df

# =====================
# DOWNLOAD HELPERS
# =====================
def to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8-sig')  # utf-8-sig for Excel-friendly Marathi text

def to_excel(sheets: dict):
    """sheets = {'Sheet Name': dataframe, ...}"""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        for sheet_name, df_sheet in sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=True)
    return buf.getvalue()

# =====================
# SESSION STATE
# =====================
if "df" not in st.session_state:
    with st.spinner("KoboToolbox मधून डेटा लोड होत आहे..."):
        st.session_state.df = load_kobo_data()

# =====================
# HERO HEADER
# =====================
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🌸 आशा मॉनिटरिंग डॅशबोर्ड</h1>
    <p class="hero-subtitle">KoboToolbox &nbsp;·&nbsp; रिअल-टाइम डेटा विश्लेषण &nbsp;·&nbsp; सहभागी नोंदी</p>
</div>
""", unsafe_allow_html=True)

# =====================
# REFRESH BUTTON
# =====================
col_btn, col_space = st.columns([1, 5])
with col_btn:
    if st.button("🔄 डेटा रिफ्रेश करा"):
        with st.spinner("नवीनतम डेटा आणत आहे..."):
            st.session_state.df = load_kobo_data()
        st.success("✅ डेटा यशस्वीरित्या अपडेट झाला!")

df = st.session_state.df

# =====================
# GUARD
# =====================
for col in ['asha', 'Paticipant', '_submission_time']:
    if col not in df.columns:
        st.error(f"⚠️ '{col}' कॉलम सापडला नाही. KoboToolbox फील्ड नावे तपासा.")
        st.stop()

# =====================
# DATE PROCESSING
# =====================
df['_submission_time'] = pd.to_datetime(df['_submission_time'])
df['Month']     = df['_submission_time'].dt.strftime('%b')
df['Month_num'] = df['_submission_time'].dt.month

# =====================
# DUPLICATE CALCULATION
# =====================
dup               = df[df.duplicated(subset=['asha', 'Paticipant'], keep=False)]
total_asha        = df['asha'].nunique()
total_participants = df['Paticipant'].nunique()
total_duplicates  = len(dup)

# =====================
# METRIC CARDS
# =====================
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card metric-card-1">
        <span class="metric-icon">📋</span>
        <div class="metric-value-1">{df.shape[0]}</div>
        <div class="metric-label">एकूण नोंदी</div>
    </div>
    <div class="metric-card metric-card-2">
        <span class="metric-icon">👩‍⚕️</span>
        <div class="metric-value-2">{total_asha}</div>
        <div class="metric-label">एकूण आशा</div>
    </div>
    <div class="metric-card metric-card-3">
        <span class="metric-icon">👥</span>
        <div class="metric-value-3">{total_participants}</div>
        <div class="metric-label">अनन्य सहभागी</div>
    </div>
    <div class="metric-card metric-card-4">
        <span class="metric-icon">⚠️</span>
        <div class="metric-value-4">{total_duplicates}</div>
        <div class="metric-label">डुप्लिकेट नोंदी</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================
# TABLE 1 : ASHA × MONTH
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue1">📅</div>
        <div>
            <p class="section-title">तक्ता १ · आशा फॉर्म भरलेले कॅलेंडर टेबल</p>
            <p class="section-desc">प्रत्येक महिन्यातील आशानिहाय सहभागी संख्या</p>
        </div>
    </div>
""", unsafe_allow_html=True)

table1 = pd.pivot_table(
    df, index='asha', columns='Month',
    values='Paticipant', aggfunc='count', fill_value=0
)
month_order = (
    df[['Month', 'Month_num']].drop_duplicates()
    .sort_values('Month_num')['Month']
)
table1 = table1.reindex(columns=month_order)
table1['🔢 एकूण'] = table1.sum(axis=1)
table1 = table1.sort_values('🔢 एकूण', ascending=False)

import matplotlib.colors as mcolors

def light_blue_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_blue", ["#ffffff", "#cce5f6"])

def light_teal_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_teal", ["#ffffff", "#c2ead8"])

styled = (
    table1.style
    .background_gradient(cmap=light_blue_cmap(), subset=list(month_order))
    .background_gradient(cmap=light_teal_cmap(), subset=['🔢 एकूण'])
    .format("{:.0f}")
    .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
    .set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                      ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]},
        {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
    ])
)

st.dataframe(styled, use_container_width=True, height=min(420, (len(table1) + 1) * 38 + 10))
st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 2 : DUPLICATE COUNT
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue2">🔁</div>
        <div>
            <p class="section-title">तक्ता २ · आशानुसार डुप्लिकेट नोंदी संख्या</p>
            <p class="section-desc">एकाच सहभागीच्या अनेक नोंदी असलेल्या आशा</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if len(dup) > 0:
    table2 = (
        dup.groupby('asha').agg(
            डुप्लिकेट_नोंदी=('Paticipant', 'count'),
            अनन्य_सहभागी=('Paticipant', 'nunique')
        )
        .reset_index()
        .sort_values('डुप्लिकेट_नोंदी', ascending=False)
        .rename(columns={'asha': '👩‍⚕️ आशा नाव'})
    )

    def light_peach_cmap():
        return mcolors.LinearSegmentedColormap.from_list("light_peach", ["#ffffff", "#ffe0c2"])

    def light_lavender_cmap():
        return mcolors.LinearSegmentedColormap.from_list("light_lav", ["#ffffff", "#ddd4ff"])

    styled2 = (
        table2.style
        .background_gradient(cmap=light_peach_cmap(), subset=['डुप्लिकेट_नोंदी'])
        .background_gradient(cmap=light_lavender_cmap(), subset=['अनन्य_सहभागी'])
        .format({'डुप्लिकेट_नोंदी': '{:.0f}', 'अनन्य_सहभागी': '{:.0f}'})
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                          ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]},
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
        ])
    )

    st.dataframe(styled2, use_container_width=True, height=min(360, (len(table2) + 1) * 38 + 10))
else:
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 3 : DUPLICATE DETAIL
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue3">🔍</div>
        <div>
            <p class="section-title">तक्ता ३ · आशानुसार डुप्लिकेट यादी</p>
            <p class="section-desc">निवडलेल्या आशाच्या एकाच सहभागीच्या सर्व नोंदी</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if len(dup) > 0:
    col1, col2 = st.columns([2, 4])
    with col1:
        selected_asha = st.selectbox(
            "👩‍⚕️ आशा निवडा",
            sorted(dup['asha'].unique()),
            help="डुप्लिकेट नोंदी असलेल्या आशा"
        )

    table3 = (
        dup[dup['asha'] == selected_asha][['asha', 'Paticipant', '_submission_time']]
        .sort_values('Paticipant')
        .copy()
    )
    table3['नोंदी_संख्या'] = table3.groupby('Paticipant')['Paticipant'].transform('count')
    table3 = table3.rename(columns={
        'asha':             '👩‍⚕️ आशा',
        'Paticipant':       '👤 सहभागी',
        '_submission_time': '🕐 नोंद वेळ',
        'नोंदी_संख्या':       '🔢 एकूण नोंदी'
    })

    st.markdown(f"""
    <div style="margin:10px 0 14px 0;">
        <span class="badge badge-warning">⚠️ {len(table3)} डुप्लिकेट नोंदी आढळल्या</span>
    </div>
    """, unsafe_allow_html=True)

    def light_rose_cmap():
        return mcolors.LinearSegmentedColormap.from_list("light_rose", ["#ffffff", "#ffd6d6"])

    styled3 = (
        table3.style
        .background_gradient(cmap=light_rose_cmap(), subset=['🔢 एकूण नोंदी'])
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                          ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]},
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
        ])
    )

    st.dataframe(styled3, use_container_width=True, height=min(420, (len(table3) + 1) * 38 + 10))
else:
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# DOWNLOAD SECTION
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-green">⬇️</div>
        <div>
            <p class="section-title">डेटा डाउनलोड करा</p>
            <p class="section-desc">कॅलेंडर टेबल व डुप्लिकेट यादी Excel स्वरूपात डाउनलोड करा</p>
        </div>
    </div>
""", unsafe_allow_html=True)

dl_col1, dl_col3 = st.columns(2)

# ── Calendar table ──
table1_export = table1.copy()
table1_export.index.name = 'आशा'

with dl_col1:
    st.markdown("**📅 कॅलेंडर टेबल**")
    buf_cal = io.BytesIO()
    with pd.ExcelWriter(buf_cal, engine='openpyxl') as w:
        table1_export.to_excel(w, sheet_name='कॅलेंडर टेबल', index=True)
    st.download_button(
        label="⬇️ Excel डाउनलोड",
        data=buf_cal.getvalue(),
        file_name="आशा_कॅलेंडर_टेबल.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# ── Duplicate detail list (all dup rows) ──
with dl_col3:
    st.markdown("**🔍 डुप्लिकेट यादी**")
    if len(dup) > 0:
        dup_export = dup[['asha', 'Paticipant', '_submission_time']].copy()
        dup_export.columns = ['आशा', 'सहभागी', 'नोंद वेळ']
        buf_dup3 = io.BytesIO()
        with pd.ExcelWriter(buf_dup3, engine='openpyxl') as w:
            dup_export.to_excel(w, sheet_name='डुप्लिकेट यादी', index=False)
        st.download_button(
            label="⬇️ Excel डाउनलोड",
            data=buf_dup3.getvalue(),
            file_name="आशा_डुप्लिकेट_यादी.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.info("कोणतेही डुप्लिकेट नाहीत.")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# REMAINING PARTICIPANTS SECTION
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue3">📂</div>
        <div>
            <p class="section-title">तक्ता ४ · उर्वरित सहभागी यादी</p>
            <p class="section-desc">मास्टर यादीतील सहभागी जे अद्याप आशाने नोंदवले नाहीत</p>
        </div>
    </div>
""", unsafe_allow_html=True)

import requests

MASTER_URL = "https://raw.githubusercontent.com/shrikantdeshmukh9766-ux/STATSOLUTION/main/Participant%20list.xlsx"

if "master_df" not in st.session_state:
    with st.spinner("GitHub वरून मास्टर यादी लोड होत आहे..."):
        try:
            resp = requests.get(MASTER_URL, timeout=15)
            resp.raise_for_status()
            st.session_state.master_df = pd.read_excel(io.BytesIO(resp.content))
            st.success("✅ मास्टर यादी यशस्वीरित्या लोड झाली!")
        except Exception as e:
            st.error(f"⚠️ GitHub वरून फाइल लोड करताना त्रुटी: {e}")

if "master_df" in st.session_state:
    try:
        master_df = st.session_state.master_df.copy()

        # Normalise column names — case-insensitive match
        master_df.columns = master_df.columns.str.strip()
        col_map = {c: c for c in master_df.columns}
        for c in master_df.columns:
            if c.lower() == 'asha':
                col_map[c] = 'asha'
            if c.lower() in ['paticipant', 'participant']:
                col_map[c] = 'Paticipant'
        master_df = master_df.rename(columns=col_map)

        if 'asha' not in master_df.columns or 'Paticipant' not in master_df.columns:
            st.error("⚠️ फाइलमध्ये 'asha' आणि 'Paticipant' कॉलम आढळले नाहीत. कृपया फाइल तपासा.")
        else:
            master_df['asha']       = master_df['asha'].astype(str).str.strip()
            master_df['Paticipant'] = master_df['Paticipant'].astype(str).str.strip()
            df['asha']              = df['asha'].astype(str).str.strip()
            df['Paticipant']        = df['Paticipant'].astype(str).str.strip()

            master_ashas = sorted(master_df['asha'].unique())

            # ── ASHA-wise summary table ──
            st.markdown("""
            <div style="font-size:15px; font-weight:700; color:#1b4f72; margin:18px 0 10px 0;">
                📊 आशानिहाय उर्वरित सहभागी सारांश
            </div>
            """, unsafe_allow_html=True)

            summary_rows = []
            for a in master_ashas:
                m_set = set(master_df[master_df['asha'] == a]['Paticipant'])
                s_set = set(df[df['asha'] == a]['Paticipant'])
                summary_rows.append({
                    '👩‍⚕️ आशा':        a,
                    '📋 मास्टर यादी':  len(m_set),
                    '✅ नोंदवलेले':    len(s_set & m_set),
                    '⏳ उर्वरित':      len(m_set - s_set),
                })
            summary_df = pd.DataFrame(summary_rows).sort_values('⏳ उर्वरित', ascending=False)
            summary_df.index = range(1, len(summary_df) + 1)
            summary_df.index.name = 'अ.क्र.'

            def light_amber_cmap():
                return mcolors.LinearSegmentedColormap.from_list("light_amber", ["#ffffff", "#fde5b4"])

            styled_summary = (
                summary_df.style
                .background_gradient(cmap=light_teal_cmap(),  subset=['✅ नोंदवलेले'])
                .background_gradient(cmap=light_amber_cmap(), subset=['⏳ उर्वरित'])
                .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                                  ('font-weight', '700'), ('font-size', '13px'),
                                                  ('border', '1px solid #b8d9f0')]},
                    {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
                ])
            )

            st.dataframe(
                styled_summary,
                use_container_width=True,
                height=min(400, (len(summary_df) + 1) * 38 + 10)
            )

            # Download ASHA-wise summary
            buf_summary = io.BytesIO()
            with pd.ExcelWriter(buf_summary, engine='openpyxl') as w:
                summary_df.to_excel(w, sheet_name='आशानिहाय उर्वरित', index=True)
            st.download_button(
                label="⬇️ आशानिहाय सारांश Excel डाउनलोड करा",
                data=buf_summary.getvalue(),
                file_name="आशानिहाय_उर्वरित_सारांश.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.markdown("<hr style='margin:20px 0'/>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:15px; font-weight:700; color:#1b4f72; margin:0 0 10px 0;">
                🔍 आशानिहाय उर्वरित सहभागी तपशील
            </div>
            """, unsafe_allow_html=True)

            rem_col1, rem_col2 = st.columns([2, 4])
            with rem_col1:
                selected_asha_rem = st.selectbox(
                    "👩‍⚕️ आशा निवडा",
                    master_ashas,
                    key="remaining_asha_select",
                    help="मास्टर यादीतील आशा"
                )

            master_participants   = set(master_df[master_df['asha'] == selected_asha_rem]['Paticipant'])
            submitted_participants = set(df[df['asha'] == selected_asha_rem]['Paticipant'])
            remaining             = sorted(master_participants - submitted_participants)

            total_master    = len(master_participants)
            total_submitted = len(submitted_participants & master_participants)
            total_remaining = len(remaining)

            st.markdown(f"""
            <div style="display:flex; gap:14px; margin:14px 0 18px 0;">
                <div style="background:#dbeeff; border-radius:12px; padding:14px 20px; flex:1; border:1px solid rgba(255,255,255,0.7);">
                    <div style="font-size:11px; color:#4a6070; font-weight:600; text-transform:uppercase; letter-spacing:0.7px;">मास्टर यादी</div>
                    <div style="font-size:26px; font-weight:800; color:#1a6fa6;">{total_master}</div>
                </div>
                <div style="background:#dff5ec; border-radius:12px; padding:14px 20px; flex:1; border:1px solid rgba(255,255,255,0.7);">
                    <div style="font-size:11px; color:#4a6070; font-weight:600; text-transform:uppercase; letter-spacing:0.7px;">नोंदवलेले</div>
                    <div style="font-size:26px; font-weight:800; color:#1a8a5a;">{total_submitted}</div>
                </div>
                <div style="background:#fef3dc; border-radius:12px; padding:14px 20px; flex:1; border:1px solid rgba(255,255,255,0.7);">
                    <div style="font-size:11px; color:#4a6070; font-weight:600; text-transform:uppercase; letter-spacing:0.7px;">उर्वरित</div>
                    <div style="font-size:26px; font-weight:800; color:#b5770a;">{total_remaining}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if total_remaining == 0:
                st.success(f"✅ {selected_asha_rem} यांनी मास्टर यादीतील सर्व सहभागी नोंदवले आहेत!")
            else:
                remaining_df = pd.DataFrame({
                    '👩‍⚕️ आशा': selected_asha_rem,
                    '👤 सहभागी': remaining
                })
                remaining_df.index = range(1, len(remaining_df) + 1)
                remaining_df.index.name = 'अ.क्र.'

                styled_rem = (
                    remaining_df.style
                    .set_properties(**{
                        'font-family': 'Baloo 2, sans-serif',
                        'font-size':   '13px',
                        'color':       '#1b4f72'
                    })
                    .set_table_styles([
                        {'selector': 'th',
                         'props': [('background-color', '#d6eaf8'),
                                   ('color', '#1b4f72'),
                                   ('font-weight', '700'),
                                   ('font-size', '13px'),
                                   ('border', '1px solid #b8d9f0')]},
                        {'selector': 'td',
                         'props': [('border', '1px solid #eaf4fb')]},
                    ])
                )

                st.dataframe(
                    styled_rem,
                    use_container_width=True,
                    height=min(420, (len(remaining_df) + 1) * 38 + 10)
                )

                buf_rem = io.BytesIO()
                with pd.ExcelWriter(buf_rem, engine='openpyxl') as w:
                    remaining_df.to_excel(w, sheet_name='उर्वरित सहभागी', index=True)
                st.download_button(
                    label="⬇️ उर्वरित यादी Excel मध्ये डाउनलोड करा",
                    data=buf_rem.getvalue(),
                    file_name=f"उर्वरित_सहभागी_{selected_asha_rem}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"⚠️ डेटा प्रक्रिया करताना त्रुटी आली: {e}")
else:
    st.info("⏳ मास्टर यादी लोड होत आहे, कृपया प्रतीक्षा करा...")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# FOOTER
# =====================
st.markdown("""
<hr/>
<div style="text-align:center; color:#5a8aaa; font-size:13px; padding:6px 0 14px 0;">
    🌸 आशा मॉनिटरिंग डॅशबोर्ड &nbsp;·&nbsp; KoboToolbox द्वारे &nbsp;·&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)
