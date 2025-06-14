import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joypy
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Sleep & Stress Analysis", layout="wide")
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <style>
       html, body, [class*="st-"], .stApp, .stSidebar, .stSidebarContent {
           font-family: 'Merriweather', serif !important;
       }
   </style>
""", unsafe_allow_html=True)

# -------------------- CONSTANTS --------------------
DISORDER_ORDER = ['Sleep Apnea', 'Insomnia', 'None']
COLOR_MAP = {'Sleep Apnea': '#E6A1B3', 'Insomnia': '#E66A6A', 'None': '#D8BFD8'}
RIDGE_COLOR_MAP = {'Sleep Apnea': '#A7C7E7', 'Insomnia': '#FFD1A9', 'None': '#E66A6A'}

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    return df

df = load_data()
if df.empty:
    st.stop()

# -------------------- SESSION STATE FOR RESET --------------------
if 'reset' not in st.session_state:
    st.session_state.reset = False

if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.reset = True

# -------------------- FILTERS --------------------
st.sidebar.title("Filters")

# Default values
genders = df['Gender'].dropna().unique().tolist()
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())

if st.session_state.reset:
    selected_genders = []
    selected_disorders = []
    age_range = (min_age, max_age)
    st.session_state.reset = False  # Reset once
else:
    selected_genders = st.sidebar.multiselect("Select gender(s):", options=genders, default=[])
    selected_disorders = st.sidebar.multiselect("Select disorder types:", options=DISORDER_ORDER, default=[])
    age_range = st.sidebar.slider("Select age range:", min_age, max_age, (min_age, max_age))

# -------------------- FILTER FUNCTION --------------------
def apply_filters(data, genders, disorders, age_range):
    df = data.copy()
    if genders:
        df = df[df['Gender'].isin(genders)]
    if disorders:
        df = df[df['Sleep Disorder'].isin(disorders)]
    if isinstance(age_range, (list, tuple)) and len(age_range) == 2:
        df = df[df['Age'].between(age_range[0], age_range[1])]
    return df

filtered_df = apply_filters(df, selected_genders, selected_disorders, age_range)

# -------------------- PLOTTING --------------------
def plot_pie_chart(data):
    counts = data['Sleep Disorder'].value_counts().reindex(DISORDER_ORDER).fillna(0)
    filtered_counts = counts[counts > 0]
    if filtered_counts.empty:
        st.warning("No data for the selected filters.")
        return counts
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, _, _ = ax.pie(
        filtered_counts,
        colors=[COLOR_MAP[k] for k in filtered_counts.index],
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 13},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        pctdistance=0.8
    )
    for i, wedge in enumerate(wedges):
        ang = (wedge.theta2 + wedge.theta1) / 2
        x, y = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
        ha = "right" if x < 0 else "left"
        ax.annotate(
            filtered_counts.index[i],
            xy=(x, y),
            xytext=(1.1 * np.sign(x), 1.05 * y),
            ha=ha, va="center",
            fontsize=14,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5),
            arrowprops=dict(arrowstyle="-", color="gray")
        )
    ax.axis('equal')
    st.pyplot(fig)
    plt.close(fig)
    return counts

def plot_ridgeline(data):
    valid_counts = data['Sleep Disorder'].value_counts()
    valid_disorders = valid_counts[valid_counts > 1].index.tolist()
    ridge_df = data[data['Sleep Disorder'].isin(valid_disorders)].dropna(subset=['Stress Level'])
    if not valid_disorders or ridge_df.empty:
        st.info("Not enough data to show ridgeline plot.")
        return ridge_df
    fig, _ = joypy.joyplot(
        ridge_df,
        by='Sleep Disorder',
        column='Stress Level',
        color=[RIDGE_COLOR_MAP[d] for d in valid_disorders],
        alpha=0.7,
        figsize=(8, 6),
        fade=True
    )
    plt.xlabel('Stress Level', fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    return ridge_df

# -------------------- INTERPRETATION FUNCTIONS --------------------
def badge(text, color="#FFD700"):
    return f'<span style="background-color:{color}; color:black; padding:3px 8px; border-radius:8px; font-size:13px;">{text}</span>'

def colored_number(value):
    try:
        val = float(value)
        if val < 5:
            color = "#668fd4"
        elif val < 7:
            color = "#fa9850"
        else:
            color = "#e4444e"
        return f'<span style="color:{color}; font-weight:bold;">{val:.2f}</span>'
    except:
        return f'<span style="color:gray;">N/A</span>'

def generate_dynamic_analysis(counts, ridge_df):
    total = counts.sum()
    dominant = counts.idxmax() if total > 0 else None
    if total == 0:
        pie_summary = "No data available for current filter selection."
    else:
        pie_summary = f"The most common sleep condition is {badge(dominant, COLOR_MAP.get(dominant, '#ccc'))}."
    if ridge_df.empty:
        ridge_summary = "Stress level distribution is not available for the current filters."
    else:
        avg_stress = ridge_df.groupby('Sleep Disorder')['Stress Level'].mean().sort_values(ascending=False)
        highest = avg_stress.index[0]
        ridge_summary = f"People with {badge(highest, COLOR_MAP.get(highest, '#ccc'))} have highest stress: {colored_number(avg_stress.iloc[0])}."
    return pie_summary, ridge_summary

# -------------------- DISPLAY --------------------
st.title("🩺 Sleep Disorders & Stress Level Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sleep Disorder Proportion")
    disorder_counts = plot_pie_chart(filtered_df)

with col2:
    st.subheader("Stress Level Distribution by Disorder")
    ridge_data = plot_ridgeline(filtered_df)

# -------------------- SUMMARY --------------------
pie_en, ridge_en = generate_dynamic_analysis(disorder_counts, ridge_data)
st.markdown("---")
st.subheader("Summary Insights")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"<div style='padding:12px 20px; background:#f0f2f6; border-radius:10px'>{pie_en}<br>{ridge_en}</div>", unsafe_allow_html=True)

with col_b:
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

