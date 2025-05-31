import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_lottie import st_lottie
import base64
import time
import json
from streamlit.components.v1 import html

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sleep Health & Lifestyle", page_icon="🛌", layout="wide")

# --- MUSIC BACKGROUND ---
def get_audio_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

audio_base64 = get_audio_base64("lofi.mp3")  # Ensure this file exists in the same folder
audio_html = f"""
<audio autoplay loop>
    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
</audio>
"""
st.markdown(audio_html, unsafe_allow_html=True)

# --------- Font Styling ---------
st.markdown("""
   <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
   <link href="https://fonts.googleapis.com/css2?family=Lobster&display=swap" rel="stylesheet">
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
       .colatin-title {
           font-family: 'Lobster', cursive !important;
           font-size: 3.5em;
           font-weight: 700;
           text-align: center;
           background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           padding: 40px;
           border-radius: 12px;
       }
   </style>
""", unsafe_allow_html=True)

st.markdown('''
   <div class="fade-in-section">
       <h1 style='text-align: center;
                  background: -webkit-linear-gradient(45deg, #6C63FF, #20B2AA);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  font-weight: 750;
                  font-size: 4.5em; 'class="colatin-title">Sleep Health and Lifestyle</h1>
   </div>
''', unsafe_allow_html=True)

st.markdown(
   """
   <p style='
       text-align: center;
       font-size:25px;
       font-family: "Merriweather", serif;
       font-weight: 400;
   '>
      A Data Project in Business IT 2
   </p>
   """,
   unsafe_allow_html=True)

# --- LOTTIE LOADER ---
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# --- RAIN EFFECT ---
rain(emoji="💤", font_size=44, falling_speed=5, animation_length="2")

# --- INTRO WITH TYPING ---
with st.empty():
    for line in [
        "We analyze how sleep patterns correlate with well-being.",
        "Data meets wellness through interactive insights.",
        "A visual exploration of sleep data — discover patterns, trends, and insights from real-world sources."
    ]:
        st.write(f"### ✨ {line}")
        time.sleep(1.5)

# --- HEADER ANIMATION ---
lottie_animation = load_lottie_file("sleepy.json")
st_lottie(lottie_animation, height=300, key="header_lottie")

# --- TEAM SECTION ---
st.markdown("<div id='team'></div>", unsafe_allow_html=True)
st.subheader("👨‍💻 Our Team")

team = [
    {"name": " Võ Phương Hiền", "id": "106240134", "image": "Hien.jpg"},
    {"name": " Đoàn Mai Khánh Ngọc", "id": "103240413", "image": "Ngoc.jpg"},
    {"name": " Nguyễn Thụy Vân Quỳnh", "id": "106240331", "image": "quynh.jpg"},
    {"name": " Phạm Gia Linh", "id": "103240155", "image": "linh.jpg"},
    {"name": " Võ Anh Kiệt", "id": "106240395", "image": "kiet.jpg"}
]

team_html = """
<style>
.team-wrapper {
    display: grid;
    place-items: center;
    overflow-x: auto;
    padding-bottom: 1rem;
    width: 100%;
}
.team-container {
    display: flex;
    flex-wrap: nowrap;
    gap: 1.2rem;
    min-width: max-content;
}
.team-card {
    flex: 0 0 auto;
    width: 220px;
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s;
}
.team-card:hover {
    transform: scale(1.06);
}
.team-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
.team-card h4 {
    margin: 10px 0 5px 0;
    font-weight: 700;
    font-size: 1.1rem;
    color: #333;
}
.team-card p {
    font-style: italic;
    margin-bottom: 10px;
    font-size: 1.1rem;
    color: #777;
}
</style>
<div class='team-wrapper'>
<div class='team-container'>
"""

for member in team:
    try:
        with open(member["image"], "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        img_src = f"data:image/jpeg;base64,{img_base64}"
    except:
        img_src = "https://via.placeholder.com/220x220.png?text=No+Image"

    team_html += f"""
    <div class='team-card'>
        <img src="{img_src}" alt="{member['name']}">
        <h4>{member['name']}</h4>
        <p>{member['id']}</p>
    </div>
    """

team_html += "</div></div>"
html(team_html, height=350, scrolling=False)

# --- CONTACT SECTION ---
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.subheader("📬 Contact Us")
st.caption("Got a question or feedback? We’d love to hear from you!")

contact_animation = load_lottie_file("contact.json")
st_lottie(contact_animation, height=200, key="contact_anim")

st.markdown("""
<div style='background-color: rgba(255, 245, 230, 0.9); padding: 30px; border-radius: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.1); max-width: 600px; margin: auto; animation: bounceIn 1.2s;'>
    <form action="https://formsubmit.co/106240134@student.vgu.edu.vn" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required style='margin-bottom: 10px; width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #ccc;'>
        <input type="email" name="email" placeholder="Your email address" required style='margin-bottom: 10px; width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #ccc;'>
        <textarea name="message" placeholder="Your message or feedback..." rows="5" required style='margin-bottom: 10px; width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #ccc;'></textarea>
        <button type="submit" style='background-color: #ff9966; color: white; padding: 12px 25px; border: none; border-radius: 12px; font-weight: bold; cursor: pointer;'>
            📨 Send
        </button>
    </form>
</div>
""", unsafe_allow_html=True)
