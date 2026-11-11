from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Flask, request, render_template, redirect, url_for
from utils.file_processor import load_feedback_from_csv
from utils.classifier import classify_and_route
import re 
from dotenv import load_dotenv
import os
from utils.email_extractor import fetch_emails
from googletrans import Translator

load_dotenv()

app = Flask(__name__)

DEPARTMENT_EMAILS = {
    "administration": " ",
    "exam": " ",
    "finance": " ",
    "library": " ",
    "hostel": " ",
    "canteen": " ",
    "admission": " ",
    "transport": " ",
    "sports": " ",
    "trainig and placement": " "
}

def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.environ["SENDER_EMAIL"]
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(os.environ["SMTP_SERVER"], os.environ["SMTP_PORT"]) as server:
            server.starttls()
            server.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_PASSWORD"])
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
            recipient_email = DEPARTMENT_EMAILS.get(item['category'], os.environ["SENDER_EMAIL"])
            subject = f"New {item['category'].capitalize()} Complaint"
            body = f"Complaint Details:\n\n{item['feedback']}\n\nPlease address this issue in the {item['category']} department."
            send_email(recipient_email, subject, body)
    
    return render_template("results.html", results=results)

@app.route('/fetch_emails', methods=['GET'])
def fetch_emails_data():
    translator = Translator()

    def translate_if_needed(text):
        detected = translator.detect(text)
        if detected.lang in ['hi', 'mr', 'te']:
            translation = translator.translate(text, dest='en')
            return translation.text
        else:
            return text
        
    try:
        feedback_list = fetch_emails(os.environ["SENDER_EMAIL"], os.environ["SENDER_PASSWORD"])
        if not feedback_list:
            return "No new emails found or failed to extract feedback.", 400
        
        feedback_list_lang_change = []
        for list_item in feedback_list:
            feedback_list_lang_change.append(translate_if_needed(list_item))

        results = classify_and_route(feedback_list_lang_change)

        for item in results:
            recipient_email = DEPARTMENT_EMAILS.get(item['category'], os.environ["SENDER_EMAIL"])
            subject = f"New {item['category'].capitalize()} Complaint"
            body = f"Complaint Details:\n\n{item['feedback']}\n\nPlease address this issue in the {item['category']} department."
            send_email(recipient_email, subject, body)

        return render_template("results.html", results=results)

    except Exception as e:
        return f"Error fetching emails: {e}", 500
    

if __name__ == "__main__":
    app.run(debug=True)
