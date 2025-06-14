# --------- SIDEBAR: Age Filter ---------
st.sidebar.header("Filter by Age")
min_age = int(df['Age'].min())
max_age = int(df['Age'].max())

# Khởi tạo session_state nếu chưa có
if 'selected_age' not in st.session_state:
    st.session_state.selected_age = (min_age, max_age)
if 'filter_sleep_quality' not in st.session_state:
    st.session_state.filter_sleep_quality = False
if 'filter_high_hr' not in st.session_state:
    st.session_state.filter_high_hr = False

# Nút reset filter
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.selected_age = (min_age, max_age)
    st.session_state.filter_sleep_quality = False
    st.session_state.filter_high_hr = False
    st.rerun()

# Slider age range với session_state
selected_age = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=st.session_state.selected_age,
    key='selected_age'
)

# --------- ADVANCED FILTERS ---------
st.sidebar.markdown("### 🧪 Advanced Filters")
filter_sleep_quality = st.sidebar.checkbox(
    "Only Poor Sleepers (≤6)",
    value=st.session_state.filter_sleep_quality,
    key='filter_sleep_quality'
)
filter_high_hr = st.sidebar.checkbox(
    "Only High Heart Rate (>80 bpm)",
    value=st.session_state.filter_high_hr,
    key='filter_high_hr'
)

# --------- Filter dataset by Age and advanced filters ---------
filtered_df = df[(df['Age'] >= selected_age[0]) & (df['Age'] <= selected_age[1])]

if filter_sleep_quality:
   filtered_df = filtered_df[filtered_df['Quality of Sleep'] <= 6]
if filter_high_hr:
   filtered_df = filtered_df[filtered_df['Heart Rate'] > 80]
