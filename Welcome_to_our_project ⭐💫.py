import streamlit as st
import base64

# PAGE CONFIG
st.set_page_config(page_title="🌙 Welcome – Understand Your Sleep", layout="wide", initial_sidebar_state="collapsed")

# Import Google Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Lato&family=Playfair+Display&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# BACKGROUND

def set_background_with_overlay(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(
            rgba(255, 246, 240, 0.85),
            rgba(255, 246, 240, 0.85)
        ),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        animation: fadeIn 1.5s ease-in-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    .block-container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem !important;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        animation: slideUp 1s ease-in-out;
    }}

    @keyframes slideUp {{
        from {{ transform: translateY(40px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 1rem 2rem;
        background-color: rgba(255, 246, 240, 0.95);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(200,180,170,0.5);
        animation: fadeInDown 1s ease;
    }}

    @keyframes fadeInDown {{
        from {{ transform: translateY(-20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    .navbar-title {{
        font-family: 'Playfair Display', serif;
        color: #a66f6f;
        font-size: 1.8rem;
        letter-spacing: 0.5px;
    }}

    .navbar-link {{
        font-family: 'Lato', sans-serif;
        color: #7a5c61;
        text-decoration: none;
        font-weight: 500;
        padding: 0.2rem 0.5rem;
        border-radius: 0.4rem;
        transition: background 0.3s ease;
    }}

    .navbar-link:hover {{
        background: rgba(122,92,97,0.1);
    }}

    .hero {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 1rem;
        padding: 3rem 2rem;
        margin: 6rem auto 3rem;
        border: 1px solid rgba(200,180,170,0.5);
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
        backdrop-filter: blur(8px);
        text-align: center;
        animation: slideUp 1.2s ease-in-out;
    }}

    .hero h1 {{
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #8b5e5e;
        margin-bottom: 2rem;
    }}

    .hero p {{
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        color: #5c4a4a;
        line-height: 1.6;
        margin-bottom: 1rem;
        text-align: left;
    }}

    .hero-button, div.stButton > button:first-child {{
        background: linear-gradient(
            to right,
            #ffd1dc,
            #ffe4c4
        );
        color: #5c4a4a;
        border: 1px solid rgba(140,110,110,0.3);
        border-radius: 2rem;
        padding: 0.8rem 2.5rem;
        font-family: 'Lato', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(140,110,110,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-top: 2rem;
        animation: fadeIn 2s ease;
    }}

    .hero-button:hover, div.stButton > button:first-child:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(140,110,110,0.15);
    }}

    @media screen and (max-width: 768px) {{
        .hero h1 {{ font-size: 2.2rem; }}
        .hero p {{ font-size: 1rem; }}
        .hero-button, div.stButton > button:first-child {{
            font-size: 1rem;
            padding: 0.6rem 1.8rem;
        }}
        .navbar-title {{ font-size: 1.4rem; }}
    }}
    </style>

    <div class="navbar">
        <div class="navbar-title">🛌 Sleep Health</div>
        <div><a class="navbar-link" href="?reset=true">🔙 Back to Welcome</a></div>
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)

def show_landing():
    st.markdown("""
        <div class="hero">
            <h1>Welcome to Sleep Health & Lifestyle</h1>
            <p>🧠 <strong>Sleep matters.</strong><br>
            Sleep plays a vital role in our cognitive performance, emotional balance, and overall health. Yet, many daily lifestyle factors — such as diet, physical activity, and routine habits — can significantly impact the quality of our rest.</p>
            <p>📚 <strong>About this project:</strong><br>
            This interactive web application is part of the final project for the <em>Business IT – Python for Data Science</em> course. It explores the Sleep Health and Lifestyle dataset to uncover meaningful patterns between everyday behaviors and sleep quality.</p>
            <p>💡 <strong>What you'll gain:</strong><br>
            Through visual insights and data-driven analysis, the app provides practical guidance for improving your sleep hygiene. Whether you're a student, researcher, or simply curious about the science of rest, this tool invites you to explore the balance between lifestyle and well-being.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("🚀 Let's Start", use_container_width=True):
            st.session_state.started = True
            st.rerun()

def show_main_app():
    st.switch_page("pages/1 - Homepage.py")

def main():
    set_background_with_overlay("cafe.jpg")

    if st.query_params.get("reset") == "true":
        st.session_state.started = False
        st.query_params.clear()

    if "started" not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        show_landing()
    else:
        show_main_app()

main()
