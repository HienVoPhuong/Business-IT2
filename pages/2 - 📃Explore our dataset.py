import streamlit as st
import pandas as pd

# ====== PAGE CONFIG ======
st.set_page_config(page_title=" Sleep Dataset Explorer", layout="wide", page_icon="")

# ====== CUSTOM CSS ======
st.markdown("""
<style>
   /* Animation pulse glow for main heading */
@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 6px 2px rgba(51, 153, 255, 0.6);
        opacity: 1;
    }
    50% {
        box-shadow: 0 0 14px 6px rgba(51, 153, 255, 0.35);
        opacity: 0.85;
    }
    100% {
        box-shadow: 0 0 6px 2px rgba(51, 153, 255, 0.6);
        opacity: 1;
    }
}

/* Cyber pulse animation - dynamic neon circle */
@keyframes cyberPulse {
    0% {
        transform: translateX(0) scale(1);
        box-shadow:
            0 0 8px #00f0ff,
            0 0 16px #00d0ff,
            0 0 24px #00b0ff,
            0 0 32px #0090ff;
        opacity: 1;
    }
    50% {
        transform: translateX(6px) scale(1.15);
        box-shadow:
            0 0 12px #00fff9,
            0 0 24px #00e0ff,
            0 0 36px #00c0ff,
            0 0 48px #00a0ff;
        opacity: 0.75;
    }
    100% {
        transform: translateX(0) scale(1);
        box-shadow:
            0 0 8px #00f0ff,
            0 0 16px #00d0ff,
            0 0 24px #00b0ff,
            0 0 32px #0090ff;
        opacity: 1;
    }
}

/* Reset container padding */
.main .block-container {
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: none !important;
}

/* Main heading with icon, pulse glow animation, and cyber pulse animation */
.main-heading {
    font-family: "Georgia", serif;
    font-size: 3.1rem;
    font-weight: 900;
    color: #0077cc;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 12px;
    margin-bottom: 8px;
    user-select: none;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    animation: pulseGlow 3s ease-in-out infinite;
    border-radius: 12px;
    padding: 12px 18px;
    background: #e6f0ff;
}

.main-heading img {
    filter: drop-shadow(0 1px 1px rgba(0,0,0,0.1));
}

/* Neon circle left of the main heading text */
.cyber-pulse-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(45deg, #00f0ff, #00aaff);
    animation: cyberPulse 2.5s ease-in-out infinite;
    cursor: default;
    box-shadow: 0 0 8px #00f0ff;
}

/* Sleep wave animation container */
.sleep-wave-container {
    width: 100%;
    max-width: 600px;
    height: 100px;
    margin: 12px auto 30px auto;
    position: relative;
}

/* Primary neon wave */
.sleep-wave {
    stroke: #33aaff;
    stroke-width: 3;
    fill: none;
    filter:
        drop-shadow(0 0 4px #33aaff)
        drop-shadow(0 0 10px #33aaff);
    animation: waveMove 4s linear infinite;
    stroke-dasharray: 60 60;
}

/* Secondary dimmer neon wave */
.sleep-wave-2 {
    stroke: #33aaff99;
    stroke-width: 5;
    fill: none;
    filter:
        drop-shadow(0 0 8px #33aaffcc)
        drop-shadow(0 0 15px #33aaffcc);
    animation: waveMove 6s linear infinite reverse;
    stroke-dasharray: 80 80;
}

/* Wave animation movement */
@keyframes waveMove {
    0% {
        stroke-dashoffset: 0;
    }
    100% {
        stroke-dashoffset: -240;
    }
}

/* Sub headings */
.sub-heading {
    font-family: "Georgia", serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 6px;
    color: #444;
    display: flex;
    align-items: center;
    gap: 10px;
}

.sub-sub-heading {
    font-family: "Georgia", serif;
    font-size: 1rem;
    font-style: italic;
    color: #666;
    margin-bottom: 16px;
    padding-left: 6px;
    border-left: 4px solid #0077cc;
    user-select: none;
}

/* Section titles with icon */
.section-title {
    font-family: "Georgia", serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #0077cc;
    margin-top: 36px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 2px solid #0077cc;
    padding-bottom: 6px;
}

.section-title img {
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
}

/* Content paragraphs */
.content-text {
    font-family: "Georgia", serif;
    font-size: 1.05rem;
    color: #333;
    line-height: 1.6;
    text-align: justify;
    margin-bottom: 18px;
    max-width: 900px;
}

    /* Metric boxes with colored bars */
    .metric-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background-color: #f9f9f9;
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #222;
        user-select: none;
        transition: transform 0.15s ease-in-out;
        cursor: default;
    }
    .metric-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .metric-icon {
        width: 26px;
        height: 26px;
        filter: drop-shadow(0 1px 1px rgba(0,0,0,0.07));
    }
    .bar-blue    { border-left: 6px solid #3399ff; }
    .bar-green   { border-left: 6px solid #33cc88; }
    .bar-orange  { border-left: 6px solid #ff9933; }
    .bar-purple  { border-left: 6px solid #9966cc; }
    .bar-red     { border-left: 6px solid #ff4444; }

    /* Dataset variable description styling */
    .variable-entry {
        font-family: "Georgia", serif;
        font-size: 1.1rem;
        line-height: 2.4;
        margin-bottom: 18px;
        max-width: 850px;
        user-select: text;
    }
    .variable-entry span.name {
        color: #0077cc;
        font-weight: 700;
        padding-left: 8px;
    }
    .variable-entry em {
        color: #555;
        font-style: italic;
    }

    /* Dataset section header */
    .custom-header {
        font-family: "Georgia", serif;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-top: 40px !important;
        margin-bottom: 12px !important;
        color: #004a99;
        display: flex;
        align-items: center;
        gap: 14px;
        user-select: none;
    }
    .custom-header img {
        filter: drop-shadow(0 2px 3px rgba(0,0,0,0.15));
    }

    /* Thick divider */
    .divider-thick {
        width: 100%;
        height: 4px;
        background-color: #0077cc;
        border-radius: 8px;
        margin: 14px 0 18px 0;
    }

    /* Dataset intro text */
    .dataset-intro-text {
        font-family: "Georgia", serif;
        font-size: 1.1rem;
        color: #222;
        margin-bottom: 20px;
        max-width: 850px;
    }

    /* Horizontal rules */
    hr.custom-hr {
        border: none;
        border-top: 2px solid #ddd;
        margin-top: 28px;
        margin-bottom: 16px;
    }

    /* Sidebar filter styling overrides */
    .css-1aumxhk {
        font-family: "Georgia", serif;
    }
    .css-1emrehy {
        font-size: 1rem;
        font-weight: 600;
        color: #004a99;
    }

    /* Streamlit multiselect wide */
    .css-1pahdxg-control {
        min-width: 280px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== TITLE + ANIMATION WAVE ======
st.markdown(
    """
    <div class="main-heading">
        <div class="cyber-pulse-circle" title="Sleep Explorer"></div>
         Sleep Dataset Explorer
    </div>
    <hr class="custom-hr" />

    <!-- Sleep wave animation SVG - full width, larger -->
    <div class="sleep-wave-container" aria-label="Sleep wave animation" role="img" title="Animated sleep wave" style="width:100vw; max-width:none; height:160px; margin: 20px 0 40px 0;">
        <svg viewBox="0 0 1000 160" preserveAspectRatio="none" width="100%" height="100%">
            <path class="sleep-wave" d="
                M 0 80
                Q 50 30 100 80
                T 200 80
                T 300 80
                T 400 80
                T 500 80
                T 600 80
                T 700 80
                T 800 80
                T 900 80
                T 1000 80
            "/>
            <path class="sleep-wave-2" d="
                M 0 80
                Q 25 60 50 80
                T 100 80
                T 150 80
                T 200 80
                T 250 80
                T 300 80
                T 350 80
                T 400 80
                T 450 80
                T 500 80
                T 550 80
                T 600 80
                T 650 80
                T 700 80
                T 750 80
                T 800 80
                T 850 80
                T 900 80
                T 950 80
                T 1000 80
            "/>
        </svg>
    </div>

    <style>
    /* Main neon wave - thicker and more vivid */
    .sleep-wave {
        stroke: #33aaff;
        stroke-width: 6;
        fill: none;
        filter:
            drop-shadow(0 0 6px #33aaff)
            drop-shadow(0 0 15px #33aaff);
        animation: waveMove 6s linear infinite;
        stroke-dasharray: 120 120;
    }

    /* Secondary neon wave - dimmer */
    .sleep-wave-2 {
        stroke: #33aaff99;
        stroke-width: 10;
        fill: none;
        filter:
            drop-shadow(0 0 12px #33aaffcc)
            drop-shadow(0 0 25px #33aaffcc);
        animation: waveMove 9s linear infinite reverse;
        stroke-dasharray: 160 160;
    }

    /* Wave movement animation */
    @keyframes waveMove {
        0% {
            stroke-dashoffset: 0;
        }
        100% {
            stroke-dashoffset: -480;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ====== SUBTITLE ======
st.markdown(
    """
    <div class="sub-heading">
        <img src="https://img.icons8.com/fluency/48/open-book.png" width="30" alt="Book Icon" />
        Explore and Filter Sleep Data
    </div>
    <div class="sub-sub-heading">Dive deep into the insights behind sleep and lifestyle.</div>
    """, unsafe_allow_html=True)

# ====== METRICS ======
cols = st.columns(5)

metrics = [
    ("https://img.icons8.com/?size=96&id=HFPX8dOrlqo7&format=png", "533 rows", "bar-blue"),
    ("https://img.icons8.com/?size=96&id=80305&format=png", "15 columns", "bar-green"),
    ("https://img.icons8.com/fluency/48/sleeping-in-bed.png", "7.0 hrs sleep", "bar-orange"),
    ("https://img.icons8.com/fluency/48/heart-with-pulse--v1.png", "73 bpm", "bar-purple"),
    ("https://img.icons8.com/fluency/48/sleep.png", "29% deep", "bar-red"),
]

for col, (icon, text, color_class) in zip(cols, metrics):
    col.markdown(
        f"""
        <div style="
            background-color: #f7f9fa;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        ">
            <img src="{icon}" width="48" style="margin-bottom: 8px;" />
            <span style="font-size: 18px; font-weight: bold;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ====== DATASET OVERVIEW ======
st.markdown(
    """
    <div class="section-title">
        <img src="https://img.icons8.com/fluency/24/data-configuration.png" alt="Data Icon" />
        Dataset Overview
    </div>
    <div class="content-text">
        This dataset contains rich records of sleep, health, and lifestyle data from a diverse group of participants. It includes key measures like sleep duration, sleep quality, physical activity, dietary habits, and health indicators such as stress levels and heart rate. Demographic and lifestyle information enables multifaceted analysis of sleep health.
    </div>
    """, unsafe_allow_html=True)

# ====== WHY CHOOSE THIS DATASET ======
st.markdown(
    """
    <div class="section-title">
        <img src="https://img.icons8.com/fluency/24/why-us-female.png" alt="Why Icon" />
        Why We Chose This Dataset
    </div>
    <div class="content-text">
        The dataset combines objective data (sleep duration, blood pressure, steps) and subjective ratings (sleep quality, stress) with demographic details (age, gender, occupation). This multidimensional data allows in-depth exploration of lifestyle impacts on sleep and health, ideal for uncovering meaningful patterns.
    </div>
    """, unsafe_allow_html=True)

# ====== LOAD DATA ======
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

# ====== SIDEBAR FILTER ======
with st.sidebar:
    st.markdown("<h3 style='font-family: Georgia, serif; color:#004a99;'> Filter Dataset</h3>", unsafe_allow_html=True)
    select_all = st.checkbox("Select All", value=False)

    nationality_options = sorted(df["Nationality"].dropna().unique().tolist())
    gender_options = sorted(df["Gender"].dropna().unique().tolist())
    age_options = sorted(df["Age"].dropna().unique().astype(int))

    if select_all:
        selected_nationalities = nationality_options
        selected_genders = gender_options
        selected_ages = [str(age) for age in age_options]
    else:
        selected_nationalities = st.multiselect("Select Nationality", options=nationality_options)
        selected_genders = st.multiselect("Select Gender", options=gender_options)
        selected_ages = st.multiselect("Select Age", options=[str(age) for age in age_options])

show_data = select_all or bool(selected_nationalities) or bool(selected_genders) or bool(selected_ages)

# ====== VARIABLE DESCRIPTIONS ======
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="custom-header">
        <img src="https://img.icons8.com/fluency/48/document--v1.png" alt="Variables Icon" />
        Dataset Variables Introduction
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="font-family: Georgia, serif; font-weight:700; font-size:1.2rem; margin-bottom:14px;">VARIABLES:</div>', unsafe_allow_html=True)

variables_description = [
    ("Person_ID", "A unique identifier for each individual in the dataset."),
    ("Gender", "Gender of the respondent (e.g., Male, Female)."),
    ("Age", "Age of the respondent, typically in years."),
    ("Occupation", "Job or profession of the individual (e.g., Software Engineer, Doctor)."),
    ("Sleep_Duration", "Average number of hours the individual sleeps per night."),
    ("Quality_of_Sleep", "A rating that reflects subjective sleep quality."),
    ("Physical_Activity_Level", "An indicator of activity level, often measured in minutes or scores."),
    ("Stress_Level", "Measure of perceived stress, rated on a scale (e.g., 1–10)."),
    ("BMI_Category", "Body mass index category: Normal, Overweight, Obese, etc."),
    ("Blood_Pressure", "Blood pressure in systolic/diastolic format (e.g., 126/83)."),
    ("Heart_Rate", "Resting heart rate measured in bpm."),
    ("Daily_Steps", "Average number of steps taken per day."),
    ("Sleep_Disorder", "Whether the individual has a sleep disorder (e.g., Sleep Apnea) or none."),
]

for idx, (name, desc) in enumerate(variables_description, 1):
    st.markdown(
        f"""
        <div class="variable-entry">
            {idx}. <span class="name">{name}:</span> <em>{desc}</em>
        </div>
        """, unsafe_allow_html=True)

# ====== SHOW FILTERED DATA ======
st.markdown(
    """
    <div class="custom-header">
        <img src="https://img.icons8.com/fluency/48/ms-excel.png" alt="Dataset Icon" />
        Dataset Preview
    </div>
    <div class="divider-thick"></div>
    <div class="dataset-intro-text">Explore the filtered dataset below. Use the sidebar filters to narrow down results.</div>
    """, unsafe_allow_html=True)

if show_data:
    filtered_df = df.copy()
    if selected_nationalities:
        filtered_df = filtered_df[filtered_df["Nationality"].isin(selected_nationalities)]
    if selected_genders:
        filtered_df = filtered_df[filtered_df["Gender"].isin(selected_genders)]
    if selected_ages:
        filtered_df = filtered_df[filtered_df["Age"].astype(str).isin(selected_ages)]

    st.markdown(f"Showing {len(filtered_df):,} of {len(df):,} records")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
else:
    st.info("Please select at least one filter or check 'Select All' in the sidebar to display the dataset.")

