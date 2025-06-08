import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Sleep Dataset Explorer", layout="wide", page_icon="")

# ====== CUSTOM CSS (Toàn trang với font Merriweather) ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&display=swap');

/* Toàn trang */
html, body, [class*="css"] {
    font-family: 'Merriweather', serif !important;
}

/* Các component nội dung chính */
h1, h2, h3, h4, h5, h6, strong, b, p, li, span, div, label {
    font-family: 'Merriweather', serif !important;
}

/* Markdown và văn bản */
.stMarkdown, .stText, .stTextInput, .stSelectbox, .stDataFrame {
    font-family: 'Merriweather', serif !important;
    font-size: 16px;
}

/* Sidebar */
.sidebar .css-1d391kg, .sidebar .css-1oe5cao {
    font-family: 'Merriweather', serif !important;
}

/* Table content */
thead, tbody, tfoot, tr, td, th {
    font-family: 'Merriweather', serif !important;
}

/* Metric box */
.metric-label, .metric-value {
    font-family: 'Merriweather', serif !important;
}
</style>
""", unsafe_allow_html=True)

# ====== TITLE with gradient ======
st.markdown('''
    <div class="fade-in-section">
        <h1 style='text-align: center;
                   background: -webkit-linear-gradient(50deg, #6C63FF, #20B2AA);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: 800;
                   font-size: 2.5em;
                   font-family: "Merriweather", serif;
                   '>Sleep Dataset Explorer</h1>
    </div>
''', unsafe_allow_html=True)

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
st.markdown(
   """
   <div class="sub-heading">
       <img src="https://img.icons8.com/fluency/48/open-book.png" width="30" alt="Book Icon" />
      Explore and Filter Sleep Data
   </div>
   <div class="sub-sub-heading">Dive deep into the insights behind sleep and lifestyle.</div>
   """, unsafe_allow_html=True)

# ====== METRICS ======
cols = st.columns(2)
metrics = [
   ("https://img.icons8.com/?size=96&id=HFPX8dOrlqo7&format=png", "532 records"),
   ("https://img.icons8.com/?size=96&id=80305&format=png", "15 columns"),
]

for col, (icon, text) in zip(cols, metrics):
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
           width: 100%;
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
   st.markdown("<h3 style='font-family: Merriweather, serif; color:#004a99;'> Filter Dataset</h3>", unsafe_allow_html=True)

   nationality_options = sorted(df["Nationality"].dropna().unique().tolist())
   gender_options = sorted(df["Gender"].dropna().unique().tolist())
   age_options = sorted(df["Age"].dropna().unique().astype(int))
   default_age_range = (min(age_options), max(age_options))

   selected_nationalities = st.multiselect("Select Nationality", options=nationality_options)
   selected_genders = st.multiselect("Select Gender", options=gender_options)
   selected_age_range = st.slider("Select Age Range", min_value=default_age_range[0], max_value=default_age_range[1], value=default_age_range)

# ====== VARIABLE DESCRIPTIONS ======
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
st.markdown(
   """
   <div class="custom-header">
       <img src="https://img.icons8.com/fluency/48/document--v1.png" alt="Variables Icon" />
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

filtered_df = df.copy()
if selected_nationalities:
   filtered_df = filtered_df[filtered_df["Nationality"].isin(selected_nationalities)]
if selected_genders:
   filtered_df = filtered_df[filtered_df["Gender"].isin(selected_genders)]
if selected_age_range:
   filtered_df = filtered_df[(filtered_df["Age"] >= selected_age_range[0]) & (filtered_df["Age"] <= selected_age_range[1])]

st.markdown(f"Showing {len(filtered_df):,} of {len(df):,} records")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
