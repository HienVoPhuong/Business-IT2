import streamlit as st
import pandas as pd
import plotly.express as px

# --------- Page Configuration ---------
st.set_page_config(page_title="Stress & Sleep Dashboard", layout="wide")

# --------- Font Styling ---------
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <style>
       html, body, [class*="st-"], .stApp {
           font-family: 'Merriweather', serif !important;
       }
       h1, h2, h3, h4, h5, h6, p, span, div {
           font-family: 'Merriweather', serif !important;
       }
       .stButton>button, .stTextInput>div>input, .stSelectbox>div>div, .stMultiSelect>div>div {
           font-family: 'Merriweather', serif !important;
       }
   </style>
""", unsafe_allow_html=True)

st.markdown('''
   <div class="fade-in-section">
       <h1 style='text-align: center;
                  background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  font-weight: 800;
                  font-size: 2.5em;'>Sleep and Heart Rate Dashboard</h1>
   </div>
''', unsafe_allow_html=True)

# --------- Title Effect ---------
st.markdown("""
   <style>
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

       .fade-in-section {
           animation: fadeInUp 0.8s ease-in-out;
       }
   </style>
""", unsafe_allow_html=True)

# --------- Load Dataset from XLSX ---------
file_path = "Sleep Health Lifestyle Dataset.xlsx"
df = pd.read_excel(file_path)
df = df.dropna(subset=['Age', 'Gender', 'Heart Rate', 'Occupation', 'Sleep Duration', 'Quality of Sleep'])

# --------- SIDEBAR: Age Filter ---------
st.sidebar.header("Filter by Age")
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
selected_age = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# --------- ADVANCED FILTERS ---------
st.sidebar.markdown("### 🧪 Advanced Filters")
filter_sleep_quality = st.sidebar.checkbox("Only Poor Sleepers (≤6)", value=False)
filter_high_hr = st.sidebar.checkbox("Only High Heart Rate (>80 bpm)", value=False)

# --------- Filter dataset by Age ---------
filtered_df = df[(df['Age'] >= selected_age[0]) & (df['Age'] <= selected_age[1])]

# Apply Advanced Filters
if filter_sleep_quality:
   filtered_df = filtered_df[filtered_df['Quality of Sleep'] <= 6]
if filter_high_hr:
   filtered_df = filtered_df[filtered_df['Heart Rate'] > 80]

# --------- KPI Metrics ---------
st.markdown("#### 🗾 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
with col1:
   st.metric("👤 Records", len(filtered_df))
with col2:
   st.metric("❤️ Average Heart Rate", f"{filtered_df['Heart Rate'].mean():.1f} bpm")
with col3:
   st.metric("🛌 Average Sleep Duration", f"{filtered_df['Sleep Duration'].mean():.1f} hours")

# --------- Show Active Filters ---------
active_filters = []
if filter_sleep_quality:
   active_filters.append("🛌 Poor Sleep (≤6)")
if filter_high_hr:
   active_filters.append("💓 High Heart Rate (>80 bpm)")
if active_filters:
   st.markdown(
       f"<small><strong>Filters applied:</strong> {' | '.join(active_filters)}</small>",
       unsafe_allow_html=True
   )

# ---------- SECTION 1: Heart Rate Line Chart ----------
heart_rate_grouped = filtered_df.groupby(['Age', 'Gender'], observed=False)['Heart Rate'].mean().reset_index()
color_map = {'Female': '#E66A6A', 'Male': '#A7C7E7'}

fig_line = px.line(
   heart_rate_grouped,
   x="Age",
   y="Heart Rate",
   color="Gender",
   color_discrete_map=color_map,
   markers=True,
   title=(f" Average Heart Rate Trends by Gender (Ages {selected_age[0]}–{selected_age[1]})"),
   labels={"Heart Rate": "Average Heart Rate"},
   custom_data=["Gender"]
)
fig_line.update_traces(
   hovertemplate='<b>Age: %{x}</b><br>Avg HR: %{y:.1f}<br>Gender: %{customdata[0]}<extra></extra>',
   line=dict(width=2)
)
fig_line.update_layout(
   legend_title_text='Gender',
   height=400,
   margin=dict(l=10, r=10, t=40, b=20),
   font=dict(family="Merriweather, serif", size=12),
   title_font_family="Merriweather, serif",
   title_font_size=24 
)
st.plotly_chart(fig_line, use_container_width=True)

# ---------- SECTION 2: Sleep Quality Bar Chart ----------
occupations = sorted(filtered_df['Occupation'].dropna().unique())
occupation_options = ['All'] + occupations
selected_occupation = st.selectbox("🔎 Select an Occupation", occupation_options, key="bar_occupation_filter")
bar_df = filtered_df.copy() if selected_occupation == 'All' else filtered_df[filtered_df['Occupation'] == selected_occupation].copy()
bar_df['Quality of Sleep'] = bar_df['Quality of Sleep'].astype(str)

if bar_df.empty:
   st.warning("⚠️ No data for the selected occupation and age range.")
else:
   sleep_counts = bar_df.groupby(['Occupation', 'Quality of Sleep'], observed=False).size().reset_index(name='Count')
   sleep_order = ['4', '5', '6', '7', '8', '9']
   sleep_colors = {
       '4': '#F7D794', '5': '#A7C7E7', '6': '#E6A1B3',
       '7': '#E66A6A', '8': '#FF7F00', '9': '#5E548E'
   }
   fig_bar = px.bar(
       sleep_counts,
       x='Occupation',
       y='Count',
       color='Quality of Sleep',
       barmode='group',
       title=" Distribution of Sleep Quality Across Occupations" + ("" if selected_occupation == 'All' else f" – {selected_occupation}"),
       labels={'Quality of Sleep': 'Sleep Quality', 'Occupation': 'Occupation'},
       category_orders={'Quality of Sleep': sleep_order},
       color_discrete_map=sleep_colors
   )
   fig_bar.update_layout(
       xaxis_tickangle=0,
       xaxis_title="Occupation",
       yaxis_title="Count",
       font=dict(family="Merriweather, serif", size=12),
       title_font_family="Merriweather, serif",
       title_font_size=24, 
       height=400
   )
   st.plotly_chart(fig_bar, use_container_width=True)

# -------------------- ANALYTICAL UTILS --------------------
def badge(text, color="#FFD700"):
   return f'<span style="background-color:{color}; color:black; padding:3px 8px; border-radius:8px; font-size:13px;">{text}</span>'

def colored_number(value):
   try:
       val = float(value)
       if val < 60:
           color = "#668fd4"
       elif val < 80:
           color = "#fa9850"
       else:
           color = "#e4444e"
       return f'<span style="color:{color}; font-weight:bold;">{val:.1f}</span> bpm'
   except:
       return '<span style="color:gray;">N/A</span>'

# -------------------- ANALYTICAL SUMMARY --------------------
def generate_analytical_summary(filtered_df):
   if filtered_df.empty:
       return "⚠️ <em>No summary available due to current filters.</em>"

   avg_hr = filtered_df['Heart Rate'].mean()
   avg_sleep = filtered_df['Sleep Duration'].mean()
   top_occupation = (
       filtered_df['Occupation'].value_counts().idxmax()
       if not filtered_df['Occupation'].isnull().all()
       else None
   )

   summary = (
       f"🔹 The average heart rate recorded is {colored_number(avg_hr)}, reflecting overall cardiovascular activity in this group.<br><br>"
       f"🔹 Participants typically sleep around <strong style='color:#20B2AA'>{avg_sleep:.1f} hours</strong> per night, which can significantly impact their health and stress levels.<br><br>"
   )

   if top_occupation:
       summary += f"🔹 The most common profession is {badge(top_occupation, '#98A8D2')}, which may influence lifestyle and sleep patterns."
   else:
       summary += "🔹 Occupation data is not available for this selection."

   return summary

# -------------------- DEMOGRAPHIC INSIGHTS --------------------
def generate_demographic_insights(df):
   insights = ""

   if df.empty:
       return "⚠️ <em>No demographic data available based on current filters.</em>"

   if 'Gender' in df.columns and not df['Gender'].isnull().all():
       gender_stats = df.groupby('Gender', observed=False)['Heart Rate'].mean()
       insights += "<strong>🔸 Average Heart Rate by Gender:</strong><br>"
       for gender, hr in gender_stats.items():
           insights += f"- {gender}: {colored_number(hr) if pd.notna(hr) else '<span style=\"color:gray;\">No data</span>'}<br>"
   else:
       insights += "⚠️ Gender data is not available.<br>"

   if 'Age' in df.columns:
       df = df.copy()
       df = df[df['Age'] < 60] 
       df['Age Group'] = pd.cut(df['Age'], bins=[0, 25, 40, 60], labels=["<25", "25–40", "40–60"])
       group_stats = df.groupby('Age Group', observed=False)['Heart Rate'].mean()
       insights += "<br><strong>🔸 Heart Rate by Age Group:</strong><br>"
       for age_group, hr in group_stats.items():
           insights += f"- Age {age_group}: {colored_number(hr) if pd.notna(hr) else '<span style=\"color:gray;\">No data</span>'}<br>"

   return insights

# -------------------- DISPLAY SUMMARIES --------------------
st.markdown("---")
st.subheader(" Analytical Summary")
st.markdown("This analytical summary is displayed based on the chosen filter criteria")
col_a, col_b = st.columns(2)

with col_a:
   general_summary = generate_analytical_summary(filtered_df)
   st.markdown(
       f"""
       <div class="fade-in-section" style="padding:20px; background-color:#f9f9f9; border-left: 5px solid #9E122C; border-radius:10px; box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);">
           <h3 style="margin-top:0; color:#333;">📊 <strong>Key Observations</strong></h3>
           <p style="font-size:16px;">{general_summary}</p>
           <hr style="margin:15px 0;">
           <p style="font-size:14px;"><strong>🔻Legend:</strong><br>
               <strong>Heart Rate Colors:</strong>
               <span style="color:#668fd4; font-weight:bold;">Low &lt; 60 bpm</span> |
               <span style="color:#fa9850; font-weight:bold;">Moderate 60–79 bpm</span> |
               <span style="color:#e4444e; font-weight:bold;">High ≥ 80 bpm</span><br><br>
               <strong>Badge Highlight:</strong>
               <span style="background-color:#98A8D2; padding:3px 6px; border-radius:6px;">Top Occupation</span>
           </p>
       </div>
       """, unsafe_allow_html=True
   )

with col_b:
   demographic_summary = generate_demographic_insights(filtered_df)
   st.markdown(
       f"""
       <div class="fade-in-section" style="padding:20px; background-color:white; border-left: 5px solid #FBCB77; border-radius:10px; box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);">
           <h3 style="margin-top:0; color:#333;">🧠 <strong>Demographic Patterns</strong></h3>
           <p style="font-size:16px;">{demographic_summary}</p>
       </div>
       """, unsafe_allow_html=True
   )

# -------------------- RAW DATA --------------------
with st.expander("View Filtered Raw Data"):
   st.caption("Filtered dataset preview:")
   st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
