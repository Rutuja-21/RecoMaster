import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

remail = os.getenv("email")
spassword = os.getenv("password")

def send_email(sender_email, sender_name, message_content):
    # Email configuration
    receiver_email = remail  # Your email address to receive contact requests
    sender_password = spassword      # You might need to create an app password if using Gmail

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Contact Us Form: {sender_name}"
    
    # Email body
    body = f"Sender Name: {sender_name}\nSender Email: {sender_email}\n\nMessage:\n{message_content}"
    msg.attach(MIMEText(body, 'plain'))
    
    # SMTP server setup (this example uses Gmail's SMTP)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(receiver_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# Streamlit Contact Form
st.title("Contact Us")

# Form for user input
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message")
    
    submitted = st.form_submit_button("Send Message")
    
    # If the form is submitted, send the email
    if submitted:
        if name and email and message:
            success = send_email(email, name, message)
            if success:
                st.success("Your message has been sent successfully!")
        else:
            st.error("Please fill out all fields.")
