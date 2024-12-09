import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.constants.email import *
import os


def sendEmail(receiver_email,use_case,placeholders):
    # Email details

    password = os.getenv("EMAIL_PASSWORD")  # Use App Passwords for Gmail for better security
    
    email_template=EMAIL_TEMPLATES.get(use_case)
    if not email_template:
            raise ValueError(f"No email template found for use case: {use_case}")
        
    subject = email_template["subject"]
    body = email_template["body"].format(**placeholders)


    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, password)  # Log in
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())  # Send the email
            print("Email sent successfully!")
            return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

# Call the function
# sendEmail()
