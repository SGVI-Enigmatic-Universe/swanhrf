import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import json
import requests
import base64
import bcrypt
from pathlib import Path
import numpy as np
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import geopandas as gpd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import io
import os
import textwrap
from flask import Flask, render_template
import subprocess
import threading

#python -m streamlit run app.py
#py -3.11 -m pipreqs.pipreqs "S:/swan_survey"--force

st.set_page_config(page_title="SWAN Status", page_icon="logo.png", layout="wide", initial_sidebar_state="expanded", menu_items=None)
st.markdown("""
<style>
.fit-container {
    width: 100%;          /* fixed design width */
    min-width: 1150px;
    max-width: 1150px;
    margin: auto;
    transform-origin: top center;
}

</style>
""", unsafe_allow_html=True)
st.markdown('<div class="fit-container">', unsafe_allow_html=True)

# ---- YOUR ENTIRE STREAMLIT APP HERE ----


#st.markdown("<style>.block-container {max-width: 1400px; min-width: 1400px; margin-left: 80px;}</style>", unsafe_allow_html=True)
st.markdown("<style>.block-container {max-width: 1150px; min-width: 1150px; margin: auto;}</style>", unsafe_allow_html=True)
st.markdown("<style>section[data-testid='stMain'] {padding-top: 0rem !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>section[data-testid='stMain'] > div {padding-top: 0rem !important;}</style>", unsafe_allow_html=True)
#st.markdown("<h1 style='margin-top:0rem;'>Tamil Nadu (District-wise) SWAN Survey Summary</h1>", unsafe_allow_html=True)
components.html("""
<script type="text/javascript">
    const metaOgTitle = document.createElement('meta');
    metaOgTitle.setAttribute('property', 'og:title');
    metaOgTitle.content = "SWAN";
    document.head.appendChild(metaOgTitle);
</script>
""", height=0)
st.markdown("""
        <meta property="og:title" content="SWAN">
        <meta property="og:description" content="District-level survey insights for Tamil Nadu">
        <meta property="og:image" content="https://swan.tn1st.in/logo.png">
        <meta property="og:url" content="https://swan.tn1st.in">
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto Condensed', serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    :root {
        --accent-color: #6a0dad; /* Forces slider, radio button, checkbox, etc. */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>

/* ===== GLOBAL ACCENT COLOR OVERRIDE ===== */
:root {
    --primary-color: #6a0dad;
}

/* ================= BUTTONS ================= */
div.stButton > button {
    background: #6a0dad !important;
    color: white !important;
    border: none !important;
}
div.stButton > button:hover {
    background: #5a009c !important;
}

/* ================= MULTISELECT / SELECTBOX ================= */

/* Border */
div[data-testid="stSelectbox"] div,
div[data-testid="stMultiSelect"] div {
    border-color: #6a0dad !important;
}

/* Selected pills */
span[data-baseweb="tag"] {
    background-color: #6a0dad !important;
    color: white !important;
}

/* Dropdown hover */
li[role="option"]:hover {
    background-color: #f4ecff !important;
}

/* ================= SLIDER (FORCE PURPLE) ================= */

/* Slider Text */
div[data-testid="stSlider"] * {
    color: #6a0dad !important;
}

/* ===== SLIDER THUMB ===== */
div[data-testid="stSlider"] [role="slider"] {
    background-color: #6a0dad !important;
    border-color: #6a0dad !important;
}
/* ===== ACTIVE FILLED TRACK – DEFINITIVE FIX ===== */
div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="width"] {
    background-color: #6a0dad !important;
}

/* ===== RADIO BUTTON SELECTED CIRCLE ===== */
div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] div:first-child {
    border-color: #6a0dad !important;
}

/* ===== RADIO BUTTON OUTER RING ===== */
div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] div {
    border-color: #6a0dad !important;
}

/* ===== RADIO BUTTON LABEL TEXT ===== */
div[data-testid="stRadio"] label {
    color: #6a0dad !important;
}

/* ===== ONLY SELECTED RADIO DOT ===== */
div[data-testid="stRadio"] input:checked + div {
    color: #6a0dad !important;
    border-color: #6a0dad !important;
}
/* ===== ONLY SELECTED RADIO DOT ===== */
input[type="radio"]:checked + div {
    color: #6a0dad !important;
    border-color: #6a0dad !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Fix sidebar width */
    .css-1d391kg {  /* class controlling sidebar width */
        min-width: 250px !important;
        max-width: 250px !important;
    }
    /* Optional: hide the drag handle */
    .css-1o3x0b7 { 
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Force light mode */
    html[data-theme='dark'] {
        filter: invert(0%) !important;
        background-color: rgba(241, 232, 252, 1) !important;
        color: #000000 !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
if "booted" not in st.session_state:
    st.session_state.booted = True
    #st.markdown("### 🚀 Loading SWAN Dashboard…")
    #st.progress(25)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
logo_base64 = get_base64_image("logo.png")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /*header {visibility: hidden;}*/
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""
<style>

/* ===== FIX DARK MODE TEXT VISIBILITY ===== */

/* Dropdown / multiselect text */
html[data-theme="dark"] div[data-baseweb="select"] * {
    color: white !important;
}

/* Selected items (pills) */
html[data-theme="dark"] span[data-baseweb="tag"] {
    color: white !important;
}

/* Input text inside selectbox */
html[data-theme="dark"] input {
    color: white !important;
}

/* Labels */
html[data-theme="dark"] label {
    color: white !important;
}

/* General widget text safety */
html[data-theme="dark"] .stMarkdown,
html[data-theme="dark"] .stText {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

hide_st_style = """
<style>
/* Cover top-right menu/avatar without removing header */
header[data-testid="stHeader"]::after {
    content: "";
    position: relative;
    top: 0;
    right: 0;
    width: 150px;   /* adjust width to cover menu/avatar */
    height: 100%;
    background: #f4ecff;  /* same as app background */
    z-index: 0;
}
header[data-testid="stHeader"]::before,
header[data-testid="stHeader"]::after {
    background: #f4ecff !important;        /* enforce on pseudo elements */
    content: none !important;
}


</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


header_html = f"""
<style>
header[data-testid="stHeader"] {{
    background-color: rgba(249, 247, 250, 1) !important;
    box-shadow: none !important;
    height: 70px;
}}
header[data-testid="stHeader"]::before,
header[data-testid="stHeader"]::after {{
    background: rgba(249, 247, 250, 1) !important;        /* enforce on pseudo elements */
    content: none !important;
}}
.custom-header {{
    position: fixed;
    top: 0;
    left: 55%;
    right: 0;
    transform: translateX(-50%);
    height: 70px;
    display: flex;
    align-items: center;
    padding-left: 20px;
    background: rgba(249, 247, 250, 1);
    z-index: 999999;
}}
.custom-header button,
.custom-header a {{
    pointer-events: none;
}}

.custom-header img {{
    height: 45px;
    margin-right: 12px;
}}

.custom-header-text {{
    line-height: 1.1;
}}

.custom-header-text .title {{
    font-size: 26px;
    font-weight: 700;
    color: #6a0dad;
}}

.custom-header-text .subtitle {{
    font-size: 14px;
    color: black;
}}

/* prevent content hiding behind fixed header */
.block-container {{
    padding-top: 90px;
}}
</style>

<div class="custom-header">
    <img src="data:image/png;base64,{logo_base64}">
    <div class="custom-header-text">
        <div class="title">SWAN</div>
        <div class="subtitle">Single Women's Action Network</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    section[data-testid="stMain"] > div {
        padding-top: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<div style="
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background-color:#6a0dad; /*5e2b97*/
    color:white;
    text-align:center;
    padding:6px;
    font-size:12px;
    z-index:999;
">
©This is the sister website of Human Rights Advocacy and Research Foundation  ·  Data Updated Daily
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
/* ===== PAGE BACKGROUND ===== */
.stApp {{
    background: rgba(249, 247, 250, 1);
    color: #000000;  /* force black text */
}}

/* Logo watermark */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: url("data:image/png;base64,{logo_base64}") center/45% no-repeat;
    opacity: 0.02;
    pointer-events: none;
    z-index: 0;
}}

/* Keep content above background */
.stApp > div {{
    position: relative;
    z-index: auto;
}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background: #e0d1ff;
}}

/* ===== BUTTONS ===== */
.stButton > button {{
    background: linear-gradient(135deg, #6a0dad, #8e44ad);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}}

.stButton > button:hover {{
    background: linear-gradient(135deg, #7d3cff, #a569bd);
    color: white;
}}
/* ===== FIX SIDEBAR SCROLL ===== */
section[data-testid="stSidebar"] > div:first-child {{
    height: 100vh;
    overflow-y: auto;
}}

</style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    label[data-testid="stWidgetLabel"] p {
        color: #6a0dad !important;   /* ⭐ your purple */
        font-weight: 600;            /* optional */
    }
    </style>
    """,
    unsafe_allow_html=True
)

BASE_DIR = Path(__file__).parent
USER_FILE = BASE_DIR / "user.xlsx"
USER_LOGS_FILE = "userlogs.csv"

if "user_logs_df" not in st.session_state:
    if os.path.exists(USER_LOGS_FILE):
        st.session_state.user_logs_df = pd.read_csv(USER_LOGS_FILE)

