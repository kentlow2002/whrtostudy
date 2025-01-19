import streamlit as st
from db import push_email

st.set_page_config(
    page_title="About Us",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

left,middle,right = st.columns(3)
if left.button(label="About",use_container_width=True):
    st.switch_page("pages/about.py")
middle.link_button(label="Github",url="https://github.com/kentlow2002/whrtostudy",use_container_width=True)
if right.button(label="Home",use_container_width=True):
    st.switch_page("home.py")

st.title("About Us")
st.header("Made for :red[students] by :red[students] :student:")
st.balloons()
st.subheader(":sparkles: Meet the team :sparkles:")
st.subheader("Code 606 @ Hack&Roll 2025")
st.subheader("Team Members:")

st.subheader("Kent :mechanic:")
st.link_button("LinkedIn", "https://www.linkedin.com/in/kent-low-09b383186/")

st.subheader("Kabil :cook:")
st.link_button("LinkedIn", "https://www.linkedin.com/in/kabileswaran")

st.subheader("Michell :artist:")
st.link_button("LinkedIn", "https://www.linkedin.com/in/michelltansq/")

st.subheader("Leave a message! 📬")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
with st.form("message_form"):
    category = st.selectbox(
        "Category",
        ["Feedback", "Complaint", "Suggestion", "Inquiry", "Other"],
        help="Select the category of your message."
    )
    message = st.text_area("Message", placeholder="Type your message here...", height=200)
    email = st.text_input("Your Email (Optional)", placeholder="Enter your email (optional)")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not message.strip():
            st.error("Please enter a message before submitting.")
        else:
            sender_email = "whrtostudy@gmail.com"
            sender_password = "Whr2Study?"
            recipient_email = "whrtostudy@gmail.com"
            subject = f"New Message: {category}"

            email_message = MIMEMultipart()
            email_message["From"] = sender_email
            email_message["To"] = recipient_email
            email_message["Subject"] = subject

            body = f"Category: {category}\n\nMessage:\n{message}\n\n"
            if email:
                body += f"User's Email: {email}"
                push_email(email, subject, body)
            else:
                push_email('anonymous', subject, body)

            st.success("We welcome feedback with open arms 🤗")