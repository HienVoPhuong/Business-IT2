import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Sleep Dataset Explorer", layout="wide", page_icon="")

# ====== CUSTOM CSS ======
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&display=swap');

html, body, [class*="css"] {
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
   background-clip: text;
   text-fill-color: transparent;
   user-select: none;
   margin: 6px 0 4px 0;
   text-align: center;
   width: 100%;
   text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.main-heading img {
   filter: drop-shadow(0 1px 1px rgba(0,0,0,0.1));
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
   user-select: none;
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

.section-title img {
   filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
}

.content-text {
   font-size: 1.05rem;
   color: #000000;
   line-height: 1.6;
   text-align: justify;
   margin-bottom: 18px;
   max-width: 900px;
}

.metric-box {
   display: flex;
   align-items: center;
   gap: 12px;
   background-color: #f9f9f9;
   padding: 14px 18px;
   border-radius: 12px;
   box-shadow: 0 3px 6px rgba(0,0,0,0.05);
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

.variable-entry {
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
   color: #000000;
   font-style: italic;
}

/* Fade-in animation */
.fade-in-section {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 1s forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.custom-header {
   font-size: 1.5rem !important;
   font-weight: 700 !important;
   margin-top: 40px !important;
   margin-bottom: 12px !important;
   color: #000000;
   display: flex;
   align-items: center;
   gap: 14px;
   user-select: none;
}
.custom-header img {
   filter: drop-shadow(0 2px 3px rgba(0,0,0,0.15));
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

# ====== TITLE with gradient and fade-in ======
st.markdown('''
    <div class="fade-in-section">
        <h1 style='text-align: center;
                   background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: 800;
                   font-size: 2.5em;'>Sleep Dataset Explorer</h1>
    </div>
''', unsafe_allow_html=True)

# Load lottie animation from local file
def load_lottie_file(filepath: str):
   with open(filepath, "r") as f:
       return json.load(f)

lottie_sleep = load_lottie_file("panda_sleep.json")

if lottie_sleep:
   st_lottie(
       lottie_sleep,
       speed=1,
       loop=True,
       quality="high",
       height=300,
       key="sleep_animation"
   )
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
   ("https://img.icons8.com/?size=96&id=HFPX8dOrlqo7&format=png", "533 rows", "bar-blue"),
   ("https://img.icons8.com/?size=96&id=80305&format=png", "15 columns", "bar-green"),
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
           width: 100%;
       ">
           <img src="{icon}" width="48" style="margin-bottom: 8px;" />
           <span style="font-size: 18px; font-weight: bold;">{text}</span>
       </div>
       """,
       unsafe_allow_html=True,
   )

st.markdown(
   """
   <style>
   .section-title {
       display: flex;
       align-items: center;
       font-weight: bold;
       font-size: 24px;
       margin-bottom: 10px;
   }
   .section-title img {
       margin-right: 10px;
   }
   .content-text {
       width: 100%;
       font-size: 18px;
       line-height: 1.6;
       margin-bottom: 30px;
       text-align: justify;
   }
   </style>
   """, unsafe_allow_html=True
)

# ====== DATASET OVERVIEW ======
st.markdown(
   """
   <div class="section-title">
       <img src="https://img.icons8.com/fluency/24/data-configuration.png" alt="Data Icon" />
       Dataset Overview
   </div>
   <div class="content-text" style="width: 100%; max-width: none;">
       This dataset contains rich records of sleep, health, and lifestyle data from a diverse group of participants. It includes key measures like sleep duration, sleep quality, physical activity, dietary habits, and health indicators such as stress levels and heart rate. Demographic and lifestyle information enables multifaceted analysis of sleep health.
   </div>
   """, unsafe_allow_html=True
)

# ====== WHY CHOOSE THIS DATASET ======
st.markdown(
   """
   <div class="section-title">
       <img src="https://img.icons8.com/fluency/24/why-us-female.png" alt="Why Icon" />
       Why We Chose This Dataset
   </div>
   <div class="content-text" style="width: 100%; max-width: none;">
       The dataset combines objective data (sleep duration, blood pressure, steps) and subjective ratings (sleep quality, stress) with demographic details (age, gender, occupation). This multidimensional data allows in-depth exploration of lifestyle impacts on sleep and health, ideal for uncovering meaningful patterns.
   </div>
   """, unsafe_allow_html=True
)
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
