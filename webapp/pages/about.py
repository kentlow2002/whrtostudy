import streamlit as st

st.set_page_config(
    page_title="About Us",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("About Us")
st.header("Made for :red[students] by :red[students] :student:")
st.balloons()
st.subheader(":sparkles: Meet the team :sparkles:")
st.subheader("Code 606 @ Hack&Roll 2025")
st.subheader("Team Members:")

st.subheader("Kent :mechanic:")
st.link_button("LinkedIn", "https://streamlit.io/gallery")

st.subheader("Kabil :cook:")
st.link_button("LinkedIn", "https://streamlit.io/gallery")

st.subheader("Michell :artist:")
st.link_button("LinkedIn", "https://www.linkedin.com/in/michelltansq/")