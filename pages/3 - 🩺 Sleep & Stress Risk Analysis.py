import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joypy
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Sleep Disorders & Stress", layout="wide", page_icon="💤")

# -------------------- CUSTOM FONTS & AOS --------------------
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
   <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
   <script>
       AOS.init();
   </script>
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
       .stSlider>div>div,
       .stSlider>div>div>div {
           font-family: 'Merriweather', serif !important;
       }
       .fade-in-section {
           animation: fadeInUp 0.8s ease-in-out;
       }
       @keyframes fadeInUp {
           from {
               opacity: 0;
               transform: translate3d(0, 20px, 0);
           }
           to {
               opacity: 1;
               transform: none;
           }
       }
       .insight-box:hover {
           box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
           transform: translateY(-4px);
           transition: all 0.3s ease;
       }
       .insight-box {
           transition: all 0.3s ease;
       }
       .stDataFrame thead tr th {
           background-color: #f0f2f6;
           color: #333;
       }
       .stDataFrame tbody tr:hover {
           background-color: #f6f6f6;
       }
   </style>
""", unsafe_allow_html=True)


# -------------------- DATA LOADING --------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    return df

# -------------------- FILTER FUNCTION --------------------
def apply_filters(data, genders, disorders, age_range):
    return data[
        (data['Gender'].isin(genders)) &
        (data['Sleep Disorder'].isin(disorders)) &
        (data['Age'].between(age_range[0], age_range[1]))
    ]

# -------------------- PIE CHART --------------------
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

# -------------------- RIDGELINE --------------------
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

# -------------------- ANALYSIS FUNCTIONS --------------------
def generate_dynamic_analysis(counts, ridge_df):
    total = counts.sum()
    dominant = counts.idxmax() if total > 0 else None
    BADGE_COLOR = COLOR_MAP

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

    pie_summary = "No data available." if total == 0 else f"The most common sleep condition is {badge(dominant, BADGE_COLOR.get(dominant, '#ccc'))}."
    ridge_summary = "No stress data available." if ridge_df.empty else f"{badge(ridge_df['Sleep Disorder'].value_counts().idxmax())} group shows highest stress."
    return pie_summary, ridge_summary

def generate_demographic_insight(filtered_df):
    if filtered_df.empty: return "No demographic insights available."
    insight = "<strong>🔸 Gender & Age Patterns</strong><br><br>"
    for gender, group in filtered_df.groupby('Gender'):
        common = group['Sleep Disorder'].value_counts().idxmax()
        avg_stress = group['Stress Level'].mean()
        insight += f"- <strong>{gender}</strong>: Most common is <b>{common}</b>, Avg stress: {avg_stress:.2f}<br>"
    return insight

# -------------------- CONSTANTS --------------------
DISORDER_ORDER = ['Sleep Apnea', 'Insomnia', 'None']
COLOR_MAP = {'Sleep Apnea': '#E6A1B3', 'Insomnia': '#E66A6A', 'None': '#D8BFD8'}
RIDGE_COLOR_MAP = {'Sleep Apnea': '#A7C7E7', 'Insomnia': '#FFD1A9', 'None': '#E66A6A'}

# -------------------- LOAD DATA & FILTER --------------------
df = load_data()
st.sidebar.title("Filters")
selected_genders = st.sidebar.multiselect("Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_disorders = st.sidebar.multiselect("Disorders:", DISORDER_ORDER, default=DISORDER_ORDER)
age_range = st.sidebar.slider("Age:", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
filtered_df = apply_filters(df, selected_genders, selected_disorders, age_range)

# -------------------- TITLE --------------------
st.markdown('''
    <div data-aos="fade-down">
        <h1 style='text-align:center;
                   background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: 800;
                   font-size: 2.6em;'>Sleep Disorders & Stress Level Analysis</h1>
        <p style='text-align:center; font-size:18px;'>An interactive visual exploration of sleep health.</p>
    </div>
''', unsafe_allow_html=True)

# -------------------- VISUALIZATIONS --------------------
col1, col2 = st.columns(2)
with col1:
    with st.spinner("Rendering pie chart..."):
        st.markdown('<div data-aos="fade-up">', unsafe_allow_html=True)
        st.subheader("Disorder Proportion")
        disorder_counts = plot_pie_chart(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.spinner("Generating ridgeline..."):
        st.markdown('<div data-aos="fade-up">', unsafe_allow_html=True)
        st.subheader("Stress Level by Disorder")
        ridge_data = plot_ridgeline(filtered_df)
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INTERPRETATION --------------------
pie_text, ridge_text = generate_dynamic_analysis(disorder_counts, ridge_data)
demo_text = generate_demographic_insight(filtered_df)

st.markdown("---")
st.markdown('<div data-aos="fade-up">', unsafe_allow_html=True)
st.subheader("Analytical Summary")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""
        <div class="insight-box" style="padding:20px; background:#f9f9f9; border-left: 5px solid #6C63FF; border-radius:10px;">
            <h3>General Insights</h3>
            <p>{pie_text}</p>
            <p>{ridge_text}</p>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
        <div class="insight-box" style="padding:20px; background:white; border-left: 5px solid #20B2AA; border-radius:10px;">
            <h3>Demographic Patterns</h3>
            <p>{demo_text}</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- RAW DATA --------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
