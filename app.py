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
# CUSTOM CSS
# ===================== 
st.markdown(""" 
<style> 
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap'); 
html, body, [class*="css"] { font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif; } 
.stApp { background: #eaf4fb; min-height: 100vh; } 
.stApp::before { 
    content: ''; position: fixed; inset: 0; 
    background-image: radial-gradient(circle, #b8d9f0 1px, transparent 1px); 
    background-size: 28px 28px; opacity: 0.35; pointer-events: none; z-index: 0; 
} 
.block-container { padding-top: 1.8rem !important; padding-bottom: 2rem !important; position: relative; z-index: 1; } 
.hero-banner { 
    background: linear-gradient(135deg, #1b4f72 0%, #1a6fa6 50%, #2e86c1 100%); 
    border-radius: 22px; padding: 34px 40px; margin-bottom: 26px; 
    box-shadow: 0 8px 32px rgba(27,79,114,0.18), inset 0 1px 0 rgba(255,255,255,0.12); 
    position: relative; overflow: hidden; 
} 
.hero-banner::before { 
    content: '🌸'; position: absolute; right: 44px; top: 50%; 
    transform: translateY(-50%); font-size: 72px; opacity: 0.12; 
} 
.hero-title { font-size: 36px; font-weight: 800; color: #ffffff; margin: 0 0 7px 0; line-height: 1.2; text-shadow: 0 2px 8px rgba(0,0,0,0.18); } 
.hero-subtitle { color: rgba(255,255,255,0.72); font-size: 13.5px; font-weight: 400; margin: 0; letter-spacing: 0.4px; } 
.metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 26px; } 
.metric-card { 
    border-radius: 16px; padding: 20px 22px; position: relative; overflow: hidden; 
    box-shadow: 0 4px 18px rgba(27,79,114,0.10); transition: transform 0.2s, box-shadow 0.2s; 
    border: 1px solid rgba(255,255,255,0.7); 
} 
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 10px 28px rgba(27,79,114,0.15); } 
.metric-card-1 { background: linear-gradient(135deg, #dbeeff, #c2dcf7); } 
.metric-card-2 { background: linear-gradient(135deg, #dff5ec, #c2ead8); } 
.metric-card-3 { background: linear-gradient(135deg, #e8e4ff, #d3ccf9); } 
.metric-card-4 { background: linear-gradient(135deg, #fef3dc, #fde5b4); } 
.metric-card::after { 
    content: ''; position: absolute; top: -20%; right: -8%; 
    width: 70px; height: 70px; border-radius: 50%; background: rgba(255,255,255,0.35); 
} 
.metric-icon { font-size: 26px; margin-bottom: 9px; display: block; } 
.metric-value-1 { font-size: 32px; font-weight: 800; color: #1a6fa6; line-height:1; margin-bottom:3px; } 
.metric-value-2 { font-size: 32px; font-weight: 800; color: #1a8a5a; line-height:1; margin-bottom:3px; } 
.metric-value-3 { font-size: 32px; font-weight: 800; color: #5a44cc; line-height:1; margin-bottom:3px; } 
.metric-value-4 { font-size: 32px; font-weight: 800; color: #b5770a; line-height:1; margin-bottom:3px; } 
.metric-label { font-size: 11.5px; color: #4a6070; font-weight: 600; text-transform: uppercase; letter-spacing: 0.7px; } 
.section-card { 
    background: rgba(255,255,255,0.96); border-radius: 18px; padding: 26px 30px; 
    margin-bottom: 22px; box-shadow: 0 4px 20px rgba(27,79,114,0.08); border: 1px solid #d6eaf8; 
} 
.section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 2px solid #eaf4fb; } 
.section-icon { width: 40px; height: 40px; border-radius: 11px; display: flex; align-items: center; justify-content: center; font-size: 19px; flex-shrink: 0; } 
.icon-blue1 { background: #d6eaf8; } 
.icon-blue2 { background: #d1f0e8; } 
.icon-blue3 { background: #e2dcff; } 
.icon-blue4 { background: #fde8b4; } 
.icon-blue5 { background: #ffd6d6; } 
.section-title { font-size: 18px; font-weight: 700; color: #1b4f72; margin: 0; } 
.section-desc { font-size: 12.5px; color: #7f9aaa; margin: 2px 0 0 0; } 
.stButton > button { 
    background: linear-gradient(135deg, #1a6fa6, #2e86c1) !important; color: white !important; 
    border: none !important; border-radius: 11px !important; padding: 9px 26px !important; 
    font-family: 'Baloo 2', sans-serif !important; font-size: 14.5px !important; font-weight: 600 !important; 
    letter-spacing: 0.2px !important; box-shadow: 0 4px 14px rgba(26,111,166,0.28) !important; transition: all 0.2s !important; 
} 
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 22px rgba(26,111,166,0.36) !important; } 
.stSelectbox > div > div { border-radius: 11px !important; border: 2px solid #a9cfe8 !important; font-family: 'Baloo 2', sans-serif !important; background: white !important; } 
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; box-shadow: 0 2px 14px rgba(27,79,114,0.07) !important; } 
.stSuccess { border-radius: 11px !important; background: #eafaf1 !important; border-left: 4px solid #27ae60 !important; } 
.stSpinner > div { border-top-color: #1a6fa6 !important; } 
hr { border: none !important; height: 2px !important; background: linear-gradient(90deg, #a9cfe8, #b8e8d4, #c4b8f0) !important; border-radius: 2px !important; margin: 22px 0 !important; } 
.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.4px; } 
.badge-warning { background: #fff3cd; color: #856404; border: 1px solid #ffc10744; } 
.badge-success { background: #d4edda; color: #155724; border: 1px solid #28a74544; } 
.badge-danger  { background: #fde8e8; color: #922b21; border: 1px solid #e74c3c44; } 
.progress-wrap { background: #e8f4fb; border-radius: 20px; height: 10px; overflow: hidden; margin-top: 4px; } 
.progress-bar  { height: 10px; border-radius: 20px; background: linear-gradient(90deg, #1a6fa6, #27ae60); transition: width 0.4s; } 
#MainMenu, footer, header { visibility: hidden; } 
</style> 
""", unsafe_allow_html=True)

