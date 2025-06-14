import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joypy
import time

# -------------------- PAGE CONFIG --------------------
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <style>
       html, body, [class*="st-"], .stApp, .stSidebar, .stSidebarContent {
           font-family: 'Merriweather', serif !important;
       }
       h1, h2, h3, h4, h5, h6, p, span, div, label, section, input, textarea, select {
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
        .fade-in-section {
            animation: fadeInUp 0.8s ease-in-out;
        }
        .insight-box:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-4px);
            transition: all 0.3s ease;
        }
        .insight-box {
            transition: all 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- CONSTANTS --------------------
DISORDER_ORDER = ['Sleep Apnea', 'Insomnia', 'None']
COLOR_MAP = {'Sleep Apnea': '#E6A1B3', 'Insomnia': '#E66A6A', 'None': '#D8BFD8'}
RIDGE_COLOR_MAP = {'Sleep Apnea': '#A7C7E7', 'Insomnia': '#FFD1A9', 'None': '#E66A6A'}

# -------------------- DATA LOADING --------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Sleep Health Lifestyle Dataset.xlsx")
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    return df

# -------------------- FILTER FUNCTION --------------------
def apply_filters(data, genders, disorders, age_range):
    df = data.copy()
    if genders:
        df = df[df['Gender'].isin(genders)]
    if disorders:
        df = df[df['Sleep Disorder'].isin(disorders)]
    df = df[df['Age'].between(age_range[0], age_range[1])]
    return df

# -------------------- PIE CHART FUNCTION --------------------
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

# -------------------- RIDGELINE PLOT FUNCTION --------------------
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

# -------------------- INTERPRETATION GENERATORS --------------------
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
    pie_summary = (
        f"The most common sleep condition in the selected group is "
        f"{badge(dominant, BADGE_COLOR.get(dominant, '#ccc'))}, based on the filtered data."
    ) if total > 0 else "No data available for current filter selection."
    if ridge_df.empty:
        ridge_summary = "Stress level distribution is not available for the current filters."
    else:
        avg_stress = ridge_df.groupby('Sleep Disorder')['Stress Level'].mean().sort_values(ascending=False)
        highest = avg_stress.index[0]
        highest_val = avg_stress.iloc[0]
        ridge_summary = (
            f"People with {badge(highest, BADGE_COLOR.get(highest, '#ccc'))} show the highest average stress level: "
            f"{colored_number(highest_val)}."
        )
    return pie_summary, ridge_summary

def generate_demographic_insight(filtered_df):
    insights = ""
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
    if 'Gender' in filtered_df.columns and not filtered_df.empty:
        gender_groups = filtered_df.groupby('Gender', observed=False)
        insights += "<strong>🔸Gender-Based Observations</strong><br><br>"
        for gender, group in gender_groups:
            disorder_ratio = group['Sleep Disorder'].value_counts(normalize=True) * 100
            dominant_disorder = disorder_ratio.idxmax()
            stress_mean = group['Stress Level'].mean() if 'Stress Level' in group.columns else None
            insights += f"- Among <strong>{gender}</strong>, the most common sleep condition is {badge(dominant_disorder, BADGE_COLOR.get(dominant_disorder, '#ccc'))}.<br>"
            if stress_mean:
                insights += f"&nbsp;&nbsp;&nbsp;&nbsp;Average stress level: {colored_number(stress_mean)}<br>"
    if 'Age' in filtered_df.columns:
        age_bins = [0, 25, 40, 60, 100]
        age_labels = ["<25", "25-40", "40-60", "60+"]
        filtered_df = filtered_df.copy()
        filtered_df['Age Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels)
        insights += "<br><strong>🔸Age Group Insights</strong><br><br>"
        age_groups = filtered_df.groupby('Age Group', observed=False)
        for label, group in age_groups:
            if group.empty:
                continue
            disorder_counts = group['Sleep Disorder'].value_counts(normalize=True) * 100
            top_disorder = disorder_counts.idxmax()
            avg_stress = group['Stress Level'].mean() if 'Stress Level' in group.columns else None
            insights += f"- In the <strong>{label}</strong> age group, {badge(top_disorder, BADGE_COLOR.get(top_disorder, '#ccc'))} is most common.<br>"
            if avg_stress:
                insights += f"&nbsp;&nbsp;&nbsp;&nbsp;Average stress level: {colored_number(avg_stress)}<br>"
    return insights

# -------------------- MAIN APP --------------------
df = load_data()
if df.empty:
    st.stop()

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.title("Filters")
genders = df['Gender'].dropna().unique().tolist()
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())

# Reset button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.selected_genders = []
    st.session_state.selected_disorders = []
    st.session_state.age_range = (min_age, max_age)
    st.experimental_rerun()

# Widgets with session state
selected_genders = st.sidebar.multiselect(
    "Select gender(s):", options=genders,
    default=st.session_state.get('selected_genders', [])
)
selected_disorders = st.sidebar.multiselect(
    "Select disorder types:", options=DISORDER_ORDER,
    default=st.session_state.get('selected_disorders', [])
)
age_range = st.sidebar.slider(
    "Select age range:", min_value=min_age, max_value=max_age,
    value=st.session_state.get('age_range', (min_age, max_age))
)

# Save to session state
st.session_state.selected_genders = selected_genders
st.session_state.selected_disorders = selected_disorders
st.session_state.age_range = age_range

# Apply filters
filtered_df = apply_filters(df, selected_genders, selected_disorders, age_range)

# -------------------- MAIN CONTENT --------------------
st.markdown("""
    <div class="fade-in-section">
        <h1 style='text-align: center;
                   background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: 800;
                   font-size: 2.5em;'>Sleep Disorders & Stress Level Analysis</h1>
    </div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Visualizing the proportion of sleep disorders and how stress levels distribute across them.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.spinner("Loading sleep disorder chart..."):
        disorder_counts = plot_pie_chart(filtered_df)

with col2:
    with st.spinner("Generating stress level plot..."):
        ridge_data = plot_ridgeline(filtered_df)

pie_en, ridge_en = generate_dynamic_analysis(disorder_counts, ridge_data)
demographic_en = generate_demographic_insight(filtered_df)

st.markdown("---")
st.subheader("Analytical Summary")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""
    <div class="insight-box" style="padding:20px; background-color:#f9f9f9; border-left: 5px solid #6C63FF; border-radius:10px;">
        <h3 style="margin-top:0; color:#333;">General Insights</h3>
        <p>{pie_en}</p>
        <p>{ridge_en}</p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="insight-box" style="padding:20px; background-color:white; border-left: 5px solid #20B2AA; border-radius:10px;">
        <h3 style="margin-top:0; color:#333;">Demographic Patterns</h3>
        <p>{demographic_en}</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- RAW DATA --------------------
with st.expander("📄 View Filtered Raw Data"):
    st.caption("Filtered dataset preview:")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