def log_user_activity(username, ngo, district, activity):
    now = datetime.now()
   # if "user_logs_df" in st.session_state:
        #df = st.session_state.user_logs_df.copy()
    if os.path.exists(USER_LOGS_FILE):
        df = pd.read_csv(USER_LOGS_FILE)
    else:
        df = pd.DataFrame(columns=[
            "NGO", "District", "Username",
            "Login at", "Logout at", "Login_DT", "Logout_DT", 
            "Event_DT", "Duration (mins)", "Activity"
        ])
    for col in [
        "NGO", "District", "Username",
        "Login at", "Logout at",
        "Login_DT", "Logout_DT",
        "Event_DT", "Duration (mins)", "Activity"
    ]:
        if col not in df.columns:
            df[col] = pd.NaT

    # Parse Login_DT safely
    df["Login_DT"] = pd.to_datetime(
        df["Login at"],
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    )
    if activity == "Login":
        active = df[
            (df["Username"] == username) &
            (df["Activity"] == "Login") &
            (df["Logout_DT"].isna())
        ]

        if not active.empty:
            # already logged in → DO NOTHING
            st.session_state.user_logs_df = df
            #df.to_csv(USER_LOGS_FILE, index=False)
            return
        new_row = {
            "NGO": ngo,
            "District": district,
            "Username": username,
            "Login at": now.strftime("%d-%b-%Y@%I:%M:%S%p"),
            "Logout at": None,
            "Login_DT":now, 
            "Logout_DT":pd.NaT,
            "Duration (mins)": None,
            "Activity": "Login"
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    elif activity == "Logout":
        mask = (
            (df["Username"] == username) &
            (df["Activity"] == "Login") &
            (df["Logout_DT"].isna())
        )

        if mask.any():
            idx = df[mask].index[-1]
            login_dt = df.loc[idx, "Login_DT"]
            duration = (
                round((now - login_dt).total_seconds() / 60, 2)
                if pd.notna(login_dt)
                else None
            )
            df.loc[idx, "Logout at"] = now.strftime("%d-%b-%Y@%I:%M:%S%p")
            df.loc[idx, "Logout_DT"] = now
            df.loc[idx, "Event_DT"] = now
            df.loc[idx, "Duration (mins)"] = duration
    # ------------------------
    # Handle OTHER ACTIVITIES
    # ------------------------
    else:
        new_row = {
            "NGO": ngo,
            "District": district,
            "Username": username,
            "Login at": None,
            "Logout at": None,
            "Login_DT": None,
            "Logout_DT": None,
            "Event_DT": now,
            "Duration (mins)": None,
            "Activity": activity
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_csv(USER_LOGS_FILE, index=False) #to csv
    st.session_state.user_logs_df = df  # cache only


@st.cache_data
def load_users():
    return pd.read_excel(USER_FILE)
users_df = load_users()

for key in ["authenticated", "user", "role", "ngo", "district", "ngo_name", "selected_page"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "ngo" not in st.session_state:
    st.session_state.ngo = None
if "district" not in st.session_state:
    st.session_state.district = None
if "ngo_name" not in st.session_state:
    st.session_state.ngo_name = None
if "selected_page" not in st.session_state or st.session_state.selected_page is None:
    st.session_state.selected_page = "Overview"

def login():
    st.markdown("""
    <style>
    /* Center column container that HAS login-card */
    div[data-testid="stVerticalBlock"]:has(.login-card) {
        /*background: linear-gradient(135deg, #6a0dad, #8121ff);*/
        background: transparent !important; /* remove big purple background */
        padding: 0px;
        border-radius: 50px;
        box-shadow: 50px;
        color: #6a0dad;
        text-align: center;
        justify-content: center;
        align-item: center;
    }
    /* Logo centered */
    .login-card img {
        display: block;
        margin: 0 auto 20px auto;
    }
    .login-card h3 {
        text-align: center; 
    }
    
    /* Remove form background */
    div[data-testid="stForm"] {
        background: linear-gradient(135deg, #8121ff, #6a0dad);
        border-radius: 30px !important;
        padding: 20px !important;
        justify-content: center;
        align-item: center; 
        
    /* Force ALL input labels to white */
    [data-testid="stWidgetLabel"] p {
        color: white !important;
    }


 
    }
    div[data-testid="stForm"] label { color: white !important; }
    /* Button */
    .login-card .stButton > button {
        padding: 5px 26px;
        background: white;
        color: white;
        font-weight: 1000;
        border-radius: 10px;
        border: white;
        margin-top: 18px;
        cursor: pointer;
        justify-content: center;
        align-item: center;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.container():
            st.markdown('<div class="login-card">', unsafe_allow_html=True)

            st.markdown(
                f'<div style="margin-top:-150px; text-align:center;"><img src="data:image/png;base64,{logo_base64}" width="150"></div>',
                unsafe_allow_html=True
            )

            #st.markdown("### 🔐 Login")
            st.markdown('<h3 style="text-align:center;">🔐 Login</h3>', unsafe_allow_html=True)

            st.markdown(
                    """
                    <style>
                    /* Force all Streamlit input boxes (text and password) to have white background and black text */
                    div.stTextInput>div>div>input {
                        background-color: white !important;
                        color: black !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            # ✅ Before your login form
            loading_placeholder = st.empty()
            loading_placeholder.info("⏳ Loading authentication...")
            with st.form("login_form"):
                username = st.text_input("User ID")
                password = st.text_input("Password", type="password")
                
                b1, b2, b3 = st.columns([1, 1, 1])
                with b2:
                    submitted = st.form_submit_button("Login")

            st.markdown('</div>', unsafe_allow_html=True)
            loading_placeholder.empty()
    if not submitted:
        st.stop()
        #return    
    user_row = users_df[users_df["UserID"] == username]
    if user_row.empty:
        st.error("Invalid credentials")
        return
    user = user_row.iloc[0]
    st.session_state.ngo_name = user["NGO"]
    if not bool(user["Active"]):
        st.error("User is inactive. Contact administrator.")
        return
    stored_hash = str(user["Password"]).strip()
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
    #if bcrypt.checkpw(password.encode(), user["Password"] .encode()):
        st.session_state.authenticated = True
        st.session_state.user = username
        st.session_state.role = str(user["Role"]).lower()
        st.session_state.district = user["District"]
        st.session_state.ngo_name = user["NGO"]
        #if "selected_page" not in st.session_state:
        log_user_activity(
            username,
            user["NGO"],
            user["District"],
            "Login"
        )
        # persist_logs()
        st.session_state.login_logged = True
        st.session_state.selected_page = "Submissions"
        #return
        st.rerun()
    else:
        st.error("Invalid credentials")
        
def logout_user(username):
    now = datetime.now()
    # if "user_logs_df" in st.session_state:
    #     df = st.session_state.user_logs_df.copy()
    if not os.path.exists(USER_LOGS_FILE):
        #df = pd.read_csv(USER_LOGS_FILE)
    #else:
        return
    df = pd.read_csv(USER_LOGS_FILE)
    if df.empty:
        return
    # Ensure required columns exist
    for col in ["Login at", "Logout at", "Login_DT", "Logout_DT"]:
        if col not in df.columns:
            df[col] = pd.NaT

    # Parse Login_DT safely
    df["Login_DT"] = pd.to_datetime(
        df["Login at"],
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    )
    mask = (
        (df["Username"] == username) &
        (df["Activity"] == "Login") &
        (df["Logout at"].isna())
    )
    if not df[mask].empty:
        idx = df[mask].index[-1]
        login_dt = df.loc[idx, "Login_DT"]
        if pd.notna(login_dt):
            duration = round((now - login_dt).total_seconds() / 60, 2)
        else:
            duration = None
        #login_time = pd.to_datetime(df.loc[idx, "Login at"])
        #duration = (now - login_time).total_seconds() / 60
        df.loc[idx, "Logout at"] = now.strftime("%d-%b-%Y@%I:%M:%S%p")
        df.loc[idx, "Logout_DT"] = now
        df.loc[idx, "Duration (mins)"] = duration
   
    df.to_csv(USER_LOGS_FILE, index=False)
    st.session_state.user_logs_df = df
   
# Redirect to Submissions after login
if st.session_state.authenticated and st.session_state.get("selected_page") is None:
    st.session_state.selected_page = "Submissions"
if st.session_state.get("authenticated"):
    # if st.sidebar.button("🚪Logout", key="global_logout"):
    #     logout_user(st.session_state.user)
    #     #st.session_state.clear()
    #     for k in ["authenticated", "user", "role", "ngo", "district", "ngo_name", "selected_page", "login_logged"]:
    #         st.session_state.pop(k, None)
    #     st.rerun()
    col1, col2 = st.sidebar.columns([1,1.5])  # Adjust width ratio as needed
    with col1:
        if st.button("🚪Logout", key="global_logout"):
            logout_user(st.session_state.user)
            for k in ["authenticated", "user", "role", "ngo", "district", "ngo_name", "selected_page", "login_logged"]:
                st.session_state.pop(k, None)
            st.rerun()
    with col2:
        if st.button("📤Evidence", key="upload_evidence"):
            appsheet_url = "https://tinyurl.com/swantracking"  # <-- replace with your AppSheet URL
            st.query_params = {}  # This clears all query parameters
            st.markdown(f"[Go to Upload Evidence]({appsheet_url})", unsafe_allow_html=True)
            log_user_activity(
                st.session_state.user,
                st.session_state.ngo_name,
                st.session_state.district,
                "Evidence Upload"
            )
# =====================
# LOAD DATA
# =====================
#df = pd.read_excel("survey.xlsx")
@st.cache_data(show_spinner=False)
def load_data():
    #df = pd.read_csv("ksurvey.csv.gz", compression="gzip", encoding="utf-8", low_memory=False)
    sheet_id = "1826GGT50IjlTBgLCrqpiJV8fcS9siJ2KfT90PYArC00"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    #start = time.time()
    df = pd.read_csv(sheet_url)
    df = df.dropna(how='all')
    #st.write("Sheet loaded in", time.time() - start, "seconds")
    #st.dataframe(df, use_container_width=True, hide_index=True)
    # Clean column names (VERY IMPORTANT for Google Sheets)
    df['end'] = pd.to_datetime(df['end'], errors='coerce')
    if hasattr(df['end'].dt, "tz"):
        df['end'] = df['end'].dt.tz_localize(None)
    return df
df = load_data()


DISTRICT_MAP = {
    "அரியலூர்": "Ariyalur",
    "செங்கல்பட்டு": "Chengalpet",
    "சென்னை": "Chennai",
    "கோயம்புத்தூர்": "Coimbatore",
    "கடலூர்": "Cuddalore",
    "தருமபுரி": "Dharmapuri",
    "திண்டுக்கல்": "Dindigul",
    "ஈரோடு": "Erode",
    "கள்ளக்குறிச்சி": "Kallakurichi",
    "கன்னியாகுமரி":"Kanyakumari",
    "காஞ்சிபுரம்": "Kanchipuram",
    "கரூர்": "Karur",
    "கிருஷ்ணகிரி": "Krishnagiri",
    "மதுரை": "Madurai",
    "மயிலாடுதுறை": "Mayiladuthurai",
    "நாகப்பட்டினம்": "Nagapattinam",
    "நாமக்கல்": "Namakkal",
    "நீலகிரி": "Nilgiris",
    "பெரம்பலூர்": "Perambalur",
    "புதுக்கோட்டை": "Pudukkottai",
    "ராமநாதபுரம்": "Ramanathapuram",
    "ராணிப்பேட்டை": "Ranipet",
    "சேலம்": "Salem",
    "சிவகங்கை": "Sivagangai",
    "தென்காசி": "Tenkasi",
    "தஞ்சாவூர்": "Thanjavur",
    "தேனி": "Theni",
    "தூத்துக்குடி": "Thoothukudi",
    "திருநெல்வேலி": "Tirunelveli",
    "திருப்பத்தூர்": "Tirupathur",
    "திருப்பூர்": "Tiruppur",
    "திருவள்ளூர்": "Tiruvallur",
    "திருவண்ணாமலை": "Tiruvannamalai",
    "திருவாரூர்": "Tiruvarur",
    "திருச்சிராப்பள்ளி": "Tiruchirappalli",
    "வேலூர்": "Vellore",
    "விழுப்புரம்": "Villupuram",
    "விருதுநகர்": "Virudhunagar"
}
# =====================
# CONFIG
# =====================
DISTRICT_COL = "1.மாவட்டத்தின் பெயர்"
NGO_COL = "2.கணக்கெடுப்பு நடத்தும் அமைப்பின் பெயர்"
DOB_COL = "6.பிறந்த தேதி (அடையாள அட்டையின் படி)"
SYSTEM_COLS = [
    "_uuid", "_status", "version",
    "location_start", "location_end",
    "start", "end", "age", "_location_start_latitude", 
    "_location_start_longitude", "_location_start_altitude", 
    "_location_start_precision", "_id", "_uuid", "_uuid.1", "_submission_time",
    "_validation_status", "_notes", "_status", "_submitted_by",
    "__version__", "_tags", "_index", "has_real_data", "all_sel",
    "3.உங்கள் தற்போதைய இருப்பிடம்: ${location_start}"
]

st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
<style>
/* Override option-menu icon font-family */
.bi {
    font-family: "Bootstrap Icons" !important;
}
</style>
""", unsafe_allow_html=True)

columns_in_order = [c for c in df.columns if c not in SYSTEM_COLS]
options = ["Overview", "Submissions", "Dashboard", "Entitlements"]
icons = ["file-earmark-text", "stack-overflow", "bar-chart-line", "file-person"]

UserID = st.session_state.get("user")
role = st.session_state.get("role")

users_df = pd.read_excel(USER_FILE)  # or wherever your users are stored

# 2️⃣ Add admin-only page
if st.session_state.get("role") == "admin":
    options.append("User Activity")
    icons.append("file-earmark-lock2")  # icon for user activity
    options.append("Add New Users")
    icons.append("person-plus")
# Only HRF Super Admin
if role == "admin" and UserID == "hrfadmin" :
    options.append("Manage Users")
    icons.append("people")
    
with st.sidebar:
    selected = option_menu(
        menu_title="Menu 🔎",
        options=options,
        icons=icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0px",
                "background-color": "#e0d1ff",
                "border-radius": "0px"
            },
            "icon": {
                "color": "white",
                "font-size": "18px"
            },
            "nav-link": {
                "background": "linear-gradient(135deg, #a480d3, #a480d3)",
                #8121ff, #6b3ba9)",
                "color": "white",
                "font-weight": "600",
                "border-radius": "15px",
                "margin": "6px",
                "padding": "10px 30px"
            },
            "nav-link-hover": {
                "background": "linear-gradient(135deg, #7d3cff, #a569bd)",
                "color": "white"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #6a0dad, #6a0dad)",
                "color": "white",
                "font-weight": "800"
            }
        }
    )
st.session_state["selected_page"] = selected
page = selected

# =====================
# OVERVIEW PAGE
# =====================
if page == "Overview":
    #st.title("Tamil Nadu (District-wise) SWAN Survey Summary")
    #st.markdown("<h1 style='margin-top:0rem;'>Tamil Nadu (District-wise) SWAN Survey Summary</h1>", unsafe_allow_html=True)
    
    st.markdown(
        "<div style='text-align:center; margin-top:-100px; margin-bottom:0px;'><h2 style='font-size:30px; color:#6a0dad'>Tamil Nadu (District-wise) SWAN Survey Summary</h2></div>",
        unsafe_allow_html=True
    )
#border:2px solid #6b3ba9
    #start = time.time()
    # --- KPI CSS
    district_count = f"{df[DISTRICT_COL].nunique():,}"
    ngo_count = f"{df[NGO_COL].nunique():,}"
    total_submissions = f"{len(df):,}"
    # --- Display KPI cards
    col1, col2, col3, col4 = st.columns([0.3, 0.5, 1.5, 0.3])
    with col2:
        st.write("")
        st.markdown(f"""<div style="display:flex;">
        <div style="flex:1; aspect-ratio: 3 / 1; border-radius:14px; color:white; font-weight:600; box-shadow:0 4px 10px rgba(0,0,0,0.15); text-align:center; background: linear-gradient(135deg, #6a0dad, #6a0dad);
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    padding: 2%;
                    box-sizing: border-box;
                    margin-top:60px;
                    margin-bottom:30px;">
        <div style="font-size:20px; line-height:1.1; margin-bottom:0px; opacity:0.9;">Districts</div>
        <div style="font-size:30px; line-height:1; margin:0; margin-top:0px; margin-bottom:0px;">{district_count}</div>
        </div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="display:flex;">
        <div style="flex:1; aspect-ratio: 3 / 1; border-radius:14px; color:white; font-weight:600; box-shadow:0 4px 10px rgba(0,0,0,0.15); text-align:center; background: linear-gradient(135deg, #6a0dad, #6a0dad);
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    padding: 2%;
                    box-sizing: border-box;
                    margin-bottom:30px;">
        <div style="font-size:20px; line-height:1.1; margin-bottom:0px; opacity:0.9;">NGOs</div>
        <div style="font-size:30px; line-height:1; margin:0; margin-top:0px; margin-bottom:0px;">{ngo_count}</div>
        </div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div style="display:flex;">
        <div style="flex:1; aspect-ratio: 3 /1 ; border-radius:14px; color:white; font-weight:600; box-shadow:0 4px 10px rgba(0,0,0,0.15); text-align:center; background: linear-gradient(135deg, #6a0dad, #6a0dad);
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    padding: 2%;
                    box-sizing: border-box;
                    margin-bottom:30px;">
        <div style="font-size:20px; line-height:1.1; margin-bottom:0px; opacity:0.9;">Total Submissions</div>
        <div style="font-size:30px; line-height:1; margin:0; margin-top:0px; margin-bottom:0px;">{total_submissions}</div>
        </div>
        </div>""", unsafe_allow_html=True)
        
        sheet_id = "1dlxiNuYJlaBv5BSpeBzZmuPDgcMUNsSBSB8DrKkNNp8"
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df_ent = pd.read_csv(sheet_url)
        df_ent.columns = df_ent.columns.str.strip()
        # Ensure 'Received' column exists and is numeric
        if "Status" in df_ent.columns:
            total_received = df_ent[df_ent["Status"] == "Received"].shape[0]
        else:
            total_received = 0
        total_received_formatted = f"{total_received:,}"
        st.markdown(f"""<div style="display:flex;">
        <div style="flex:1; aspect-ratio: 3 /1 ; border-radius:14px; color:white; font-weight:600; box-shadow:0 4px 10px rgba(0,0,0,0.15); text-align:center; background: linear-gradient(135deg, #6a0dad, #6a0dad);
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    align-items:center;
                    padding: 2%;
                    box-sizing: border-box;
                    margin-bottom:30px;">
        <div style="font-size:20px; line-height:1.1; margin-bottom:0px; opacity:0.9;">Total Entitlements</div>
        <div style="font-size:30px; line-height:1; margin:0; margin-top:0px; margin-bottom:0px;">{total_received_formatted}</div>
        </div>
        </div>""", unsafe_allow_html=True)
    @st.cache_data(show_spinner=False)
    def load_map_assets(df):
        with open("tn_districts_simplified.geojson", "r", encoding="utf-8") as f:
            geojson = json.load(f)
        for idx, feature in enumerate(geojson["features"]):
            feature["id"] = idx
            
        df = df.copy()
        df['District_EN'] = df[DISTRICT_COL].map(DISTRICT_MAP).fillna(df[DISTRICT_COL])
        totals = df.groupby('District_EN').size().reset_index(name='Total Submissions')    
    
        features = []
        for idx, feature in enumerate(geojson["features"]):
            district_name = feature["properties"]["dist"]
            total = totals.loc[totals['District_EN']==district_name, 'Total Submissions']
            #total_value = int(total.values[0]) if len(total) else 0
            features.append({'feature_id': idx,'District': district_name,'Total Submissions': int(total.iloc[0]) if len(total) else 0})
        return geojson, pd.DataFrame(features)
    geojson_data, map_df_full = load_map_assets(df)
    
    @st.cache_data(show_spinner=False, persist="disk")
    def prepare_map_df(map_df_full, geojson_data):
    # --- Choropleth 
        custom_scale = [
            [0, "#ffffff"], # start from white
            [0.01, "#e0c3f4"],
               # middle light purple (adjust as you like)
            [1, "#6a0dad"]       # dark purple at the max
        ]

        fig = px.choropleth_mapbox(
            map_df_full,
            geojson=geojson_data,
            locations="feature_id",
            color="Total Submissions",
            color_continuous_scale=custom_scale,
            hover_data={'District': True, 'Total Submissions': True, 'feature_id': False},
            mapbox_style="carto-positron",
            center={"lat": 10.9, "lon": 78.8},
            zoom=6,
            labels={'Total Submissions': 'Submissions'}
        )
        
        fig.update_layout(
            mapbox={
                'style': {'version': 8,'sources': {},'layers': []},
                'domain': {'x': [0.0, 1.0],'y': [0.0, 1.0]}},
            paper_bgcolor='rgba(0,0,0,0)',
            margin={"r":0,"t":0,"l":0,"b":0},
            height=550,
            autosize=True, font=dict(color="black"),
            coloraxis_colorbar=dict(
                x=0.85,y=0.55,xanchor='left',len=0.5,thickness=10,
                tickfont=dict(color="black", size=12),   # ⭐ ticks
                title=dict(text="Submissions", font=dict(color="black")),          # ⭐ title
                outlinecolor="black", outlinewidth=0.7
            ))
        return fig
    fig = prepare_map_df(map_df_full,geojson_data)
    #st.session_state.map_render_id = st.session_state.get("map_render_id", 0) + 1
    # with col2:
    # col1,col2,col3 = st.columns([0.3, 2, 0.5])
    with col3:
        #st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=f"district_map_{st.session_state.map_render_id}")
        components.html(fig.to_html(include_plotlyjs="cdn",full_html=False,config={"displayModeBar": False}),height=550)
    # --- Group by district and NGO
    @st.cache_data(show_spinner=False)
    def get_grouped_ngo(df, DISTRICT_COL, NGO_COL):
        grouped_ngo = (df.groupby([DISTRICT_COL, NGO_COL]).size().reset_index(name='Count per NGO'))
        # --- Aggregate district total
        district_totals = grouped_ngo.groupby(DISTRICT_COL)['Count per NGO'].sum().reset_index(name='Total per District')
        return grouped_ngo.merge(district_totals, on=DISTRICT_COL)
    grouped_ngo = get_grouped_ngo(df, DISTRICT_COL, NGO_COL)

    grouped_ngo["_District_EN"] = grouped_ngo[DISTRICT_COL].map(DISTRICT_MAP).fillna(grouped_ngo[DISTRICT_COL])
    grouped_ngo["_NGO_EN"] = grouped_ngo[NGO_COL].astype(str)
    grouped_ngo = grouped_ngo.sort_values(
        by=["_District_EN", "_NGO_EN"],
        kind="mergesort"   # keeps group stability
    ).reset_index(drop=True)
    grouped_ngo["District"] = grouped_ngo["_District_EN"]
    grouped_ngo["NGO"] = grouped_ngo[NGO_COL]
    grouped_ngo = grouped_ngo.drop(columns=["_District_EN", "_NGO_EN"])

    grouped_ngo["Total_Display"] = grouped_ngo["Total per District"]
    
    serials = []
    prev_district = None
    serial_num = 1
    for district in grouped_ngo[DISTRICT_COL]:
        if district != prev_district:
            serials.append(serial_num)
            prev_district = district
            serial_num += 1
        else:
            serials.append(np.nan)
    grouped_ngo["S.N."] = serials  # 👈 Use proper header
    #grouped_ngo["S.N."] = grouped_ngo["S.N."].astype("Int64")

    # --- Columns to display
    final_df = grouped_ngo[["S.N.", "District", "NGO", "Count per NGO", "Total_Display"]]
    final_df_display = final_df.copy()

    final_df = grouped_ngo[["S.N.", "District", "NGO", "Count per NGO", "Total_Display"]].copy()
    final_df = final_df.rename(columns={"Total_Display": "Total per District"})
    final_df["District"] = final_df["District"].map(DISTRICT_MAP).fillna(final_df["District"])

    
    display_df = final_df.copy()
    # Fill NaN with previous serial number for rowspan calculation
    display_df["S.N."] = display_df["S.N."].ffill().astype(int)

    # --- Calculate rowspan for merged cells in S.N., District, Total per District
    
    def compute_rowspan(series):
        rowspan = []
        prev_val = object()  # unique placeholder
        count = 0
        temp_counts = []
        for val in series:
            val_safe = val if pd.notna(val) else object()
            if val_safe == prev_val:
                count += 1
            else:
                if count > 0:
                    temp_counts.extend([count]*count)
                count = 1
                prev_val = val_safe
        temp_counts.extend([count]*count)
        return pd.Series(temp_counts)
    rowspan_dict = {col: compute_rowspan(display_df[col]) for col in ["S.N.", "District", "Total per District"]}
    printed = {col: set() for col in ["S.N.", "District", "Total per District"]}

    html = '<table style="width:100%; border-collapse: collapse;">'
    html += '<thead>'
    html += '<tr style="background-color: rgba(106,13,173,0.1); ">'
    html += '<th style="padding:6px; text-align:center; font-weight:600; font-size:15px;">S.N.</th>'
    html += '<th style="padding:10px; text-align:left; font-weight:600; font-size:15px;">&nbsp;District</th>'
    html += '<th style="padding:10px; text-align:left; font-weight:600; font-size:15px;">&nbsp;Organisation Name (NGO)</th>'
    html += '<th style="padding:6px; text-align:center;font-weight:600; font-size:15px; ">Count per NGO</th>'
    html += '<th style="padding:6px; text-align:center; font-weight:600; font-size:15px;">Total per District</th>'
    html += '</tr></thead>'
    html += '<tbody>'

    for i, row in display_df.iterrows():
        html += '<tr style="background-color: rgba(255,255,255,0);">'
        for col in ["S.N.", "District", "NGO", "Count per NGO", "Total per District"]:
            if col in ["S.N.", "District", "Total per District"]:
                if i not in printed[col]:
                    span = int(rowspan_dict[col].iloc[i])
                    val = "" if pd.isna(row[col]) else row[col]
                    style = "text-align:left;" if col=="District" else "text-align:center; "
                    html += f'<td rowspan="{span}" style="{style} vertical-align: top; ">{val}</td>'
                    printed[col].update(range(i, i+span))
            else:
                style = "text-align:left;" if col=="NGO" else "text-align:center;"
                val = "" if pd.isna(row[col]) else row[col]
                html += f'<td style= "{style}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)
    #st.markdown('<p style="color:#6a0dad; font-weight:bold;">Last updated: 09 Feb 2026</p>', unsafe_allow_html=True)
    
    today_india = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y")

    st.markdown(
        f"""
        <div style='text-align:left; margin-top:-20px; margin-bottom:0px;'>
            <h2 style='font-size:15px; color:#6a0dad'>⇒ Last updated: {today_india}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# =====================
# SUBMISSIONS PAGE
# =====================
elif page == "Submissions":
    if "login_ready" not in st.session_state:
        placeholder = st.empty()
        with placeholder.container():
            with st.spinner("Loading secure login..."):
                time.sleep(0.8)
        st.session_state.login_ready = True
        st.rerun()

    if not st.session_state.authenticated:
        placeholder = st.empty()
        with placeholder.container():
            login()
        st.stop()
        
    is_admin = st.session_state.get("role") == "admin"
    english_to_tamil = {v: k for k, v in DISTRICT_MAP.items()}  # invert your dict

    user_district_en = st.session_state.get("district", "")
    user_district_ta = english_to_tamil.get(user_district_en, None)  # None if not found
    #user_district = st.session_state.get("district","")
    user_ngo = st.session_state.get("ngo_name", "")
    
    st.markdown(f"""
    <div style="text-align:left; margin-top:-100px;">
        <h2 style="font-size:30px; color:#6a0dad; font-family:'Roboto Condensed', sans-serif;">
            Greetings! {user_ngo}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    #st.write(f"District: {st.session_state.get('district','')}")
    st.markdown(f"""
    <div style="text-align:left; margin-top:-70px;">
        <h2 style="font-size:15px; color:#6a0dad; font-family:'Roboto Condensed', sans-serif;">
            District: {user_district_en}
        </h2>
    </div>
    """, unsafe_allow_html=True)
   
    if st.session_state.get("role") != "admin":
        df_user = df[(df[DISTRICT_COL] == user_district_ta) & (df[NGO_COL] == st.session_state.get("ngo_name", ""))]
    else:
        df_user = df.copy()

# SIDEBAR
# =====================
    st.sidebar.write("Filters")
    # Start from full user dataframe
    df_temp = df_user.copy()
    selected_filters = {}
    # --- Compute available options dynamically
    if sel_ngo := st.session_state.get("ngo_filter"):  # if NGO already selected
        district_vals = sorted(df_temp[df_temp[NGO_COL].isin(sel_ngo)][DISTRICT_COL].dropna().unique())
    else:
        district_vals = sorted(df_temp[DISTRICT_COL].dropna().unique())
    district_vals = [str(d).strip() for d in district_vals]

    if sel_district := st.session_state.get("district_filter"):  # if district already selected
        ngo_vals = sorted(df_temp[df_temp[DISTRICT_COL].isin(sel_district)][NGO_COL].dropna().unique())
    else:
        ngo_vals = sorted(df_temp[NGO_COL].dropna().unique())
    ngo_vals = [str(n).strip() for n in ngo_vals]

    # --- Defaults for non-admin
    default_districts_sidebar = [user_district_ta] if (not is_admin and user_district_ta in district_vals) else []
    default_ngos_sidebar = [user_ngo] if (not is_admin and user_ngo in ngo_vals) else []

    # --- Sidebar multiselects
    sel_district = st.sidebar.multiselect(DISTRICT_COL, district_vals, default=default_districts_sidebar, key="district_filter")
    sel_ngo = st.sidebar.multiselect(NGO_COL, ngo_vals, default=default_ngos_sidebar, key="ngo_filter")
    
    # --- Apply final filtering
    mask_district = df_user[DISTRICT_COL].isin(sel_district) if sel_district else pd.Series(True, index=df_user.index)
    mask_ngo = df_user[NGO_COL].isin(sel_ngo) if sel_ngo else pd.Series(True, index=df_user.index)
    df_user = df_user[mask_district & mask_ngo]
    
    filtered_df = df_user.copy()
    valid_dates = filtered_df['end'].dropna()
    if not valid_dates.empty:
        min_date_py = valid_dates.min().date()
        max_date_py = valid_dates.max().date()
        if min_date_py == max_date_py:
            max_date_py = min_date_py + pd.Timedelta(days=1)
    else:
        # fallback: use some reasonable default
        min_date_py = pd.Timestamp.today().date()
        max_date_py = min_date_py + pd.Timedelta(days=1)

# --- Range slider for start and end
    selected_start, selected_end = st.sidebar.slider(
        "3.கணக்கெடுப்பு சமர்ப்பிப்புத் தேதி வரம்பைத் தேர்ந்தெடுக்கவும்",
        min_value=min_date_py,
        max_value=max_date_py,
        value=(min_date_py, max_date_py),  # default full range
        format="DD-MM-YYYY"
    )
    start_dt = pd.Timestamp(selected_start)
    end_dt = pd.Timestamp(selected_end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

# --- Filter dataframe for selected range
    filtered_range_df = filtered_df[(filtered_df['end'] >= start_dt) & (filtered_df['end'] <= end_dt)].copy()

# -------------------------------
# Month-wise total submissions (entire dataset)
# -------------------------------
    month_counts = (
            filtered_df.assign(Month=filtered_df['end'].dt.to_period('M').dt.to_timestamp())
            .groupby('Month').size().reset_index(name='Submitted'))
    month_counts['Month'] = month_counts['Month'].dt.strftime('%b %Y')
    month_counts = month_counts.sort_values('Month').reset_index(drop=True)
    month_counts.insert(0, "            #", range(1, len(month_counts)+1))
# =====================
# QUESTION FILTERS (SINGLE PASS, EXCEL ORDER)
# =====================
    if DOB_COL in filtered_df.columns:
        filtered_df[DOB_COL] = pd.to_datetime(df[DOB_COL], errors="coerce")
    filtered_df[DOB_COL].dt.strftime("%d-%m-%Y")
    # Get all question columns except DISTRICT_COL and NGO_COL
    question_cols = [col for col in columns_in_order if col not in [DISTRICT_COL, NGO_COL]]
    # Sort alphabetically
    question_cols_sorted = sorted(question_cols, key=lambda x: x.lower())  # case-insensitive
    mask = pd.Series(True, index=filtered_df.index)
# District & NGO filters (already handled)
    if sel_district:
        mask &= filtered_df[DISTRICT_COL].isin(sel_district)
    if sel_ngo:
        mask &= filtered_df[NGO_COL].isin(sel_ngo)
    rendered_multi = set()
    selected_filters = {DISTRICT_COL: sel_district, NGO_COL: sel_ngo}
    for col in columns_in_order:
        if col in [DISTRICT_COL, NGO_COL]:
            continue
        df_for_options = filtered_df[mask].copy()
        if "/" in col:
            question = col.split("/", 1)[0]
            if question in rendered_multi:
                continue  # already rendered
            rendered_multi.add(question)
            # collect options IN EXCEL ORDER
            option_cols = [c for c in columns_in_order if c.startswith(question + "/")]
            with st.sidebar.expander(question, expanded=False):
                for opt_col in option_cols:
                    opt_label = opt_col.split("/", 1)[1]
                    choice = st.radio(opt_label, ["All", "Yes (1)", "No (0)"], horizontal=True,key=opt_col)
                    if choice == "Yes (1)":
                        mask &= (filtered_df[opt_col] == 1)
                    elif choice == "No (0)":
                        mask &= (filtered_df[opt_col] == 0)
    
        # -------- SINGLE-SELECT / INTEGER / TEXT
        else:
            #df_current = filtered_df[mask]
            options = df_for_options[col].dropna().unique().tolist()
            if not options:
                continue
            options_sorted = sorted(options, key=lambda x: str(x).lower())
            selected = st.sidebar.multiselect(col, ["All"] + options_sorted, key=f"filter_{col}")
            if selected and "All" not in selected:
                mask &= df_for_options[col].isin(selected)
                selected_filters[col] = selected
    
    filtered_df = filtered_df[mask].copy()  # only filter once
# -------------------------------
# Filter for selected date range # Show total submissions in selected range
# -------------------------------
    st.markdown("""
    <style>
    /* ===== DATAFRAME TRANSPARENCY ===== */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0);  /* 30% transparent */
        border-radius: 10px;
        padding: 8px;
    }

    /* Remove inner white blocks */
    div[data-testid="stDataFrame"] > div {
        background: transparent;
    }

    /* ===== COL3 METRIC BOX ===== */
    .col3-metric {
        text-align: center;
        background: rgba(255, 255, 255, 0); /* same as dataframe */
        padding: 18px;
        border-radius: 12px;
        font-weight: 700;
        color: #6a0dad;  /* purple */
    }

    /* Metric value */
    .col3-metric div[data-testid="stMetricValue"] {
        color: #6a0dad;
        font-weight: 800;
    }

    /* Metric label */
    .col3-metric div[data-testid="stMetricLabel"] {
        color: #6a0dad;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display WITHOUT pandas index
    col1, col2, col3, col4 = st.columns([2, 0.5, 2.0, 0.5])
    with col1:
    # Transparent container with heading inside
        st.markdown(
            f"""
            <div style="
                background: rgba(255, 255, 255, 0); 
                padding: 12px; 
                border-radius: 12px;
            ">
                <div style="
                    font-size: 20px;  /* same as subheader in col3 */
                    font-weight: 600;
                    text-align: center;
                    margin-bottom: 8px;
                ">
                    மாதவாரியான மொத்த சமர்ப்பிப்புகள்
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        month_counts['Submitted'] = month_counts['Submitted'].map(lambda x: f"{x:,}")
        html_table = month_counts.to_html(index=False)

        st.components.v1.html(f"""
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;600&display=swap" rel="stylesheet">

        <style>
        table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 14px;
        }}

        th {{
            background-color: rgba(106, 13, 173, 0.3);  /* #6a0dad */
            padding: 10px;
            text-align: center;
            border: 1px solid rgba(0,0,0,0.15);
            font-weight: 600;
        }}

        td {{
            padding: 10px;
            text-align: center;
            background-color: transparent;
            border: 1px solid rgba(0,0,0,0.15);
        }}

        tr:nth-child(even) {{
            background-color: rgba(0,0,0,0.03);
        }}
        </style>

        {html_table}
        """, height=250, scrolling=False)

    with col3:
        st.title(" ")
        filtered_range_df = filtered_df[(filtered_df['end'] >= start_dt) & (filtered_df['end'] <= end_dt)].copy()
        count_text = f"{len(filtered_range_df):,}"
        date_text = f"{selected_start.strftime('%d-%m-%Y')} → {selected_end.strftime('%d-%m-%Y')}"

        st.components.v1.html(f"""
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;600;700&display=swap" rel="stylesheet">

        <div style="
            text-align:center;
            background: rgba(106, 13, 173, 0.1);
            padding:20px;
            border-radius:14px;
            font-family:'Roboto Condensed', sans-serif;
        ">

            <div style="font-size:18px; font-weight:600; margin-bottom:6px;">
                தேர்ந்தெடுக்கப்பட்ட வரம்பில் உள்ள சமர்ப்பிப்புகள்
            </div>

            <div style="font-size:14px; margin-bottom:10px; opacity:0.85;">
                {date_text}
            </div>

            <div style="font-size:36px; font-weight:700; color:#6a0dad; line-height:1;">
                {count_text}
            </div>

        </div>
        """, height=180, scrolling=False)
        
        if DOB_COL in filtered_df.columns:
            filtered_df[DOB_COL] = pd.to_datetime(filtered_df[DOB_COL], errors="coerce")

# =====================
# DISPLAY TABLE
# =====================
    st.write("கணக்கெடுப்பு தரவு")
    
    @st.cache_data(show_spinner=False)
    def get_display_df(filtered_df):
        df_to_show = filtered_df[[c for c in filtered_df.columns if c not in SYSTEM_COLS]].copy()
        df_to_show.index = df_to_show.index + 1
        return df_to_show

    display_df = get_display_df(filtered_df)
    
    log_user_activity(
        st.session_state.user,
        st.session_state.ngo_name,
        st.session_state.district,
        "Viewed Submissions")
    st.session_state.viewed_submissions_logged = True
    # ---------------------------------
    # Log: Applied Filters (ONLY WHEN USED)
    # ---------------------------------
    if (sel_district and "All" not in sel_district) or (sel_ngo and sel_ngo != []):
        #if "filters_logged" not in st.session_state:
        log_user_activity(
            st.session_state.user,
            st.session_state.ngo_name,
            st.session_state.district,
            "Applied Filters")
        st.session_state.filters_logged = True
            
    # 1️⃣ Prepare filename with timestamp (safe)
    now_str = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    file_name = f"{st.session_state.ngo_name}_submissions ({now_str}).xlsx"
    # Capture session state values
    user = st.session_state.get("user", "unknown")
    ngo_name = st.session_state.get("ngo_name", "unknown")
    district = st.session_state.get("district", "unknown")
    # Make a copy so you don't modify original
    df_to_display = filtered_range_df[[c for c in filtered_range_df.columns if c not in SYSTEM_COLS]].copy()
    # Reset index starting from 1
    df_to_display.reset_index(drop=True, inplace=True)
    df_to_display.index += 1  # Optional: start index at 1 instead of 0
    
    dob_col = "6.பிறந்த தேதி (அடையாள அட்டையின் படி)"
    if dob_col in df_to_display.columns:
        # Ensure it's datetime first
        df_to_display[dob_col] = pd.to_datetime(df_to_display[dob_col], errors="coerce")
        # Format as YYYY-MM-DD (drop time)
        df_to_display[dob_col] = df_to_display[dob_col].dt.strftime("%d-%m-%Y")
    # 2️⃣ Lazy download using a lambda for data
    st.download_button(
        label="⬇️ Download Excel",
        data=lambda: create_excel_bytes(df_to_display, user, ngo_name, district),
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel"
    )

    # --- helper function
    def create_excel_bytes(df, user, ngo_name, district):
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Submissions")
        excel_buffer.seek(0)
        # log download AFTER creating the file
        log_user_activity(
            user,
            ngo_name,
            district,
            "Downloaded Excel"
        )
        return excel_buffer.getvalue()  # return bytes

    st.markdown("""
    <style>
    div[data-testid="stToolbar"] {
        display: none;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df_to_display, use_container_width=True)
    st.caption(f"மொத்த பதிவுகள்: {len(df_to_display)}")   
    # --- Ensure DOB column is datetime AFTER filtering

# =====================
# DASHBOARD PAGE
# =====================
elif page == "Dashboard":
    #st.title("📊 Interactive Dashboard")
    st.markdown(
        "<div style='text-align:center; margin-top:-100px; '><h2 style='font-size:30px; color:#6a0dad'>Interactive Dashboard</h2></div>",
        unsafe_allow_html=True
    )
    st.write("Data for comparison and Findings🔎")
    # =====================
    # PREP DATA (FAST)
    # =====================
    @st.cache_data(show_spinner=False)
    def prep_dashboard_df(df):
        out = df.copy()

        # Ensure dates
        if "end" in out.columns:
            out["end"] = pd.to_datetime(out["end"], errors="coerce")

        if DOB_COL in out.columns:
            out[DOB_COL] = pd.to_datetime(out[DOB_COL], errors="coerce")
            out["age"] = ((pd.Timestamp.today() - out[DOB_COL]).dt.days // 365)
        return out

    district_tn_to_en = {
        "அரியலூர்": "Ariyalur",
        "செங்கல்பட்டு": "Chengalpet",
        "சென்னை": "Chennai",
        "கோயம்புத்தூர்": "Coimbatore",
        "கடலூர்": "Cuddalore",
        "தருமபுரி": "Dharmapuri",
        "திண்டுக்கல்": "Dindigul",
        "ஈரோடு": "Erode",
        "கள்ளக்குறிச்சி": "Kallakurichi",
        "கன்னியாகுமரி":"Kanyakumari",
        "காஞ்சிபுரம்": "Kanchipuram",
        "கரூர்": "Karur",
        "கிருஷ்ணகிரி": "Krishnagiri",
        "மதுரை": "Madurai",
        "மயிலாடுதுறை": "Mayiladuthurai",
        "நாகப்பட்டினம்": "Nagapattinam",
        "நாமக்கல்": "Namakkal",
        "நீலகிரி": "Nilgiris",
        "பெரம்பலூர்": "Perambalur",
        "புதுக்கோட்டை": "Pudukkottai",
        "ராமநாதபுரம்": "Ramanathapuram",
        "ராணிப்பேட்டை": "Ranipet",
        "சேலம்": "Salem",
        "சிவகங்கை": "Sivagangai",
        "தென்காசி": "Tenkasi",
        "தஞ்சாவூர்": "Thanjavur",
        "தேனி": "Theni",
        "தூத்துக்குடி": "Thoothukudi",
        "திருநெல்வேலி": "Tirunelveli",
        "திருப்பத்தூர்": "Tirupathur",
        "திருப்பூர்": "Tiruppur",
        "திருவள்ளூர்": "Tiruvallur",
        "திருவண்ணாமலை": "Tiruvannamalai",
        "திருவாரூர்": "Tiruvarur",
        "திருச்சிராப்பள்ளி": "Tiruchirappalli",
        "வேலூர்": "Vellore",
        "விழுப்புரம்": "Villupuram",
        "விருதுநகர்": "Virudhunagar"
    }
    base_df = prep_dashboard_df(df)
    dash_df = base_df.copy()
    # 🔑 Normalize district names BEFORE any grouping
    dash_df["_District_EN"] = (
        dash_df[DISTRICT_COL]
        .astype(str)
        .str.strip()
        .map(district_tn_to_en)
    )

    # --- Map Tamil → English for districts
    
    #district_vals = ["All"] + sorted(dash_df[DISTRICT_COL].dropna().unique())
    district_vals_en = ["All"] + sorted(district_tn_to_en.values())
    
    reverse_map = {v: k for k, v in district_tn_to_en.items()}
    col1, col2, col3, col4, col5 = st.columns([0.5, 0.1, 1.0, 0.1, 1.0])
    with col3:
        district_vals_en = ["All"] + sorted(district_tn_to_en.values())
        if st.session_state.get("ngo_filter"):   # NGO selected
            districts_with_ngo = df[df[NGO_COL].isin(st.session_state["ngo_filter"])][DISTRICT_COL].dropna().unique().tolist()
            district_vals_en = ["All"] + sorted(district_tn_to_en.get(d, d) for d in districts_with_ngo)
        else:  # No NGO selected → show all districts
            district_vals_en = ["All"] + sorted(district_tn_to_en.values()) 
        sel_district = st.multiselect("Select District(s)",options=district_vals_en, key="district_filters")

# Filter dash_df based on selection (keep reverse map)
        if sel_district and "All" not in sel_district:
            dash_df = dash_df[dash_df[DISTRICT_COL].isin([reverse_map[d] for d in sel_district])]    
    
    # # ---- Handle All
    if sel_district and "All" not in sel_district:
        selected_tamil = [k for k, v in district_tn_to_en.items() if v in sel_district]
        dash_df = dash_df[dash_df[DISTRICT_COL].isin(selected_tamil)]
        #dash_df = dash_df[dash_df[DISTRICT_COL].isin([reverse_map[d] for d in sel_district])]
    #dash_df[DISTRICT_COL] = dash_df[DISTRICT_COL].map(district_tn_to_en).fillna(dash_df[DISTRICT_COL])
    dash_df = dash_df.copy()
    district_vals_en = ["All"] + sorted(district_tn_to_en.values())
    #dash_df["District_EN"] = dash_df[DISTRICT_COL].map(district_tn_to_en)

    if dash_df.empty:
        st.markdown(
            '<div style="padding:20px; border-radius:12px; background:#ffdddd; color:#900; font-weight:700; text-align:center;">'
            '⚠️ Records for the selected district(s) are not available!</div>',
            unsafe_allow_html=True
        )
    else:
# ---- NGO (only actual NGOs, no "All")
        with col3:
            ngo_vals = sorted(dash_df[NGO_COL].dropna().unique().tolist())
            sel_ngo = st.multiselect("Select NGO(s)", ngo_vals, key="ngo_filter")
            if sel_ngo:
                dash_df = dash_df[dash_df[NGO_COL].isin(sel_ngo)]
            else:
                ngo_vals = sorted(df[NGO_COL].dropna().unique().tolist())

        with col3:
        # ---- Age Slider
            if "age" in dash_df.columns and not dash_df["age"].dropna().empty:
                min_age = int(dash_df["age"].dropna().min())
                max_age = int(dash_df["age"].dropna().max())
                if min_age == max_age:
                    st.info(f"Only age available: {min_age}")
                    age_min = age_max = min_age
                else:
                    age_min, age_max = st.slider("Select Age Range",min_value=min_age,max_value=max_age,value=(min_age, max_age))
                dash_df = dash_df[(dash_df["age"] >= age_min) & (dash_df["age"] <= age_max)]
        # ---- Question selector (ANY N)
        #col1, col2, col3 = st.columns([1, 2, 2])
        
        with col5:
            QUESTION_GROUPS = {
                # ---------- MCQ GROUP ----------
                "30.புதிதாக விண்ணப்பிக்க வேண்டிய ஆவணங்கள்?": {
                    "type": "mcq",
                    "prefix": "30.புதிதாக விண்ணப்பிக்க வேண்டிய ஆவணங்கள்?/",
                    "label": "New Documents to be Applied"
                },
                "29.இல்லையெனில் எந்த ஆவணங்கள் புதுப்பிக்கப்பட (அ) திருத்தம் செய்யப்பட வேண்டும்?": {
                    "type": "mcq",
                    "prefix": "29.இல்லையெனில் எந்த ஆவணங்கள் புதுப்பிக்கப்பட (அ) திருத்தம் செய்யப்பட வேண்டும்?/",
                    "label": "Documents to be Updated / Corrected"
                },
                "38.உங்கள் குடும்பத்தில் அதிகம் சம்பாதிக்கும் குடும்ப உறுப்பினரின் பணி வகை?": {
                    "type": "mcq",
                    "prefix": "38.உங்கள் குடும்பத்தில் அதிகம் சம்பாதிக்கும் குடும்ப உறுப்பினரின் பணி வகை?/",
                    "label": "Occupation of highest paid family member"
                },
                # ---------- SINGLE SELECT ----------
                "13.அவர் மாற்றுத்திறனாளியா?": {
                    "type": "single",
                    "label": "PWD"
                },
                "11.சமூகம்": {
                    "type": "single",
                    "label": "Community"
                },
                "57.நீங்கள் நடைபாதை வியாபாரியா?": {
                    "type": "single",
                    "label": "Street Vendor"
                },
                "கணவரை இழந்த (விதவை) பெண்கள் எனில், கணவர் எப்படி இறந்தார்?": {
                    "type": "single",
                    "label": "Widow women's husband death type"
                },
                "37.வறுமை கோட்டு பட்டியல் (Below Poverty Line - BPL), மக்கள் நிலை ஆய்வு பட்டியல் (Participatory Identification of Poor - PIP) ஆகியவற்றில் உங்கள் பெயர் உள்ளதா?": {
                    "type": "single",
                    "label": "Included BPL/PIP"
                },
                "60.உங்களுக்கு சட்டம் சார்ந்த உதவிகள் ஏதேனும் தேவையா?": {
                    "type": "single",
                    "label": "Legal aid required"
                },
                "20.உங்கள் குடும்பத்தில் மூன்றாம் பாலினத்தவர் உள்ளனரா? (உங்களை தவிர்த்து)": {
                    "type": "single",
                    "label": "Any transgender in family"
                }
            }

            OPT_TAM_ENG = {
                "விதவை சான்று" : "Widow certificate",
                "ஆதரவற்ற பெண் சான்று" : "Destitute woman certificate",
                "கணவனால் கைவிடப்பட்டோர் சான்று" : "Abandonment by husband certificate",
                "மணமுறிவு நீதிமன்ற ஆணை" : "Divorce court order",
                "முதிர்கன்னியர் சான்று" : "Unmarried women certificate",
                "குடும்ப அட்டை" : "Ration card",
                "ஆதார் அட்டை" : "Aadhar card",
                "வாக்காளர் அடையாள அட்டை" : "Voter ID card",
                "பான் அட்டை" : "PAN card",
                "தொழிற்சங்க பதிவு அட்டை" : "Trade Union registration card",
                "கல்வித்தகுதி சான்றுகள்" : "Educational qualification certificate",
                "சாதி சான்று" : "Community certificate",
                "வருமான சான்று" : "Income certificate",
                "வாரிசு சான்று" : "Legal Heir certificate",
                "இருப்பிட சான்று" : "Nativity certificate",
                "எதுவும் வேண்டாம்" : "Don't want anything",
                "ஆம்" : "Yes",
                "இல்லை" : "No",
                "தெரியாது" : "Not known",
                "மற்றவை":"Other",
                "விவாசாயம்" : "Farming",
                "சொந்த வேலை(அ)வியாபாரம்" : "Self employment/Business",
                "கூலி வேலை" : "Daily waged employment",
                "தனியார் நிறுவனத்தில் பணி" : "Private company employment",
                "அரசு பணி" : "Government employment",
                "மீன்பிடி வேலை" : "Fishing work",
                "சிறு குறு தொழில்" : "Small-micro enterprises",
                "குடிசை தொழில்" : "Cottage industry",
                "கைத்தொழில்" : "Handicraft",
                "ஒப்பந்த அடிப்படையில் பணி" : "Contractual work",
                "அரசு உதவி தொகை மட்டுமே பெறுபவர்" : "Recipient of only government assistance",
                "தெரியவில்லை" : "Not known",
                "அமைப்புசாரா தொழிலாளர் நல வாரியம்" : "TNUW",
                "மீனவ நல வாரியம்":"Fishers",
                "வேளாண்மை தொடர்புடைய நல வாரிய":"Agri",
                "சுய வேலைவாய்ப்பு":"Self emp.", 
                "ஊதிய வேலைவாய்ப்பு":"Salaried job",
                "தொழில்முனைவோர்":"Entrepreneurship"
            }

            SINGLE_OPT_TAM_ENG = {
                "ஆம்": "Yes",
                "இல்லை": "No",
                "தெரியாது" : "Not known",
                "தெரியவில்லை" : "Not known",
                "மற்றவை":"Other",
                "பட்டியல் சாதியினர் (SC)" : "Scheduled Castes (SC)",
                "பட்டியல் சாதி - அருந்ததியர் (SCA)" : "Scheduled Caste - Arunthathiyar (SCA)",
                "பட்டியல் பழங்குடியினர் (ST)" : "Scheduled Tribes (ST)",
                "மிகவும் பிற்படுத்தப்பட்ட வகுப்பினர் (MBC)" : "Most Backward Classes (MBC)",
                "பிற்படுத்தப்பட்ட வகுப்பினர் (BC)" : "Backward Classes (BC)",
                "இதர பிற்படுத்தப்பட்ட வகுப்பினர் (OBC)" : "Other Backward Classes (OBC)",
                "பொதுப் பிரிவு (General/OC)" : "General (OC)",
                "மீனவ சமூகம் (SC)" : "Fishing Community (SC)",
                "மீனவ சமூகம் (ST)" : "Fishing Community (ST)",
                "மீனவ சமூகம் (MBC)" : "Fishing Community (MBC)",
                "மீனவ சமூகம் (BC)" : "Fishing Community (BC)",
                "உடல் உபாதை" : "Health issue",
                "ஆணவ கொலை" : "Honour killing",
                "விபத்து" : "Accident",
                "மது பழக்கம்" : "Alcohol addiction",
                "கடலில் மீன் பிடிக்கும் போது" : "While fishing in the sea"
            }

            selected_questions = st.multiselect(
                "Select Questions for Analysis",
                list(QUESTION_GROUPS.keys()),
                format_func=lambda q: QUESTION_GROUPS[q]["label"]
            )

            #selected_questions = [display_to_col[d] for d in selected_display]
            # =====================
            # APPLY QUESTION FILTERS (CORRELATION)
            # =====================
            rendered_multi = set()
            for q in selected_questions:
                q_meta = QUESTION_GROUPS[q]
                q_type = q_meta["type"]
                q_label = q_meta["label"]
                
                if q_type == "mcq":
                    prefix = q_meta["prefix"]
                # 🔹 ONLY option columns (0/1)
                    opt_cols = sorted(
                        [c for c in dash_df.columns if c.startswith(prefix)],
                        key=lambda c: OPT_TAM_ENG.get(c.replace(prefix, ""), c.replace(prefix, "")).lower()
                    )

                    if not opt_cols:
                        continue

                    with st.expander(q_label):

                        for opt_col in opt_cols:

                            # Extract option name
                            opt_name = opt_col.replace(prefix, "")
                            opt_label = OPT_TAM_ENG.get(opt_name, opt_name)
                            choice = st.radio(
                                opt_label,
                                ["Both", "Yes", "No"],
                                horizontal=True,
                                key=f"dash_{opt_col}"
                            )

                            if choice == "Yes":
                                dash_df = dash_df[dash_df[opt_col] == 1]
                            elif choice == "No":
                                dash_df = dash_df[dash_df[opt_col] == 0]
                
                elif q_type == "single":

                    col = q
                    raw_vals = sorted(dash_df[col].dropna().unique())

                    if not raw_vals:
                        continue
                    
                    display_map = {
                        SINGLE_OPT_TAM_ENG.get(v, v): v
                        for v in raw_vals
                    }
                    display_map = dict(sorted(display_map.items(), key=lambda x: x[0].lower()))
                    with st.expander(q_label):
                        selected_display = st.multiselect(
                            q_label,
                            list(display_map.keys()),
                            key=f"dash_{col}"
                        )

                        if selected_display:
                            selected_actual = [display_map[d] for d in selected_display]
                            dash_df = dash_df[dash_df[col].isin(selected_actual)]
        with col1:
            st.write("")
            st.markdown(
                f"""
                <div style="
                    background:#6a0dad;
                    color:white;
                    padding:7px;
                    border-radius:12px;
                    text-align:center;
                    font-weight:700;
                    margin-bottom:12px;
                ">
                    <div style="font-size:15px;margin-top:0px;">Records</div>
                    <div style="font-size:25px;margin-top:-10px;">{len(dash_df):,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # NGO Count
            st.markdown(
                f"""
                <div style="
                    background:#6a0dad;
                    color:white;
                    padding:7px;
                    border-radius:12px;
                    text-align:center;
                    font-weight:700;
                    margin-bottom:12px;
                ">
                    <div style="font-size:15px; margin-top:0px; margin-bottom:-5px;">NGOs</div>
                    <div style="font-size:25px; margin-top:-10px;">
                        {dash_df[NGO_COL].nunique(dropna=True)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # District Count
            st.markdown(
                f"""
                <div style="
                    background:#6a0dad;
                    color:white;
                    padding:7px;
                    border-radius:12px;
                    text-align:center;
                    font-weight:700;
                ">
                    <div style="font-size:15px; margin-top:0px;">Districts</div>
                    <div style="font-size:25px; margin-top:-10px;">
                        {dash_df[DISTRICT_COL].nunique(dropna=True)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")
            st.write("")
        # =====================
        # DASHBOARD LAYOUT (3 x 2)
        # =====================
        r1 = st.columns(2)
        r2 = st.columns(2)
        r3 = st.columns(2)
    
        @st.cache_data(show_spinner=False, persist="disk")
        def load_geojson_simplified():
            import json
            with open("tn_districts_simplified.geojson", "r", encoding="utf-8") as f:
                geojson = json.load(f)
            for idx, feature in enumerate(geojson['features']):
                feature['id'] = idx
            return geojson
        geojson_data = load_geojson_simplified()
        @st.cache_data(show_spinner=False, persist="disk")
        def prepare_dashboard_map_df(dash_df, geojson_data):
            
            df_map = (
                dash_df
                .dropna(subset=["_District_EN"])
                .groupby("_District_EN")
                .size()
                .reset_index(name="Count")
            )
        
            features = [{"feature_id": idx, "District": f["properties"]["dist"]} for idx, f in enumerate(geojson_data["features"])]
            full = pd.DataFrame(features)
            full = full.merge(df_map.rename(columns={"_District_EN": "District"}),on="District",how="left")
            full["Count"] = full["Count"].fillna(0)
            return full
        
        full = prepare_dashboard_map_df(dash_df, geojson_data)
            # 🔑 Tamil → English
        
        with r1[0]:
            col1, col2, col3 = st.columns([5, 1, 1])
            try:
                #st.subheader("Tamil Nadu: District-wise Records")
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Tamil Nadu: District-wise Records</h2></div>",
                    unsafe_allow_html=True
                )
                @st.cache_data(show_spinner=False)
                def load_geojson_local():
                    with open("tn_districts_simplified.geojson", "r", encoding="utf-8") as f:
                        geojson = json.load(f)
                    for idx, feature in enumerate(geojson['features']):
                        feature['id'] = idx
                    return geojson
                geojson_data = load_geojson_local()
                
                #map_df = prepare_dashboard_map_df(dash_df, geojson_data)
                custom_scale = [
                    [0, "#ffffff"], # start from white
                    [0.01, "#e0c3f4"],
                       # middle light purple (adjust as you like)
                    [1, "#6a0dad"]       # dark purple at the max
                ]
                fig = px.choropleth_mapbox(
                    full,
                    geojson=geojson_data,
                    locations="feature_id",
                    color="Count",
                    color_continuous_scale=custom_scale,
                    hover_data={'District': True, 'Count': True, 'feature_id': False},
                    mapbox_style="carto-positron",
                    center={"lat": 10, "lon": 80},
                    zoom=5.5,
                    labels={'Count': 'Submissions'}
                )
                fig.update_layout(
                    mapbox={
                        'style': {
                            'version': 8,
                            'sources': {},
                            'layers': []
                        },
                        'domain': {
                            'x': [0.0, 1.0],
                            'y': [0.1, 1.0]
                        }
                    },
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin={"r":0,"t":0,"l":0,"b":0},
                    height=550,
                    coloraxis_colorbar=dict(
                        x=0.6,
                        xanchor='left',
                        len=0.4,
                        thickness=7.5,
                        y=0.6
                    )
                )
                #st.plotly_chart(fig, use_container_width=True)
                components.html(
                    fig.to_html(
                        include_plotlyjs="cdn",
                        full_html=False,
                        config={"displayModeBar": False}
                    ),
                    height=410
                )

            except Exception as e:
                if dash_df.empty:
                    st.warning("No records for selected range")
                    map_df = prepare_empty_map_df(geojson_data)   # ← force map render
                    
                    def prepare_empty_map_df(geojson_data):
                        return pd.DataFrame({
                            "District": [f["properties"]["dist"] for f in geojson_data["features"]],
                            "Count": 0
                        })

        # =====================
        # TN DISTRICT MAP (BAR — MAP READY)
        # =====================
        
            dist_counts = dash_df[NGO_COL].value_counts()

            # =====================
            # DONUT / PIE
            # =====================
            with r2[1]:
                #st.subheader ("Govt. Financial Aid (Pensions)")
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Govt. Financial Aid (Pensions)</h2></div>",
                    unsafe_allow_html=True)
                tam_eng={
                "கணவரை இழந்த (விதவை) பெண்கள் எனில் அதற்கான அரசு நிதி உதவி பெறுகிறார்களா?": "Widow Pension",	
                "கணவரால் கைவிடப்பட்டவர் எனில் அதற்கான அரசு நிதி உதவி பெறுகிறார்களா?": "Destitute Women Aid",
                "தனித்து வாழும் பெண்(கள்) அரசு நிதி உதவி பெறுகிறார்களா?": "Single Women Aid",
                "60 வயதை தாண்டிய பெண்கள் முதியோர் ஓய்வூதியம் பெறுகிறார்களா?": "Old Age Pension",
                "ஆம் எனில், மாற்றுத் திறனாளி(கள்) அரசு நிதி உதவி பெறுகிறார்களா?": "PWD Pension",
                "35.அரசின் மகளிர் உதவித்தொகை பெறுகிறீர்களா?": "Magalir Udhavi Thogai"}

                pension_cols = [col for col in dash_df.columns if col in tam_eng.keys()]
                # pension_df = pd.DataFrame({
                #     "Pension / Aid Type": pension_cols,
                #     "Yes": dash_df[pension_cols].apply(lambda x: (x == "ஆம்").sum(), axis=0).values,
                #     "No": dash_df[pension_cols].apply(lambda x: (x == "இல்லை").sum(), axis=0).values
                # })
                yes_counts = (dash_df[pension_cols] == "ஆம்").sum()
                no_counts  = (dash_df[pension_cols] == "இல்லை").sum()
                pension_df = pd.DataFrame({
                    "Pension / Aid Type": pension_cols,
                    "Yes": yes_counts.values,
                    "No": no_counts.values
                })
                pension_df["Pension / Aid Type"] = pension_df["Pension / Aid Type"].replace(tam_eng)
                pension_df_display = pension_df.copy()
                pension_df_display["Yes"] = pension_df_display["Yes"].apply(lambda x: f"<span>{x}</span>")
                pension_df_display["No"] = pension_df_display["No"].apply(lambda x: f"<span>{x}</span>")
                st.markdown(
                    """
                    <style>
                    .static-table {
                        width: 100% !important;
                        table-layout: fixed;
                    }
                    /* Header alignment */
                    .static-table th:first-child {
                        text-align: left;      /* Column 1 header stays left */
                    }

                    .static-table th:nth-child(2),
                    .static-table th:nth-child(3) {
                        text-align: center;    /* Yes / No headers centered */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    pension_df_display.to_html(index=False, escape=False, classes="static-table"),
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Employment & Welfare Coverage</h2></div>",
                    unsafe_allow_html=True)
                tam_eng1={
                "23.உங்களுக்கு வேலைவாய்ப்பு தேவையா? (தனித்து வாழும் பெண்ணிற்கு)": "Employment required",	
                "22.குடும்ப உறுப்பினர்களின் கல்வித்தகுதி வேலைவாய்ப்பு அலுவலகத்தில் பதியப்பட்டுள்ளதா?": "Employment Registration",
                "ஆம் எனில், குறித்த நேரத்தில் புதுப்பிக்கப்பட்டுள்ளதா?": "Employment Registration Renewal",
                "41.தொழிற்கல்வி மற்றும் பயிற்சி சான்றிதழ் உள்ளதா (VET)?": "Professional/Vocational Education Certificate",
                "42.தொழில் சார்ந்த தனித்திறன் உள்ளதா?": "Professional Skills",
                "45.உங்கள் குடும்பத்திற்கு MGNREGA (நூறுநாள் வேலை) அட்டை உள்ளதா?":"MGNREGA Card",
                "52.நுண்கடன் நிறுவனங்களில் குழுக்கடன் பெற்றுள்ளீர்களா?": "Debt from Micro-finance"}

                pension_cols = [col for col in dash_df.columns if col in tam_eng1.keys()]
                # pension_df = pd.DataFrame({
                #     "Type": pension_cols,
                #     "Yes": dash_df[pension_cols].apply(lambda x: (x == "ஆம்").sum(), axis=0).values,
                #     "No": dash_df[pension_cols].apply(lambda x: (x == "இல்லை").sum(), axis=0).values
                # })
                yes_counts = (dash_df[pension_cols] == "ஆம்").sum()
                no_counts  = (dash_df[pension_cols] == "இல்லை").sum()
                pension_df = pd.DataFrame({
                    "Type": pension_cols,
                    "Yes": yes_counts.values,
                    "No": no_counts.values
                })

                pension_df["Type"] = pension_df["Type"].replace(tam_eng1)
                pension_df_display = pension_df.copy()
                pension_df_display["Yes"] = pension_df_display["Yes"].apply(lambda x: f"<span>{x}</span>")
                pension_df_display["No"] = pension_df_display["No"].apply(lambda x: f"<span>{x}</span>")
                st.markdown(
                    """
                    <style>
                    .static-table {
                        width: 100% !important;
                        table-layout: fixed;
                    }
                    /* Header alignment */
                    .static-table th:first-child {
                        text-align: left;      /* Column 1 header stays left */
                    }

                    .static-table th:nth-child(2),
                    .static-table th:nth-child(3) {
                        text-align: center;    /* Yes / No headers centered */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    pension_df_display.to_html(index=False, escape=False, classes="static-table"),
                    unsafe_allow_html=True
                )
                
                MNREGA_COL = "45.உங்கள் குடும்பத்திற்கு MGNREGA (நூறுநாள் வேலை) அட்டை உள்ளதா?"
                WELFARE_COL = "46.ஏதேனும் நல வாரியங்களின் கீழ் பதிவு உள்ளதா?"
                WELFARE_PREFIX = "ஆம் எனில், சம்பந்தப்பட்ட வாரியத்தின் பெயரை குறிப்பிடவும்/"
                EMP_COL = "23.உங்களுக்கு வேலைவாய்ப்பு தேவையா? (தனித்து வாழும் பெண்ணிற்கு)"
                EMP_PREFIX = "ஆம் எனில், எந்த வகையில்?/"
                #st.subheader("Employment & Welfare Coverage")
                # st.markdown(
                #     "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Employment & Welfare Coverage</h2></div>",
                #     unsafe_allow_html=True
                # )
                PURPLE_YES_NO = ["#6a0dad", "#D1B3E0"]  # deep purple, light purple
                WINE_SCALE = [
                    "#2f2f2f",   # dark charcoal
                    "#6b6b6b",   # medium dark grey
                    "#a8a8a8",   # soft grey
                    "#e0e0e0"    # very light grey
                ]
                pie_col1, pie_col2, pie_col3 = st.columns(3)
                pie_col1, pie_col2, pie_col3 = st.columns([1, 1, 1.2])
                
                with pie_col1:
                    mnrega_counts = (
                        dash_df[MNREGA_COL]
                        .value_counts()
                        .reindex(["ஆம்", "இல்லை"], fill_value=0)
                    )

                    fig_mnrega = px.pie(
                        names=["Yes", "No"],
                        values=mnrega_counts.values,
                        hole=0.6, color_discrete_sequence=PURPLE_YES_NO
                    )

                    fig_mnrega.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=150, margin=dict(t=0, b=20, l=0, r=0)
                    )

                    fig_mnrega.update_traces(
                        textinfo="label",
                        textposition="inside",
                        hovertemplate="<b>%{label}</b><br>Count: %{value}, (%{percent})<extra></extra>"
                    )
                    fig_mnrega.add_annotation(
                        text="MNREGA Availability",
                        x=0.5, y=-0.2,  # y < 0 places it below the chart
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=12, color="black")
                    )
                    #st.plotly_chart(fig_mnrega, use_container_width=True)
                    # st.markdown(
                    #     "<div style='text-align:center; margin-top:-100px; font-size:12px;font-weight:600;'>MNREGA Card Availability </div>",
                    #     unsafe_allow_html=True
                    # )
                    emp_yes_df = dash_df[dash_df[EMP_COL] == "ஆம்"]

                    emp_opt_cols = [
                        c for c in dash_df.columns
                        if c.startswith(EMP_PREFIX)
                    ]

                    if emp_opt_cols and not emp_yes_df.empty:
                        # st.markdown(
                        #     "<div style='text-align:center; margin-bottom:-1000px; font-size:12px;font-weight:600;'>Welfare Board Type</div>",
                        #     unsafe_allow_html=True
                        # )
                        emp_counts = (
                            emp_yes_df[emp_opt_cols]
                            .apply(lambda x: (x == 1).sum())
                            .sort_values(ascending=False)
                        )

                        emp_labels = [
                            OPT_TAM_ENG.get(
                                c.replace(EMP_PREFIX, ""),
                                c.replace(EMP_PREFIX, "")
                            )
                            for c in emp_counts.index
                        ]

                        fig_emp_types = px.pie(
                            names=emp_labels,
                            values=emp_counts.values,
                            hole=0.6, color_discrete_sequence=WINE_SCALE
                        )

                        fig_emp_types.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            height=155, margin=dict(t=15, b=20, l=0, r=0),
                            showlegend=False
                        )

                        fig_emp_types.update_traces(
                            rotation=180, textinfo="label",
                            textposition="inside", textfont=dict(color="black", size=10),insidetextfont=dict(color="white"),
                            marker=dict(line=dict(color="white", width=0)),
                            hovertemplate="<b>%{label}</b><br>Count: %{value} (%{percent})<extra></extra>"
                        )
                        fig_emp_types.add_annotation(
                            text="Required Employment Type",
                            x=0.5, y=-0.2,  # y < 0 places it below the chart
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="black")
                        )
                        st.plotly_chart(fig_emp_types, use_container_width=True)
                    
                with pie_col2:
                    # st.markdown(
                    #     "<div style='text-align:center; margin-bottom:-100px; font-size:12px;font-weight:600;'>Welfare Board Registration </div>",
                    #     unsafe_allow_html=True
                    # )
                    welfare_counts = (
                        dash_df[WELFARE_COL]
                        .value_counts()
                        .reindex(["ஆம்", "இல்லை"], fill_value=0)
                    )

                    fig_welfare = px.pie(
                        names=["Yes", "No"],
                        values=welfare_counts.values,
                        hole=0.6, color_discrete_sequence=PURPLE_YES_NO
                    )

                    fig_welfare.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=150, margin=dict(t=15, b=18, l=20, r=0)
                    )

                    fig_welfare.update_traces(
                        textinfo="label",
                        textposition="inside", #insidetextfont=dict(color="white"),
                        hovertemplate="<b>%{label}</b><br>Count: %{value} (%{percent})<extra></extra>"
                    )
                    fig_welfare.add_annotation(
                        text="Welfare Board Registration",
                        x=0.5, y=-0.2,  # y < 0 places it below the chart
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=12, color="black")
                    )
                    st.plotly_chart(fig_welfare, use_container_width=True)
                    
                with pie_col3:
                    # Filter only Welfare = Yes
                    welfare_yes_df = dash_df[dash_df[WELFARE_COL] == "ஆம்"]

                    welfare_opt_cols = [
                        c for c in dash_df.columns
                        if c.startswith(WELFARE_PREFIX)
                    ]

                    if welfare_opt_cols and not welfare_yes_df.empty:
                        # st.markdown(
                        #     "<div style='text-align:center; margin-bottom:-1000px; font-size:12px;font-weight:600;'>Welfare Board Type</div>",
                        #     unsafe_allow_html=True
                        # )
                        welfare_counts = (
                            welfare_yes_df[welfare_opt_cols]
                            .apply(lambda x: (x == 1).sum())
                            .sort_values(ascending=False)
                        )

                        welfare_labels = [
                            OPT_TAM_ENG.get(
                                c.replace(WELFARE_PREFIX, ""),
                                c.replace(WELFARE_PREFIX, "")
                            )
                            for c in welfare_counts.index
                        ]

                        fig_welfare_types = px.pie(
                            names=welfare_labels,
                            values=welfare_counts.values,
                            hole=0.6, color_discrete_sequence=WINE_SCALE
                        )

                        fig_welfare_types.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            height=155, margin=dict(t=15, b=20, l=0, r=0),
                            showlegend=False
                        )

                        fig_welfare_types.update_traces(
                            rotation=180, textinfo="label",
                            textposition="inside", textfont=dict(color="black", size=12),insidetextfont=dict(color="white"),
                            marker=dict(line=dict(color="white", width=0)),
                            hovertemplate="<b>%{label}</b><br>Count: %{value} (%{percent})<extra></extra>"
                        )
                        fig_welfare_types.add_annotation(
                            text="Welfare Board Type",
                            x=0.5, y=-0.2,  # y < 0 places it below the chart
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=12, color="black")
                        )
                        st.plotly_chart(fig_welfare_types, use_container_width=True)

                
            with r3[1]:
                st.write("")
                #st.write("Contribution %")
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Contribution % from each organisation</h2></div>",
                    unsafe_allow_html=True
                )
                ngo_counts = dash_df[NGO_COL].value_counts().head(6)
                ngo_counts = ngo_counts.sort_values(ascending=False)
                purple_scale = [
                    "#6a0dad",  # darkest
                    "#7c2bb5",
                    "#8e49bd",
                    "#a067c5",
                    "#b285cd",
                    "#c2a3d6"   # lightest
                ]

                fig = px.pie(
                    names=ngo_counts.index,
                    values=ngo_counts.values,
                    hole=0.6,
                    color=ngo_counts.index,
                    color_discrete_sequence=purple_scale[:len(ngo_counts)]
                )
                fig.update_traces(
                    textinfo="none",  # no labels inside donut
                    textposition="inside", insidetextfont=dict(color="white"),
                    texttemplate="<br>%{percent}",
                    #hovertemplate="<b>%{label}</b> — %{value} (%{percent})<extra></extra>",
                    hovertemplate="<b>%{label}</b><br>Contribution: %{value}<extra></extra>",
                    pull=[0.02] * len(ngo_counts)
                )
                fig.add_annotation(
                    text="NGO %<br>Contribution",
                    x=0.5, y=0.5,
                    font=dict(size=14, color="black"),
                    showarrow=False
                )

                fig.update_layout(height=350, showlegend=False, paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig, use_container_width=True)

            # =====================
            # LINE CHART (TIME)
            # =====================
            with r3[0]:
                st.write("")
                #st.write("Submissions Over Time")
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Submissions Over Time</h2></div>",
                    unsafe_allow_html=True
                )
                if "end" in dash_df.columns:
                    ts = dash_df.groupby(dash_df["end"].dt.to_period("M")).size()
                    ts.index = ts.index.to_timestamp()
                    ts = ts.reset_index(name="Count")  # convert to dataframe for Plotly
                    fig = px.line(
                        ts,
                        x="end",
                        y="Count",
                        markers=True,              # dots at each point
                    )

                    # Smooth curve
                    fig.update_traces(line_shape='spline',  # smooth curve
                                    line=dict(color="#6a0dad", width=2),
                                    marker=dict(size=12, color="#6a0dad"))

                    # Transparent background
                    fig.update_layout(
                        template="plotly_white",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='black'),
                        xaxis=dict(title="Period", showgrid=False, showline=True, zeroline=False,         # ⭐ axis line visible
                                    linecolor="black",linewidth=1,ticks="outside", 
                                    tickfont=dict(color="black", size=12), tickcolor="black", 
                                    title_font=dict(color="black"), dtick="M1",
                                    # tickformatstops=[
                                    #     dict(dtickrange=[None, "M1"], value="%d %b %Y"),
                                    #     dict(dtickrange=["M1", None], value="%b %Y"),],
                                    ),
                        yaxis=dict(title="Submission(s)", showgrid=False,
                                    showline=True, zeroline=False,        # ⭐ axis line visible
                                    linecolor="black",
                                    linewidth=0.5,
                                    ticks="outside", tickcolor="black", 
                                    dtick=1000,               # ⭐ EXACTLY 5 ticks
                                    tickfont=dict(color="black", size=12),
                                    title_font=dict(color="black")),
                        margin=dict(l=0, r=0, t=30, b=0),
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with r2[0]:
                required_prefix = "30.புதிதாக விண்ணப்பிக்க வேண்டிய ஆவணங்கள்?/" 
                correction_prefix = "29.இல்லையெனில் எந்த ஆவணங்கள் புதுப்பிக்கப்பட (அ) திருத்தம் செய்யப்பட வேண்டும்?/"

                # Get relevant columns dynamically
                required_cols = [col for col in dash_df.columns if col.startswith(required_prefix)]
                correction_cols = [col for col in dash_df.columns if col.startswith(correction_prefix)]

                tamil_to_english = {
                "விதவை சான்று": "Widow Certificate",
                "ஆதரவற்ற பெண் சான்று": "Destitute Woman Certificate",
                "கணவனால் கைவிடப்பட்டோர் சான்று": "Abandoned by Husband Certificate",
                "மணமுறிவு நீதிமன்ற ஆணை": "Divorce Court Order",
                "முதிர்கன்னியர் சான்று": "Unmarried Certificate",
                "குடும்ப அட்டை": "Ration Card",
                "ஆதார் அட்டை": "Aadhar Card",
                "வாக்காளர் அடையாள அட்டை": "Voter ID Card",
                "பான் அட்டை": "PAN Card",
                "தொழிற்சங்க பதிவு அட்டை": "Trade Union Registration Card",
                "கல்வித்தகுதி சான்றுகள்": "Educational Qualification Certificates",
                "சாதி சான்று": "Community Certificate",
                "வருமான சான்று": "Income Certificate",
                "வாரிசு சான்று": "Legal heir  Certificate",
                "இருப்பிட சான்று": "Residence Certificate",
                "எதுவும் வேண்டாம்": "Not Interested"}

                # Create a summary dataframe for 0-counts
                summary_df = pd.DataFrame({
                    "Documents/Certificates": [col.replace(required_prefix, "") for col in required_cols],
                    "To apply (new)": dash_df[required_cols].apply(lambda x: (x==1).sum(), axis=0).values,
                    "To update": dash_df[correction_cols].apply(lambda x: (x==1).sum(), axis=0).values
                })
                #st.write("Documents Status Summary")
                st.markdown(
                    "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Documents Status Summary</h2></div>",
                    unsafe_allow_html=True
                )
                summary_df["Documents/Certificates"] = summary_df["Documents/Certificates"].replace(tamil_to_english)
                
                st.markdown(
                    """
                    <style>
                    .static-table th {
                        font-size: 14px; font-weight: 550; background-color: rgba(106,13,173,0.1);  /* transparent */
                        text-align: left; padding: 4px 8px;
                    }
                    .static-table td {
                        font-size: 14px; background-color: rgba(106,13,173,0);  /* transparent */
                        text-align: left; padding: 4px 8px;
                    }
                    /* Column 1 already left-aligned */
                    .static-table td:first-child { 
                        text-align: left; 
                    }

                    /* Columns 2 & 3: cell centered but numbers slightly left */
                    .static-table td:nth-child(2),
                    .static-table td:nth-child(3) {
                        text-align: center; vertical-align: top;      /* centers the cell */
                    }

                    /* Numbers inside cells slightly left-of-center */
                    .static-table td:nth-child(2) span,
                    .static-table td:nth-child(3) span {
                        display: inline-block;
                        margin-left: -10px;  /* tweak as needed */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # Wrap numbers in span for left-of-center effect
                summary_df_display = summary_df.copy()
                summary_df_display["To apply (new)"] = summary_df_display["To apply (new)"].apply(lambda x: f"<span>{x}</span>")
                summary_df_display["To update"] = summary_df_display["To update"].apply(lambda x: f"<span>{x}</span>")

                st.markdown(
                    summary_df_display.to_html(index=False, escape=False, classes="static-table"),
                    unsafe_allow_html=True
                )
                # st.markdown(
                #     "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Employment & Welfare Coverage</h2></div>",
                #     unsafe_allow_html=True)
                tam_eng2={
                "கணவரது இறப்புச் சான்றிதழ் உள்ளதா?":"Husband's Death Certificate",
                "53.உங்கள் குடும்ப உறுப்பினர்களில் திருமணமானவர்களுக்கு திருமண பதிவு சான்றிதழ் உள்ளதா?":"Marriage Certificate", 
                "வீட்டில் உள்ள அனைத்து குழந்தைகளுக்கும் பிறப்பு சான்றிதழ் உள்ளதா?":"Child's Birth Certificate"}

                pension_cols = [col for col in dash_df.columns if col in tam_eng2.keys()]
                yes_counts = (dash_df[pension_cols] == "ஆம்").sum()
                no_counts  = (dash_df[pension_cols] == "இல்லை").sum()
                pension_df = pd.DataFrame({
                    "Mandatory Documents": pension_cols,
                    "Yes": yes_counts.values,
                    "No": no_counts.values
                })
                pension_df["Mandatory Documents"] = pension_df["Mandatory Documents"].replace(tam_eng2)
                pension_df_display = pension_df.copy()
                pension_df_display["Yes"] = pension_df_display["Yes"].apply(lambda x: f"<span>{x}</span>")
                pension_df_display["No"] = pension_df_display["No"].apply(lambda x: f"<span>{x}</span>")
                st.markdown(
                    """
                    <style>
                    .static-table {
                        width: 100% !important;
                        table-layout: fixed;
                    }
                    /* Header alignment */
                    .static-table th:first-child {
                        text-align: left;      /* Column 1 header stays left */
                    }

                    .static-table th:nth-child(2),
                    .static-table th:nth-child(3) {
                        text-align: center;    /* Yes / No headers centered */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    pension_df_display.to_html(index=False, escape=False, classes="static-table"),
                    unsafe_allow_html=True
                )
            with r1[1]:
                # Mapping Tamil → English for '11.சமூகம்' categories
                single_women_map = {
                    "கணவரை இழந்தவர்": "Widow",
                    "கணவரால் கைவிடப்பட்டவர்": "Abandoned by husband",
                    "கணவரைப் பிரிந்தவர்": "Separated from husband",
                    "விவாகரத்தானவர்": "Divorced",
                    "45 வயதுக்கு மேற்பட்ட திருமணம் ஆகாத பெண்": "Unmarried (45<)"
                }
	
	
                if "12.தனித்து வாழும் பெண்களின் சரியான வகையை தேர்ந்தெடுக்கவும்?" in dash_df.columns:
                    # Map Tamil to English
                    dash_df["Single_Women_Category"] = dash_df["12.தனித்து வாழும் பெண்களின் சரியான வகையை தேர்ந்தெடுக்கவும்?"].map(single_women_map).fillna(dash_df["12.தனித்து வாழும் பெண்களின் சரியான வகையை தேர்ந்தெடுக்கவும்?"])

                    # Count per category
                    category_counts = dash_df["Single_Women_Category"].value_counts().reset_index()
                    category_counts.columns = ["Category", "Count"]
                    #category_counts = category_counts.sort_values("Category")

                    # Plotly Express bar chart
                    fig = px.bar(
                        category_counts,
                        x="Category",
                        y="Count",
                        text="Count",
                        color_discrete_sequence=["#6a0dad"],  # purple
                    )
                    # Rounded bars + transparent background + dots at top
                    fig.update_traces(
                        marker_line_width=0,
                        marker_line_color='rgba(0,0,0,0)',
                        marker=dict(line=dict(width=0),), width=0.6,
                        textposition='outside', textfont=dict(color="black"),
                        hovertemplate="%{x}<br>Count: %{y}<extra></extra>"
                    )
                    fig.update_layout(height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        bargap=0.35, barcornerradius=30, font=dict(color="black"),
                        xaxis=dict(showgrid=False, showline=True, linecolor='black', linewidth=0.1, ticks="outside", tickcolor="black", tickangle=0, automargin=True, tickfont=dict(color="black", size=12), title=dict(text="Category", font=dict(color="black")),),
                        yaxis=dict(showgrid=False, showline=True, linecolor='black', linewidth=0.1, ticks="outside", tickcolor="black", dtick=1000, tickfont=dict(color="black"), title=dict(text="Submission(s)",  font=dict(color="black")),),
                        #xaxis_title="Category",
                        #yaxis_title="Submission(s)",
                        uniformtext_minsize=11,
                        uniformtext_mode='hide',
                        margin=dict(l=0, r=0, t=20, b=0)
                    )
                    fig.update_xaxes(
                        tickvals=category_counts["Category"],
                        ticktext=[
                            "<br>".join(textwrap.wrap(str(label), width=16))
                            for label in category_counts["Category"]
                        ]
                    )

                    st.write("")
                    #st.subheader("Single Women by Category")
                    st.markdown(
                        "<div style='text-align:left;'><h2 style='font-size:20px; color:#6a0dad'>Single Women by Category</h2></div>",
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for Single Women category.")

# =====================
# USER ACTIVITY PAGE (Admin Only)
# =====================
elif page == "User Activity": 
    log_user_activity(
        st.session_state.user,
        st.session_state.ngo_name,
        st.session_state.district,
        "User Activity Logs"
    )
    # sheet_idul = "1y-m_sSp9Oi8w93YLit9QKamzCel0mYy5JSxV63-i_F0"
    # USER_LOGS_FILE = f"https://docs.google.com/spreadsheets/d/{sheet_idul}/export?format=csv"
    USER_LOGS_FILE = "userlogs.csv"
    if not st.session_state.get("authenticated", False):
        login()
        st.stop()

    if st.session_state.get("role") != "admin":
        st.warning("⚠️ Only admin users can access this page.")
        st.stop()

    st.title("📝 User Activity Logs")
    
    #if "user_logs_df" not in st.session_state:
    if os.path.exists(USER_LOGS_FILE):
        df = pd.read_csv(USER_LOGS_FILE)
        
        df = df.drop(columns=["S.N."], errors="ignore")
    else:
        df = pd.DataFrame(columns=[
            "NGO", "District", "Username",
            "Login at", "Logout at", "Login_DT", "Logout_DT",
            "Event_DT", "Duration (mins)", "Activity"])    

    df["Login_DT"] = pd.to_datetime(
        df.get("Login at"),
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    )
    df["Logout_DT"] = pd.to_datetime(
        df.get("Logout at"),
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    )
    df["Event_DT"] = pd.to_datetime(df.get("Event_DT"), errors="coerce")

    #st.session_state.user_logs_df = df    
    #df = st.session_state.user_logs_df.copy()  
    df = df.copy()
    df["Login_DT"] = pd.to_datetime(
        df["Login at"],
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    ).dt.tz_localize("Asia/Kolkata")

    df["Logout_DT"] = pd.to_datetime(
        df["Logout at"],
        format="%d-%b-%Y@%I:%M:%S%p",
        errors="coerce"
    ).dt.tz_localize("Asia/Kolkata")

    df["Event_DT"] = pd.to_datetime(
        df["Event_DT"],
        errors="coerce"
    ).dt.tz_localize("Asia/Kolkata")
                        
    # Apply UTC+5:30 offset for Azure deployment
    # time_delta = pd.Timedelta(hours=5, minutes=30)
    # df["Login_DT"] = pd.to_datetime(df["Login_DT"], errors="coerce") + time_delta
    # df["Logout_DT"] = pd.to_datetime(df["Logout_DT"], errors="coerce") + time_delta
    # df["Event_DT"] = pd.to_datetime(df["Event_DT"], errors="coerce") + time_delta
    #df["Event_Date"] = df["Event_DT"].dt.date
    # Filters
    col1, col2, col3, col4, col5, col6 = st.columns([0.8,0.8,0.8,0.5,0.5,0.5])
    with col1:
        district_list = sorted(df['District'].dropna().unique().tolist())
        if "All" not in district_list:
            district_list = ["All"] + district_list
        selected_district = st.selectbox("Filter by District", district_list)
        #selected_district = st.selectbox("Filter by District",["All"]+sorted(df['District'].dropna().unique().tolist()))
    with col2:
        if selected_district == "All":
            ngos_options = ["All"] + sorted(df['NGO'].dropna().unique())
        else:
            ngos_options = ["All"] + sorted(df[df["District"]==selected_district]["NGO"].dropna().unique())
        selected_ngo = st.selectbox("Filter by NGO", ngos_options)
        #selected_ngo = st.selectbox("Filter by NGO", ["All"] + sorted(df['NGO'].dropna().unique().tolist()))
    
    with col3:
        selected_user = st.selectbox("Filter by User", ["All"] + sorted(df['Username'].dropna().unique().tolist()))
    with col4:
        #selected_act = st.selectbox("Filter by Activity", ["All"] + sorted(df['Activity'].dropna().unique().tolist()))
        activity_options = ["All"] + sorted(df['Activity'].dropna().unique().tolist())
        default_index = activity_options.index("Login") if "Login" in activity_options else 0
        selected_act = st.selectbox("Filter by Activity", activity_options, index=default_index)

    with col5:
        start_date = st.date_input("Start Date", datetime.today() - timedelta(days=30))
    with col6:
        end_date = st.date_input("End Date", datetime.today())

    logs_df = df.copy()
    # Convert date inputs to datetime at midnight for safe comparison
    #start_dt = pd.to_datetime(start_date)
    #end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    start_dt = pd.Timestamp(start_date, tz="Asia/Kolkata")
    end_dt = (
        pd.Timestamp(end_date, tz="Asia/Kolkata")
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )
    if "Event_DT" not in df.columns:
        df["Event_DT"] = pd.NaT

    df.loc[df["Event_DT"].isna() & df["Login_DT"].notna(), "Event_DT"] = df["Login_DT"]
    df.loc[df["Event_DT"].isna() & df["Logout_DT"].notna(), "Event_DT"] = df["Logout_DT"]
    
    #df["Event_DT"] = pd.to_datetime(df["Event_DT"], errors="coerce")
    
    # logs_df = df[
    #     df["Event_DT"].notna() &
    #     (df["Event_DT"] >= start_dt) &
    #     (df["Event_DT"] <= end_dt)
    # ]
    # logs_df = pd.concat([logs_df,df[df["Activity"] == "Evidence Upload"]], ignore_index=True)
    logs_df = df.copy()
    if selected_district != "All":
        logs_df = logs_df[logs_df["District"]==selected_district]
    if selected_ngo != "All":
        logs_df = logs_df[logs_df["NGO"]==selected_ngo]
    if selected_user != "All":
        logs_df = logs_df[logs_df["Username"]==selected_user]
    # if selected_act != "All":
    #if selected_act == "Login":
    if selected_act != "All":
        logs_df = logs_df[logs_df["Activity"] == selected_act]
    # elif selected_act == "All":
    #     logs_df = df.copy()
    # else:
    #     logs_df = df[df["Activity"] == selected_act]
    logs_df = logs_df[
        ((logs_df["Event_DT"].notna() & (logs_df["Event_DT"] >= start_dt) & (logs_df["Event_DT"] <= end_dt)) |
        (logs_df["Event_DT"].isna()))
    ]
    #logs_df["Login_DT"] = pd.to_datetime(logs_df["Login_DT"], errors="coerce")
    #logs_df["Logout_DT"] = pd.to_datetime(logs_df["Logout_DT"], errors="coerce")

    mask = logs_df["Activity"] == "Login"

    logs_df.loc[mask, "Duration (mins)"] = (
        (logs_df.loc[mask, "Logout_DT"] - logs_df.loc[mask, "Login_DT"])
        .dt.total_seconds().div(60).round(2)
    )

    logs_df = logs_df[
        (logs_df["Logout_DT"].isna()) | 
        (logs_df["Logout_DT"] >= logs_df["Login_DT"])
    ]

    # ------------------------
    # DISPLAY TABLE
    # ------------------------
    if not logs_df.empty:
        logs_df_display = logs_df.reset_index(drop=True)
        if "S.N." in logs_df_display.columns:
            logs_df_display = logs_df_display.drop(columns=["S.N."])
        # ✅ INSERT FRESH SERIAL NUMBER
        logs_df_display.insert(0, "S.N.", logs_df_display.index + 1)

        logs_df_display["Login at"] = logs_df_display["Login_DT"].dt.strftime("%d-%b-%Y@%I:%M:%S%p")
        logs_df_display["Logout at"] = logs_df_display["Logout_DT"].dt.strftime("%d-%b-%Y@%I:%M:%S%p")
        logs_df_display["Date"] = logs_df["Event_DT"].dt.strftime("%d-%b-%Y %I:%M %p")
        logs_df_display["Activity Time"] = logs_df_display["Event_DT"].dt.strftime(
            "%d-%b-%Y@%I:%M:%S%p"
        )
        logs_df_display["Event TL"] = logs_df_display["Event_DT"].dt.strftime("%I:%M:%S %p")
        logs_df_display = logs_df_display[[
            "S.N.",
            "NGO",
            "District",
            "Username",
            "Activity",
            "Login at",
            #"Logout at",
            #"Duration (mins)",
            "Event TL"
        ]]

        st.markdown("""
        <style>
        /* Container */
        .transparent-table-container {
            background: rgba(0, 0, 0, 0);  /* 30% transparent */
            border-radius: 12px;
            padding: 8px;
            overflow-x: auto; /* scrollable if wide */
        }

        /* Table styling */
        table.transparent-table {
            width: 100%;
            border-collapse: collapse;
        }
        table.transparent-table th {
            background-color: rgba(155, 89, 182, 0.9);  /* slightly transparent purple */
            color: white;
            font-weight: 600;
            text-align: center;
            padding: 6px;
        }
        table.transparent-table td {
            background-color: rgba(216, 182, 255, 0.4); /* light purple + transparency */
            text-align: center;
            padding: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Convert dataframe to HTML table without pandas inline styles
        html_table = logs_df_display.to_html(index=False, classes="transparent-table", border=0, escape=False)

        st.markdown(f'<div class="transparent-table-container">{html_table}</div>', unsafe_allow_html=True)
    else:
        st.info("No user activity records found for the selected filters.")
    
    #csv_df = pd.read_csv(USER_LOGS_FILE)
    
#------------------------------------------------------
#Entitlements page
elif page == "Entitlements":
    st.markdown(
        "<div style='text-align:center; margin-top:-100px; '><h2 style='font-size:30px; color:#6a0dad'>Entitlements Status</h2></div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <style>
    .ticker-wrapper {
        width: 100%;
        overflow: hidden;
        background: rgba(106, 13, 173, 0.1);
        border-radius: 8px;
        padding: 8px 0;
    }

    .ticker-text {
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: ticker 30s linear infinite;
        font-weight: 600;
        color: #6a0dad;
        font-size: 16px;
    }
    .ticker-text:hover {
        animation-play-state: paused;
    }
    @keyframes ticker {
        0%   { transform: translateX(0%); }
        100% { transform: translateX(-100%); }
    }
    </style>

    <div class="ticker-wrapper">
        <div class="ticker-text">
            📢 Welcome to SWAN Status Portal — We are currently conducting SWAN (Social & Community Level Impact) Survey across various districts of Tamil Nadu — 🚀 Application Tracking is NOT yet officially launched — ⚠️ Data currently displayed here is temporary test data used for system validation and performance testing — 📊 Official tracking announcement will be made soon — Thank you for your cooperation and continued support!
        </div>
    </div>
    """, unsafe_allow_html=True)
    #st.write("Currently Test Data Processed, wait until official tracking announcement")
    sheet_link = "https://docs.google.com/spreadsheets/d/1dlxiNuYJlaBv5BSpeBzZmuPDgcMUNsSBSB8DrKkNNp8/edit?usp=sharing"
    sheet_id = "1dlxiNuYJlaBv5BSpeBzZmuPDgcMUNsSBSB8DrKkNNp8"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    #df = pd.read_csv(sheet_url)
    #start = time.time()
    df = pd.read_csv(sheet_url)
    #st.write("Sheet loaded in", time.time() - start, "seconds")
    #st.dataframe(df, use_container_width=True, hide_index=True)
    # Clean column names (VERY IMPORTANT for Google Sheets)
    df.columns = df.columns.str.strip()
    
    # Build summary
    #start = time.time()
    summary_df = (df.groupby(["District", "NGO", "Status"]).size().unstack(fill_value=0).reset_index())
    #st.write("Summary grouped in", time.time() - start, "seconds")
    summary_df.columns.name = None 
    # Guarantee required columns
    if "Applied" not in summary_df.columns:
        summary_df["Applied"] = 0

    if "Received" not in summary_df.columns:
        summary_df["Received"] = 0

    # Flat clean dataframe (VERY IMPORTANT)
    table_df = summary_df[["District", "NGO", "Applied", "Received"]].copy()
    table_df = table_df.reset_index(drop=True)

    table_df.insert(0, "#", range(1, len(table_df) + 1))
    # Ensure numeric safety
    table_df["Applied"] = pd.to_numeric(table_df["Applied"], errors="coerce").fillna(0)
    table_df["Received"] = pd.to_numeric(table_df["Received"], errors="coerce").fillna(0)

    total_applied = int(table_df["Applied"].sum())
    total_received = int(table_df["Received"].sum())

    # Append totals row
    table_df.loc[len(table_df)] = [
        "",                 # Serial number
        "TOTAL",            # District column
        "",                 # NGO column
        total_applied,
        total_received
    ]
    col1, col2 = st.columns([1.5, 1])
    with col1:
        table_df = pd.DataFrame(table_df.values, columns=table_df.columns)

        # Convert to HTML
        table_html = table_df.to_html(index=False, classes="entitlements-table")

        # Render via components (bypasses Streamlit HTML quirks)
        components.html(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;500;600&display=swap');

            .entitlements-table {{
                width: auto;
                display: inline-table;
                border-collapse: collapse;
                font-family: 'Roboto Condensed', sans-serif;
                font-size: 14px;
                color: #222;
            }}

            /* Header row (very light grey / lavender tone) */
            .entitlements-table th {{
                background-color: rgba(106,13,173,0.1);
                font-weight: 600;
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                text-align: left; vertical-align: top;
            }}

            /* Body cells */
            .entitlements-table td {{
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                font-weight: 400;
            }}

            /* Center numeric columns */
            .entitlements-table th:nth-child(1),
            .entitlements-table th:nth-child(4),
            .entitlements-table th:nth-child(5),
            .entitlements-table td:nth-child(1),
            .entitlements-table td:nth-child(4),
            .entitlements-table td:nth-child(5) {{
                text-align: center; vertical-align: top;
            }}
            /* Center 2nd columns */
            .entitlements-table td:nth-child(2) {{
                text-align: left; vertical-align: top;
            }}
            /* Total row */
            .entitlements-table tr:last-child {{
                font-weight: 600;
                background-color: rgba(106,13,173,0.05);
            }}
            </style>

            {table_html}
            """,
            height=350,
            scrolling=True
        )
    with col2:
        @st.cache_data(show_spinner=False)
        def load_map(df):

            with open("tn_districts_simplified.geojson", "r", encoding="utf-8") as f:
                geojson = json.load(f)

            for idx, feature in enumerate(geojson["features"]):
                feature["id"] = idx

            received_counts = (
                df[df["Status"] == "Received"]
                .groupby("District")
                .size()
                .reset_index(name="Total Received")
            )
            
            features = []

            for idx, feature in enumerate(geojson["features"]):
                district_name = feature["properties"]["dist"]

                total = received_counts.loc[
                    received_counts["District"] == district_name,
                    "Total Received"
                ]

                features.append({
                    "feature_id": idx,
                    "District": district_name,
                    "Total Received": int(total.iloc[0]) if len(total) else 0
                })
            return geojson, pd.DataFrame(features)

        geojson, map_df = load_map(df)

        fig = px.choropleth_mapbox(
            map_df,
            geojson=geojson,
            locations="feature_id",
            color="Total Received",
            color_continuous_scale=[
                [0, "#ffffff"],
                [0.01, "#e0c3f4"],
                [1, "#6a0dad"]
            ],
            hover_data={'District': True, 'Total Received': True, 'feature_id': False},
            mapbox_style="carto-positron",
            center={"lat": 10, "lon": 80},
            zoom=5,
            labels={'Total Received': 'Received'}
        )
        fig.update_layout(
            mapbox={
                'style': {'version': 8,'sources': {},'layers': []},
                'domain': {'x': [0.0, 1.0],'y': [0.0, 1.0]}},
            paper_bgcolor='rgba(0,0,0,0)',
            margin={"r":0,"t":0,"l":0,"b":0},
            height=350,
            #autosize=True, font=dict(color="black"),
            coloraxis_colorbar=dict(
                x=0.6,y=0.6,xanchor='left',len=0.5,thickness=6,
                tickfont=dict(color="black", size=12),   # ⭐ ticks
                title=dict(text="Received", font=dict(color="black")),          # ⭐ title
                outlinecolor="black", outlinewidth=0.7
            ))
        components.html(
            fig.to_html(
                include_plotlyjs="cdn",
                full_html=False,
                config={"displayModeBar": False}
            ),
            height=350
        )
        #st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})  
    st.markdown("<div style='text-align:center; margin-top:-80px; margin-bottom:0px;'><h2 style='font-size:20px; color:#6a0dad'>Entitlements Summary</h2></div>", unsafe_allow_html=True)
    
    #filter_col1, filter_col2, filter_col3 = st.columns([1, 1.5, 0.4])
    #with filter_col1:
    st.markdown("""
    <style>
    /* Target checkbox label text */
    div[data-testid="stCheckbox"] label p {
        font-size: 15px !important;   /* h2 size */
        font-weight: 600 !important;
        color: #6a0dad !important;
    }
    </style>
    """, unsafe_allow_html=True)
    col_a, col_b, col_c, col_d, col_e= st.columns([1,1,0.3,0.3,0.3])
    with col_c:
        st.write(" ")
        st.write(" ")
        applied_sel = st.checkbox("Applied", value=True)
    with col_d:
        st.write(" ")
        st.write(" ")
        received_sel = st.checkbox("Received", value=True)

    # Build list of selected statuses
    status_selected = []
    if applied_sel:
        status_selected.append("Applied")
    if received_sel:
        status_selected.append("Received")

    # If none selected, show all (optional behavior)
    if not status_selected:
        status_selected = ["Applied", "Received"]

    with col_a:
        applied_filter = st.selectbox(
            "Document Type",
            ["All"] + sorted(df["Applied for"].dropna().unique())
        )
        # Only show categories for the selected document
        if applied_filter == "All":
            categories = ["All"] + sorted(df["Category"].dropna().unique())
        else:
            categories = ["All"] + sorted(df[df["Applied for"] == applied_filter]["Category"].dropna().unique())
    with col_b:
        category_filter = st.selectbox(
            "Subtype",
            categories
        )
    filter_col1, filter_col2 = st.columns([1,2])    
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df["Status"].isin(status_selected)]
    if applied_filter != "All":
        filtered_df = filtered_df[filtered_df["Applied for"] == applied_filter]

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]   
    district_summary = (filtered_df.groupby(["District", "Status"]).size().unstack(fill_value=0).reset_index() )

    district_summary.columns.name = None

    if "Applied" not in district_summary.columns:
        district_summary["Applied"] = 0

    if "Received" not in district_summary.columns:
        district_summary["Received"] = 0

    district_summary = district_summary[["District", "Applied", "Received"]]
    # ✅ SERIAL NUMBER COLUMN
    district_summary = district_summary.reset_index(drop=True)
    district_summary.insert(0, "#", range(1, len(district_summary) + 1))
    
    total_applied = int(district_summary["Applied"].sum())
    total_received = int(district_summary["Received"].sum())

    district_summary.loc[len(district_summary)] = [
        "", "TOTAL",
        total_applied,
        total_received
    ]
    with filter_col1:
        summary_html = district_summary.to_html(index=False, classes="entitlements-table")
        # Number of rows in the table (including TOTAL)
        row_count = len(district_summary)

        # Approximate heights (px)
        row_height = 50    # height per row (adjust if your CSS padding changes)
        header_height = 40 # header row
        max_height = 500   # maximum table height

        # Compute table height
        table_height = min(header_height + row_count * row_height, max_height)
        components.html(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;500;600&display=swap');

            .entitlements-table {{
                width: auto;
                display: inline-table;
                border-collapse: collapse;
                font-family: 'Roboto Condensed', sans-serif;
                font-size: 14px;
                color: #222;
            }}

            .entitlements-table th {{
                background-color: rgba(106,13,173,0.1);
                font-weight: 600;
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                text-align: left;
            }}

            .entitlements-table td {{
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                font-weight: 400;
            }}

            /* Center serial + numeric columns */
            .entitlements-table th:nth-child(1),
            .entitlements-table th:nth-child(3),
            .entitlements-table th:nth-child(4),
            .entitlements-table td:nth-child(1),
            .entitlements-table td:nth-child(3),
            .entitlements-table td:nth-child(4) {{
                text-align: center;
            }}

            .entitlements-table tr:last-child {{
                font-weight: 600;
                background-color: rgba(106,13,173,0.05);
            }}
            </style>

            {summary_html}
            """,
            height=table_height,
            scrolling=True
        )
        
    
    with filter_col2:
    # --- Document-wise summary table ---
    # Make sure 'Category' is truly blank, not NaN or None
        filtered_df["Category"] = filtered_df["Category"].replace({None: "", "nan": ""}).fillna("")
        doc_summary = (
            filtered_df.groupby(["Applied for", "Category", "Status"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        doc_summary.columns.name = None

        # Guarantee required columns
        if "Applied" not in doc_summary.columns:
            doc_summary["Applied"] = 0
        if "Received" not in doc_summary.columns:
            doc_summary["Received"] = 0

        # Keep only required columns
        doc_summary = doc_summary[["Applied for", "Category", "Applied", "Received"]]

        # Add serial number
        doc_summary = doc_summary.reset_index(drop=True)
        doc_summary.insert(0, "#", range(1, len(doc_summary) + 1))

        # Add totals row
        total_applied = int(doc_summary["Applied"].sum())
        total_received = int(doc_summary["Received"].sum())

        #doc_summary.loc[len(doc_summary)] = ["", "TOTAL", total_applied, total_received]
        doc_summary.loc[len(doc_summary)] = ["", "TOTAL", "", total_applied, total_received]
        # Render as HTML table
        doc_html = doc_summary.to_html(index=False, classes="entitlements-table")
        row_count = len(doc_summary)

        # Approximate heights (px)
        row_height = 50    # height per row (adjust if your CSS padding changes)
        header_height = 40 # header row
        max_height = 500   # maximum table height

        # Compute table height
        table_height = min(header_height + row_count * row_height, max_height)
        components.html(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;500;600&display=swap');

            .entitlements-table {{
                width: auto;
                display: inline-table;
                border-collapse: collapse;
                font-family: 'Roboto Condensed', sans-serif;
                font-size: 14px;
                color: #222;
            }}

            .entitlements-table th {{
                background-color: rgba(106,13,173,0.1);
                font-weight: 600;
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                text-align: left;
            }}

            .entitlements-table td {{
                padding: 10px 12px;
                border: 1px solid #e0e0e0;
                font-weight: 400;
            }}

            /* Center serial + numeric columns */
            .entitlements-table th:nth-child(1),
            .entitlements-table th:nth-child(3),
            .entitlements-table th:nth-child(4),
            .entitlements-table th:nth-child(5),
            .entitlements-table td:nth-child(1),
            .entitlements-table td:nth-child(3),
            .entitlements-table td:nth-child(4),
            .entitlements-table td:nth-child(5) {{
                text-align: center;
            }}

            .entitlements-table tr:last-child {{
                font-weight: 600;
                background-color: rgba(106,13,173,0.05);
            }}
            </style>

            {doc_html}
            """,
            height=table_height,
            scrolling=True
        )
    st.markdown("<div style='text-align:center; margin-top:-50px; margin-bottom:20px;'><h2 style='font-size:20px; color:#6a0dad'>Entitlements Overall Glance</h2></div>", unsafe_allow_html=True)
    chart_col1, chart_col2= st.columns([1.5,1])
    with chart_col1:
        #filtered_df["Category"] = filtered_df["Category"].fillna("Unknown")
        filtered_df["Category"] = filtered_df["Category"].replace({None: "", "nan": ""}).fillna("")
        chart_df = (
            filtered_df.groupby(["Applied for", "Category"])
            .size()
            .reset_index(name="Count")
        )
        
        fig_docs = px.bar(
            chart_df,
            y="Applied for",
            x="Count",
            color="Category",
            orientation="h",
            barmode="stack",

            # ✅ Light → Dark Purple Scale
            color_discrete_sequence=[
                "#d6bdf0",
                "#b993e6",
                "#9f6ad9",
                "#6a0dad"   # darkest
            ],

            # labels={
            #     "Applied for": "Document Type",
            #     "Count": "Applications",
            #     "Category": "Subtype"
            # }, hover_data={"Category": False}
        )
        doc_count = chart_df["Applied for"].nunique()
        fig_height = max(180, doc_count * 30)  
        # 30px per bar → nice thin look
        # max() prevents tiny chart when few rows
        
        fig_docs.update_layout(
            # ✅ Transparent Background
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            # ✅ All Fonts Black
            font=dict(color="black"),
            # ✅ Hide Legend
            showlegend=False,
            # ✅ Prevent huge vertical spacing
            #height=max(320, len(chart_df["Applied for"].unique()) * 28),
            height=fig_height,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        # ✅ Make bars medium-thin
        fig_docs.update_traces(
            hovertemplate="%{x}", marker_line_width=0,
        )

        fig_docs.update_yaxes(
            tickfont=dict(color="black")
        )

        fig_docs.update_xaxes(
            tickfont=dict(color="black")
        )
        
        st.plotly_chart(fig_docs, use_container_width=True)
    with chart_col2:
    # Aggregate counts for Applied and Received based on filtered_df
        status_counts = (
            filtered_df["Status"]
            .value_counts()
            .reindex(["Applied", "Received"], fill_value=0)
            .reset_index()
        )
        status_counts.columns = ["Status", "Count"]

        # Define colors
        colors = ["#d6bdf0", "#6a0dad"]  # Applied = light purple, Received = dark purple

        # Donut chart
        fig_donut = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.6,  # makes it donut
            color="Status",
            color_discrete_map={"Applied": colors[0], "Received": colors[1]},
        )
        counts = status_counts.set_index("Status")["Count"]
        nonzero_counts = counts[counts > 0]
        if len(nonzero_counts) <= 1:
            rotation_angle = 0
        else:
            # smaller slice
            smaller = nonzero_counts.min()
            total = nonzero_counts.sum()
            # rotation to visually center smaller slice
            rotation_angle = (360 * smaller / total) / 2
            # optional: cap at 25 deg max for very small slices
            rotation_angle = min(rotation_angle, 25)
    
        # Show counts inside slices, hide hover
        fig_donut.update_traces(
            text=status_counts.apply(lambda row: f"{row['Status']}: {row['Count']}", axis=1),
            textinfo="text",
            textposition="inside",  # inside by default
            insidetextorientation="auto",
            hoverinfo="skip", 
            hovertemplate=None,
            textfont_size=12, rotation=rotation_angle
        )

        # Layout adjustments
        fig_donut.update_layout(
            showlegend=False, height=fig_height,
            margin=dict(l=10, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, use_container_width=True)
#---- Add New Users Page   
elif selected == "Add New Users" and st.session_state.get("role") == "admin":
    st.markdown("<div style='text-align:center; margin-top:-100px; margin-bottom:0px;'><h2 style='font-size:30px; color:#6a0dad'>➕ Add New NGO User</h2></div>", unsafe_allow_html=True)
    USER_FILE = "user.xlsx"
    district_codes = {
        "Ariyalur": "alu",
        "Chengalpet": "cgl",
        "Chennai": "mas",
        "Coimbatore": "cbe",
        "Cuddalore": "cdl",
        "Dharmapuri": "dpj",
        "Dindigul": "ddg",
        "Erode": "erd",
        "Kallakurichi": "kkr",
        "Kanchipuram": "kcp",
        "Kanyakumari": "knk",
        "Karur": "krr",
        "Krishnagiri": "knj",
        "Madurai": "mdu",
        "Mayiladuthurai": "mld",
        "Nagapattinam": "ngt",
        "Namakkal": "nmk",
        "Nilgiris": "uam",
        "Perambalur": "prb",
        "Pudukkottai": "pdk",
        "Ramanathapuram": "rmd",
        "Ranipet": "rpt",
        "Salem": "sal",
        "Sivagangai": "svg",
        "Tenkasi": "tsi",
        "Thanjavur": "tjv",
        "Theni": "tni",
        "Thoothukudi": "tut",
        "Tirunelveli": "ten",
        "Tirupathur": "tpt",
        "Tiruppur": "tup",
        "Tiruvallur": "trl",
        "Tiruvannamalai": "tnm",
        "Tiruvarur": "tvr",
        "Tiruchirappalli": "tpj",
        "Vellore": "vlr",
        "Villupuram": "vlm",
        "Virudhunagar": "vpt",
        "Puducherry": "pdy",
        "Karaikkal": "kik"
    }

    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def get_next_userid(district, dcode):
        df = pd.read_excel(USER_FILE)

        district_users = df[df["District"] == district]

        if district_users.empty:
            return f"{dcode}001"

        existing_ids = district_users["UserID"].str.replace(dcode, "", regex=False)
        max_num = existing_ids.astype(int).max()
        return f"{dcode}{max_num + 1:03}"

    def fix_unhashed_passwords(file_path):
        df = pd.read_excel(file_path)
        updated = False
        for i, row in df.iterrows():
            pw = str(row['Password']).strip()
            if not pw.startswith("$2b$"):  # not hashed yet
                df.at[i, 'Password'] = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
                updated = True
        if updated:
            df.to_excel(file_path, index=False)
            print("✅ Unhashed passwords fixed")

    role = st.selectbox("Select Role", ["user", "admin"])
    district = st.selectbox("Select District", list(district_codes.keys()))
    ngo_name = st.text_input("NGO Name")
    
    if district:
        dcode = district_codes[district]
        auto_userid = get_next_userid(district, dcode)
        auto_password = f"{auto_userid.capitalize()}@swan"
        
        st.markdown("<div style='text-align:center; margin-top:0px; margin-bottom:0px;'><h2 style='font-size:20px; color:#6a0dad'>🔹Suggestion (Editable)</h2></div>", unsafe_allow_html=True)
        
        userid = st.text_input("UserID", value=auto_userid)
        password = st.text_input("Password", value=auto_password)
        active = st.selectbox("Active Status", [1, 0])

        if st.button("Create User"):
            log_user_activity(
                st.session_state.user,
                st.session_state.ngo_name,
                st.session_state.district,
                "Added User(s)"
            )
            df = pd.read_excel(USER_FILE)

            if userid in df["UserID"].values:
                st.error("UserID already exists!")
            else:
                #hashed_pw = hash_password(password)
                #hashed_pw = str(hashed_pw).replace("\n", "").replace("\r", "").strip()
                # --- Auto serial number ---
                serials = pd.to_numeric(df["#"], errors="coerce").fillna(0)
                next_serial = int(serials.max()) + 1 if not serials.empty else 1
                
                new_row = {
                    "#": next_serial,
                    "Role": role,
                    "District": district,
                    "NGO": ngo_name,
                    "UserID": userid,
                    "Password": password,
                    "Active": active
                }
                
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                columns_in_order = ["#", "Role", "District", "NGO", "UserID", "Password", "Active"]
                df = df[columns_in_order]
                df.to_excel(USER_FILE, index=False)
                fix_unhashed_passwords(USER_FILE)
                df_new = pd.read_excel(USER_FILE)
                st.success(f"User {userid} created successfully with serial {next_serial}!")
                
        if st.button("💥Refresh app and user data!"):
            log_user_activity(
                st.session_state.user,
                st.session_state.ngo_name,
                st.session_state.district,
                "Refreshed Users"
            )
        # Clear all session state keys
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Clear Streamlit caches
            st.cache_data.clear()
            st.cache_resource.clear()
            # Clear users_df if stored in session
            if "users_df" in st.session_state:
                del st.session_state["users_df"]
            # Set a flag to indicate full reset
            st.session_state.reset_done = True
            # Rerun the app
            st.rerun()
        #st.write("DEBUG:", st.session_state.get("user"), st.session_state.get("role"), st.session_state.get("district"))
                     
elif selected == "Manage Users" and st.session_state.get("role") == "admin" and st.session_state.get("user") == "hrfadmin":
    if not st.session_state.get("authenticated", False):
        login()
        st.stop()  # stop until user logs in
    log_user_activity(
        st.session_state.user,
        st.session_state.ngo_name,
        st.session_state.district,
        "Manage User Page"
    )
    st.markdown("<div style='text-align:center; margin-top:-100px; margin-bottom:0px;'><h2 style='font-size:30px; color:#6a0dad'>👥 Manage Users</h2></div>", unsafe_allow_html=True)
    df = pd.read_excel(USER_FILE)
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button("Save Changes"):
        log_user_activity(
            st.session_state.user,
            st.session_state.ngo_name,
            st.session_state.district,
            "Changes in Users"
        )
        edited_df.to_excel(USER_FILE, index=False)
        st.success("Changes saved successfully!")



