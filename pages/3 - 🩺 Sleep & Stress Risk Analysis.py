import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joypy
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Sleep Disorders & Stress Level Analysis", layout="wide")
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <style>
       html, body, [class*="st-"], .stApp, .stSidebar, .stSidebarContent {
           font-family: 'Merriweather', serif !important;
       }
       h1, h2, h3, h4, h5, h6, p, span, div, label, section, input, textarea, select {
           font-family: 'Merriweather', serif !important;
       }
       .stButton>button,
       .stTextInput>div>input,
       .stSelectbox>div>div,
       .stMultiSelect>div>div,
       .stSlider,
       .stSlider>div>div,
       .stSlider>div>div>div {
           font-family: 'Merriweather', serif !important;
       }
   </style>
""", unsafe_allow_html=True)

# -------------------- CUSTOM CSS EFFECT --------------------
st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 20px, 0); }
            to { opacity: 1; transform: none; }
        }
        .fade-in-section { animation: fadeInUp 0.8s ease-in-out; }
        .insight-box:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-4px);
            transition: all 0.3s ease;
        }
        .insight-box { transition: all 0.3s ease; }
        .stDataFrame thead tr th { background-color: #f0f2f6; color: #333; }
        .stDataFrame tbody tr:hover { background-color: #f6f6f6; }
    </style>
""", unsafe_allow_html=True)

DISORDER_ORDER = ['Sleep Apnea', 'Insomnia', 'None']
COLOR_MAP = {'Sleep Apnea': '#E6A1B3', 'Insomnia': '#E66A6A', 'None': '#D8BFD8'}
RIDGE_COLOR_MAP = {'Sleep Apnea': '#A7C7E7', 'Insomnia': '#FFD1A9', 'None': '#E66A6A'}

@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    return df

def apply_filters(data, genders, disorders, age_range):
    return data[
        (data['Gender'].isin(genders)) &
        (data['Sleep Disorder'].isin(disorders)) &
        (data['Age'].between(age_range[0], age_range[1]))
    ]

def plot_pie_chart(data):
    counts = data['Sleep Disorder'].value_counts().reindex(DISORDER_ORDER).fillna(0)
    filtered_counts = counts[counts > 0]
    if filtered_counts.empty:
        st.warning("No data for the selected filters.")
        return counts
    if len(filtered_counts) == 1:
        st.info(f"Only one disorder selected: **{filtered_counts.index[0]}** (100%).")
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

# === MAIN ===
df = load_data()
if df.empty:
    st.stop()

st.sidebar.title("Filters")
genders = df['Gender'].dropna().unique().tolist()
selected_genders = st.sidebar.multiselect("Select gender(s):", options=genders, default=genders)
selected_disorders = st.sidebar.multiselect("Select disorder types:", options=DISORDER_ORDER, default=DISORDER_ORDER)
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select age range:", min_age, max_age, (min_age, max_age))

with st.spinner("Processing filters..."):
    time.sleep(0.5)
    filtered_df = apply_filters(df, selected_genders, selected_disorders, age_range).copy()

st.markdown('''
    <div class="fade-in-section">
        <h1 style='text-align: center; background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.5em;'>Sleep Disorders & Stress Level Analysis</h1>
    </div>
''', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Visualizing the proportion of sleep disorders and how stress levels distribute across them.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.spinner("Loading sleep disorder chart..."):
        time.sleep(0.8)
        st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
        st.subheader("Sleep Disorder Proportion")
        disorder_counts = plot_pie_chart(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.spinner("Generating stress level plot..."):
        time.sleep(0.8)
        st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
        st.subheader("Stress Level Distribution by Disorder")
        ridge_data = plot_ridgeline(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="fade-in-section">', unsafe_allow_html=True)
st.subheader("Analytical Summary")
st.markdown("This analytical summary is displayed based on the chosen filter criteria")
# Analytical and demographic summary rendering goes here...
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("View Filtered Raw Data"):
    st.caption("Filtered dataset preview:")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
