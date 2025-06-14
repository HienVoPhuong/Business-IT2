# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.title("Filters")

# Define defaults
default_genders = df['Gender'].dropna().unique().tolist()
default_disorders = DISORDER_ORDER
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
default_age_range = (min_age, max_age)

# Initialize/reset session state
if 'filters' not in st.session_state or st.sidebar.button("🔄 Reset Filters"):
    st.session_state.filters = {
        "genders": default_genders,
        "disorders": default_disorders,
        "age_range": default_age_range
    }

# Filter widgets that update session state
selected_genders = st.sidebar.multiselect("Select gender(s):", options=df['Gender'].dropna().unique().tolist(), default=st.session_state.filters["genders"])
selected_disorders = st.sidebar.multiselect("Select disorder types:", options=DISORDER_ORDER, default=st.session_state.filters["disorders"])
age_range = st.sidebar.slider("Select age range:", min_age, max_age, st.session_state.filters["age_range"])

# Update session state with current selection
st.session_state.filters["genders"] = selected_genders
st.session_state.filters["disorders"] = selected_disorders
st.session_state.filters["age_range"] = age_range
