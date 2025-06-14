import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Sleep Dataset Explorer", layout="wide", page_icon="")

# ====== CUSTOM CSS ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&display=swap');
h1, h2, h3, h4, h5, h6, p, li, div, span, label,
.stMarkdown, .stText, .stDataFrame, button, input, select, textarea {
    font-family: 'Merriweather', serif !important;
}
.main .block-container {
   padding-left: 2rem !important;
   padding-right: 2rem !important;
   max-width: none !important;
   padding-top: 1rem !important;
   padding-bottom: 1rem !important;
}
.main-heading {
   font-size: 3.1rem;
   font-weight: 900;
   background: linear-gradient(45deg, #6C63FF, #20B2AA);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
   text-align: center;
   text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.fade-in {
    opacity: 0;
    animation: fadeIn ease 3.5s;
    animation-fill-mode: forwards;
}
@keyframes fadeIn {
    0%   { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
.sub-heading {
   font-size: 1.4rem;
   font-weight: 700;
   margin-top: 12px;
   margin-bottom: 6px;
   color: #000000;
   display: flex;
   align-items: center;
   gap: 10px;
}
.sub-sub-heading {
   font-size: 1rem;
   font-style: italic;
   color: #666;
   margin-bottom: 8px;
   padding-left: 6px;
   border-left: 4px solid #0077cc;
}
.section-title {
   font-size: 1.3rem;
   font-weight: 700;
   color: #000000;
   margin-top: 36px;
   margin-bottom: 8px;
   display: flex;
   align-items: center;
   gap: 10px;
   border-bottom: 2px solid #0077cc;
   padding-bottom: 6px;
}
.content-text {
   font-size: 1.05rem;
   color: #000000;
   line-height: 1.6;
   text-align: justify;
   margin-bottom: 18px;
   max-width: 900px;
}
.variable-entry {
   font-size: 1.1rem;
   line-height: 2.4;
   margin-bottom: 18px;
   max-width: 850px;
}
.variable-entry span.name {
   color: #0077cc;
   font-weight: 700;
   padding-left: 8px;
}
.variable-entry em {
   color: #000000;
   font-style: italic;
}
.custom-header {
   font-size: 1.5rem;
   font-weight: 700;
   margin-top: 40px;
   margin-bottom: 12px;
   color: #000000;
   display: flex;
   align-items: center;
   gap: 14px;
}
.divider-thick {
   width: 100%;
   height: 4px;
   background-color: #0077cc;
   border-radius: 8px;
   margin: 14px 0 18px 0;
}
.dataset-intro-text {
   font-size: 1.1rem;
   color: #222;
   margin-bottom: 20px;
   max-width: 850px;
}
hr.custom-hr {
   border: none;
   border-top: 2px solid #ddd;
   margin-top: 28px;
   margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ====== TITLE ======
st.markdown('<h1 class="main-heading">Sleep Dataset Explorer</h1>', unsafe_allow_html=True)

# ====== Load Lottie Animation ======
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_sleep = load_lottie_file("panda_sleep.json")

if lottie_sleep:
    st_lottie(lottie_sleep, speed=1, loop=True, quality="high", height=300, key="sleep_animation")
else:
    st.error("Failed to load animation")

# ====== SUBTITLE ======
st.markdown("""
    <div class="sub-heading fade-in">
        <img src="https://img.icons8.com/fluency/48/open-book.png" width="30" />
        Explore and Filter Sleep Data
    </div>
    <div class="sub-sub-heading fade-in">Dive deep into the insights behind sleep and lifestyle.</div>
""", unsafe_allow_html=True)

# ====== METRICS ======
cols = st.columns(2)
metrics = [
    ("https://img.icons8.com/?size=96&id=HFPX8dOrlqo7&format=png", "532 records"),
    ("https://img.icons8.com/?size=96&id=80305&format=png", "15 columns"),
]

for col, (icon, text) in zip(cols, metrics):
    col.markdown(f"""
        <div class="fade-in" style="background-color: #f7f9fa; padding: 16px; border-radius: 12px;
        text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); height: 120px; display: flex;
        flex-direction: column; justify-content: center; align-items: center; width: 100%;">
            <img src="{icon}" width="48" style="margin-bottom: 8px;" />
            <span style="font-size: 18px; font-weight: bold;">{text}</span>
        </div>
    """, unsafe_allow_html=True)

# ====== OVERVIEW ======
st.markdown("""
    <div class="section-title fade-in">
        <img src="https://img.icons8.com/fluency/24/data-configuration.png" />
        Dataset Overview
    </div>
    <div class="content-text fade-in">
         This dataset contains rich records of sleep, health, and lifestyle data from a diverse group of participants. It includes key measures like sleep duration, sleep quality, physical activity, dietary habits, and health indicators such as stress levels and heart rate. Demographic and lifestyle information enables multifaceted analysis of sleep health.
    </div>
""", unsafe_allow_html=True)

# ====== WHY THIS DATASET ======
st.markdown("""
    <div class="section-title fade-in">
        <img src="https://img.icons8.com/fluency/24/why-us-female.png" />
        Why We Chose This Dataset
    </div>
    <div class="content-text fade-in">
          The dataset combines objective data (sleep duration, blood pressure, steps) and subjective ratings (sleep quality, stress) with demographic details (age, gender, occupation). This multidimensional data allows for in-depth exploration of lifestyle impacts on sleep and health, which is ideal for uncovering meaningful patterns.
    </div>
""", unsafe_allow_html=True)

# ====== LOAD DATA ======
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

# ====== SIDEBAR FILTERS ======
with st.sidebar:
    st.markdown("<h3 style='font-family: Merriweather, serif; color:#004a99;'>Filter Dataset</h3>", unsafe_allow_html=True)
    nationality_options = sorted(df["Nationality"].dropna().unique().tolist())
    gender_options = sorted(df["Gender"].dropna().unique().tolist())
    age_options = sorted(df["Age"].dropna().unique().astype(int))
    default_age_range = (min(age_options), max(age_options))

    if st.button("Reset Filters"):
        st.session_state["selected_nationalities"] = []
        st.session_state["selected_genders"] = []
        st.session_state["selected_age_range"] = default_age_range

    selected_nationalities = st.multiselect(
        "Select Nationality", options=nationality_options,
        default=st.session_state.get("selected_nationalities", []),
        key="selected_nationalities"
    )

    selected_genders = st.multiselect(
        "Select Gender", options=gender_options,
        default=st.session_state.get("selected_genders", []),
        key="selected_genders"
    )

    selected_age_range = st.slider(
        "Select Age Range",
        min_value=default_age_range[0],
        max_value=default_age_range[1],
        value=st.session_state.get("selected_age_range", default_age_range),
        key="selected_age_range"
    )

# ====== VARIABLE DESCRIPTION ======
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
st.markdown("""
    <div class="custom-header fade-in">
        <img src="https://img.icons8.com/fluency/48/document--v1.png" />
        Dataset Variables Introduction
    </div>
""", unsafe_allow_html=True)

variables_description = [
    ("Person_ID", "A unique identifier for each individual in the dataset."),
    ("Gender", "Gender of the respondent (e.g., Male, Female)."),
    ("Age", "Age of the respondent, typically in years."),
    ("Occupation", "Job or profession of the individual."),
    ("Sleep_Duration", "Average number of hours the individual sleeps per night."),
    ("Quality_of_Sleep", "A rating that reflects subjective sleep quality."),
    ("Physical_Activity_Level", "An indicator of activity level."),
    ("Stress_Level", "Measure of perceived stress, rated on a scale."),
    ("BMI_Category", "Body mass index category."),
    ("Blood_Pressure", "Blood pressure in systolic/diastolic format."),
    ("Heart_Rate", "Resting heart rate measured in bpm."),
    ("Daily_Steps", "Average number of steps taken per day."),
    ("Sleep_Disorder", "Whether the individual has a sleep disorder or none."),
]

for idx, (name, desc) in enumerate(variables_description, 1):
    st.markdown(f"""
        <div class="variable-entry fade-in">
            {idx}. <span class="name">{name}:</span> <em>{desc}</em>
        </div>
    """, unsafe_allow_html=True)

# ====== FILTER DATA ======
filtered_df = df.copy()
if selected_nationalities:
    filtered_df = filtered_df[filtered_df["Nationality"].isin(selected_nationalities)]
if selected_genders:
    filtered_df = filtered_df[filtered_df["Gender"].isin(selected_genders)]
if selected_age_range:
    filtered_df = filtered_df[(filtered_df["Age"] >= selected_age_range[0]) & (filtered_df["Age"] <= selected_age_range[1])]

# ====== DISPLAY DATA ======
st.markdown("""
    <div class="custom-header fade-in">
        <img src="https://img.icons8.com/fluency/48/ms-excel.png" />
        Dataset Preview
    </div>
    <div class="divider-thick fade-in"></div>
    <div class="dataset-intro-text fade-in">Explore the filtered dataset below. Use the sidebar filters to narrow down results.</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""<div class='fade-in'>Showing <span style='color:blue; font-weight:bold;'>{len(filtered_df):,}</span> 
    of <span style='color:red; font-weight:bold;'>{len(df):,}</span> records</div>""",
    unsafe_allow_html=True
)

st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
