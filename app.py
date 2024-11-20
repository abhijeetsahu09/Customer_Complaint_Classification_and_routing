from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Flask, request, render_template, redirect, url_for
from utils.file_processor import load_feedback_from_csv
from utils.classifier import classify_and_route
import re 

app = Flask(__name__)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'testing.g16.project@gmail.com'
SENDER_PASSWORD = 'wrwwojlsosmegyex'

DEPARTMENT_EMAILS = {
    "Administration": "abhijeetsahu937@gmail.com",
    "Exam": "abhijeetsahu937@gmail.com",
    "Finance": "abhijeetsahu937@gmail.com",
    "Library": "abhijeetsahu937@gmail.com",
    "Hostel": "abhijeetsahu937@gmail.com",
    "Canteen": "abhijeetsahu937@gmail.com"
}

def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400
    
    feedback_list = load_feedback_from_csv(file)
    
    results = classify_and_route(feedback_list)

    for item in results:
            recipient_email = DEPARTMENT_EMAILS.get(item['category'], SENDER_EMAIL)
            subject = f"New {item['category'].capitalize()} Complaint"
            body = f"Complaint Details:\n\n{item['feedback']}\n\nPlease address this issue in the {item['category']} department."
            send_email(recipient_email, subject, body)
    
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