# ===================== 
# CONSTANTS 
# ===================== 
TOKEN     = "23801d339dd6d16509a79250731f126401d5f7a3" 
BASE_URL  = "https://kobo.humanitarianresponse.info/api/v2" 
asset_uid = "afWux6DQFqmZrEpK54BobD" 

# ===================== 
# HELPERS
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

def to_csv_bytes(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

def to_excel_bytes(sheets: dict):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
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
dup                = df[df.duplicated(subset=['asha', 'Paticipant'], keep=False)] 
total_asha         = df['asha'].nunique() 
total_participants = df['Paticipant'].nunique() 
total_duplicates   = len(dup) 

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

import matplotlib.colors as mcolors

def light_blue_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_blue", ["#ffffff", "#cce5f6"])
def light_teal_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_teal", ["#ffffff", "#c2ead8"])
def light_peach_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_peach", ["#ffffff", "#ffe0c2"])
def light_lavender_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_lav", ["#ffffff", "#ddd4ff"])
def light_rose_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_rose", ["#ffffff", "#ffd6d6"])
def light_red_cmap():
    return mcolors.LinearSegmentedColormap.from_list("light_red", ["#ffffff", "#ffb3b3"])

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

styled = ( 
    table1.style 
    .background_gradient(cmap=light_blue_cmap(), subset=list(month_order)) 
    .background_gradient(cmap=light_teal_cmap(), subset=['🔢 एकूण']) 
    .format("{:.0f}") 
    .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'}) 
    .set_table_styles([ 
        {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'), ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]}, 
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
    styled2 = ( 
        table2.style 
        .background_gradient(cmap=light_peach_cmap(),    subset=['डुप्लिकेट_नोंदी']) 
        .background_gradient(cmap=light_lavender_cmap(), subset=['अनन्य_सहभागी']) 
        .format({'डुप्लिकेट_नोंदी': '{:.0f}', 'अनन्य_सहभागी': '{:.0f}'}) 
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'}) 
        .set_table_styles([ 
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'), ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]}, 
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
        .sort_values('Paticipant').copy() 
    ) 
    table3['नोंदी_संख्या'] = table3.groupby('Paticipant')['Paticipant'].transform('count') 
    table3 = table3.rename(columns={ 
        'asha': '👩‍⚕️ आशा', 'Paticipant': '👤 सहभागी', 
        '_submission_time': '🕐 नोंद वेळ', 'नोंदी_संख्या': '🔢 एकूण नोंदी' 
    }) 
    st.markdown(f""" 
    <div style="margin:10px 0 14px 0;"> 
        <span class="badge badge-warning">⚠️ {len(table3)} डुप्लिकेट नोंदी आढळल्या</span> 
    </div>""", unsafe_allow_html=True) 
    styled3 = ( 
        table3.style 
        .background_gradient(cmap=light_rose_cmap(), subset=['🔢 एकूण नोंदी']) 
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'}) 
        .set_table_styles([ 
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'), ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]}, 
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]}, 
        ]) 
    ) 
    st.dataframe(styled3, use_container_width=True, height=min(420, (len(table3) + 1) * 38 + 10)) 
else: 
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.") 
st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 4 : REMAINING PARTICIPANTS
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue5">📌</div>
        <div>
            <p class="section-title">तक्ता ४ · आशानुसार उर्वरित सहभागी</p>
            <p class="section-desc">मास्टर यादीतील ज्या सहभागींचे फॉर्म अद्याप भरले नाहीत</p>
        </div>
    </div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "📂 मास्टर सहभागी CSV अपलोड करा  (कॉलम: asha, Paticipant)",
    type=["csv"],
    help="CSV मध्ये किमान दोन कॉलम असणे आवश्यक: 'asha' आणि 'Paticipant'"
)

if uploaded is not None:
    try:
        master = pd.read_csv(uploaded)

        required_cols = {'asha', 'Paticipant'}
        if not required_cols.issubset(master.columns):
            st.error(f"⚠️ CSV मध्ये '{', '.join(required_cols)}' कॉलम असणे आवश्यक आहे.")
        else:
            master['asha']       = master['asha'].astype(str).str.strip()
            master['Paticipant'] = master['Paticipant'].astype(str).str.strip()

            filled = (
                df.drop_duplicates(subset=['asha', 'Paticipant'])
                [['asha', 'Paticipant']]
                .copy()
            )
            filled['asha']       = filled['asha'].astype(str).str.strip()
            filled['Paticipant'] = filled['Paticipant'].astype(str).str.strip()
            filled['filled']     = True

            merged    = master.merge(filled, on=['asha', 'Paticipant'], how='left')
            remaining = merged[merged['filled'].isna()][['asha', 'Paticipant']].copy()

            summary = (
                master.groupby('asha')
                .agg(एकूण_सहभागी=('Paticipant', 'count'))
                .reset_index()
            )
            filled_count = (
                filled.groupby('asha')
                .agg(भरलेले=('Paticipant', 'count'))
                .reset_index()
            )
            summary = summary.merge(filled_count, on='asha', how='left').fillna(0)
            summary['भरलेले']  = summary['भरलेले'].astype(int)
            summary['उर्वरित'] = summary['एकूण_सहभागी'] - summary['भरलेले']
            summary['% पूर्ण'] = (summary['भरलेले'] / summary['एकूण_सहभागी'] * 100).round(1)
            summary = summary.sort_values('उर्वरित', ascending=False)
            summary = summary.rename(columns={'asha': '👩‍⚕️ आशा'})

            total_master    = len(master)
            total_filled    = len(filled)
            total_remaining = len(remaining)
            pct_done        = round(total_filled / total_master * 100, 1) if total_master else 0

            st.markdown(f"""
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:18px;">
                <div style="background:#dff5ec; border-radius:14px; padding:16px 20px; border:1px solid #c2ead8;">
                    <div style="font-size:11px; font-weight:700; color:#1a8a5a; text-transform:uppercase; letter-spacing:.6px;">एकूण मास्टर</div>
                    <div style="font-size:28px; font-weight:800; color:#1a8a5a;">{total_master}</div>
                </div>
                <div style="background:#dbeeff; border-radius:14px; padding:16px 20px; border:1px solid #c2dcf7;">
                    <div style="font-size:11px; font-weight:700; color:#1a6fa6; text-transform:uppercase; letter-spacing:.6px;">भरलेले</div>
                    <div style="font-size:28px; font-weight:800; color:#1a6fa6;">{total_filled}</div>
                </div>
                <div style="background:#fef3dc; border-radius:14px; padding:16px 20px; border:1px solid #fde5b4;">
                    <div style="font-size:11px; font-weight:700; color:#b5770a; text-transform:uppercase; letter-spacing:.6px;">उर्वरित</div>
                    <div style="font-size:28px; font-weight:800; color:#b5770a;">{total_remaining}</div>
                </div>
            </div>
            <div style="margin-bottom:18px;">
                <div style="font-size:12px; color:#4a6070; font-weight:600; margin-bottom:4px;">एकूण प्रगती &nbsp;·&nbsp; {pct_done}% पूर्ण</div>
                <div class="progress-wrap">
                    <div class="progress-bar" style="width:{pct_done}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            styled4 = (
                summary.style
                .background_gradient(cmap=light_teal_cmap(),     subset=['भरलेले'])
                .background_gradient(cmap=light_red_cmap(),      subset=['उर्वरित'])
                .background_gradient(cmap=light_lavender_cmap(), subset=['% पूर्ण'])
                .format({'एकूण_सहभागी': '{:.0f}', 'भरलेले': '{:.0f}', 'उर्वरित': '{:.0f}', '% पूर्ण': '{:.1f}%'})
                .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '13px', 'color': '#1b4f72'})
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'), ('font-weight', '700'), ('font-size', '13px'), ('border', '1px solid #b8d9f0')]},
                    {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
                ])
            )
            st.dataframe(styled4, use_container_width=True, height=min(420, (len(summary) + 1) * 38 + 10))

            st.markdown("---")
            st.markdown("**📋 उर्वरित सहभागींची तपशीलवार यादी**")

            col1, col2 = st.columns([2, 4])
            with col1:
                asha_filter = st.selectbox(
                    "👩‍⚕️ आशा निवडा",
                    ["सर्व"] + sorted(remaining['asha'].unique().tolist()),
                    help="विशिष्ट आशाची उर्वरित यादी पाहा"
                )

            filtered_remaining = remaining if asha_filter == "सर्व" else remaining[remaining['asha'] == asha_filter]
            filtered_remaining = filtered_remaining.rename(columns={'asha': '👩‍⚕️ आशा', 'Paticipant': '👤 उर्वरित सहभागी'})

            st.dataframe(filtered_remaining, use_container_width=True, height=min(420, (len(filtered_remaining) + 1) * 38 + 10))

            st.markdown("---")
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    label="⬇️ उर्वरित यादी CSV डाउनलोड करा",
                    data=to_csv_bytes(filtered_remaining),
                    file_name="remaining_participants.csv",
                    mime="text/csv"
                )
            with dl_col2:
                excel_data = to_excel_bytes({
                    "उर्वरित सहभागी": filtered_remaining,
                    "आशा सारांश": summary
                })
                st.download_button(
                    label="⬇️ Excel डाउनलोड करा",
                    data=excel_data,
                    file_name="remaining_participants.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"⚠️ फाइल वाचताना त्रुटी आली: {e}")

st.markdown("</div>", unsafe_allow_html=True)
