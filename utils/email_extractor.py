import imaplib
import email
from email.header import decode_header

def fetch_emails(username, password, folder='inbox', subject_filter="Complaint"):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select(folder)
    
    status, messages = mail.search(None, f'SUBJECT "{subject_filter}"')
    email_ids = messages[0].split()
    complaints = []
    
    for e_id in email_ids[-5:]:
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            complaints.append(part.get_payload(decode=True).decode())
                else:
                    complaints.append(msg.get_payload(decode=True).decode())

    mail.logout()
    return complaints