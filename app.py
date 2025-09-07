import streamlit as st

st.title("Traffic Light Detection")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi"])

if uploaded_video:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_video.getbuffer())
    st.video("temp_video.mp4")

    # Add your traffic light detection code here, and show results
    st.write("Processing video...")
