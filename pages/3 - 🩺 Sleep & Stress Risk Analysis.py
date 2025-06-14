# ---------------- SIDEBAR FILTERS + RESET BUTTON ----------------
st.sidebar.title("Filters")

# Default filter values
default_genders = df['Gender'].dropna().unique().tolist()
default_disorders = DISORDER_ORDER
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
default_age_range = (min_age, max_age)

# Initialize session state values (only if not present)
if "selected_genders" not in st.session_state:
    st.session_state.selected_genders = []  # Không chọn gì lúc đầu
if "selected_disorders" not in st.session_state:
    st.session_state.selected_disorders = []  # Không chọn gì lúc đầu
if "age_range" not in st.session_state:
    st.session_state.age_range = default_age_range

# Reset button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.selected_genders = []
    st.session_state.selected_disorders = []
    st.session_state.age_range = default_age_range
    st.experimental_rerun()

# Sidebar inputs linked to session state, không chọn sẵn giá trị
st.sidebar.multiselect(
    "Select gender(s):",
    options=default_genders,
    default=st.session_state.selected_genders,
    key="selected_genders"
)

st.sidebar.multiselect(
    "Select disorder types:",
    options=DISORDER_ORDER,
    default=st.session_state.selected_disorders,
    key="selected_disorders"
)

st.sidebar.slider(
    "Select age range:",
    min_value=min_age,
    max_value=max_age,
    value=st.session_state.age_range,
    key="age_range"
)

# Áp dụng filter theo session_state
with st.spinner("Processing filters..."):
    time.sleep(0.5)
    # Nếu filter rỗng (gender hoặc disorder), thì không lọc theo trường đó
    filtered_df = df.copy()
    if st.session_state.selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(st.session_state.selected_genders)]
    if st.session_state.selected_disorders:
        filtered_df = filtered_df[filtered_df['Sleep Disorder'].isin(st.session_state.selected_disorders)]
    filtered_df = filtered_df[filtered_df['Age'].between(st.session_state.age_range[0], st.session_state.age_range[1])]
