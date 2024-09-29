import streamlit as st
import pyodbc
import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

semail = os.getenv("email")
spassword = os.getenv("password")

# Function to connect to the SQL Server
def init_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-OJD0AB2\\SQLEXPRESS;'  # Adjust server as needed
        'DATABASE=RecoMaster;'
        'Trusted_Connection=yes;'
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if email exists
def check_email_exists(email):
    conn = init_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    data = cursor.fetchone()
    conn.close()
    return data is not None

# Function to generate a random password
def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Function to update password in the database
def update_password(email, new_password):
    conn = init_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(new_password)
    cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
    conn.commit()
    conn.close()

# Function to send email with the temporary password
def send_email(recipient_email, temp_password):
    sender_email = semail  
    sender_password = spassword  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use port 587 for TLS

    subject = "Your Password"
    body = f"Your new password is: {temp_password}\nPlease log in with new password."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit UI for Forgot Password
st.title("Forgot Password")

email = st.text_input("Enter your email address")

if st.button("Reset Password"):
    if email:
        if check_email_exists(email):
            # Generate a temporary password
            temp_password = generate_temp_password()
            # Update the password in the database
            update_password(email, temp_password)
            # Send email to the user
            if send_email(email, temp_password):
                st.success("A new password has been generated and sent to your email.")
            else:
                st.error("Failed to send the email. Please try again later.")
        else:
            st.error("No account found with that email address.")
    else:
        st.error("Please enter your email address.")
