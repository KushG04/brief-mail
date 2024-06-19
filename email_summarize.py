import base64
import email
from transformers import pipeline

def summarize_emails(service, email_ids):
    summarizer = pipeline("summarization")
    summaries = []

    for email_id in email_ids:
        try:
            msg = service.users().messages().get(userId='me', id=email_id, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)
            
            subject = mime_msg['subject']
            sender = mime_msg['from']
            date = mime_msg['date']
            
            body = ""
            if mime_msg.is_multipart():
                for part in mime_msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = mime_msg.get_payload(decode=True).decode()
            
            if body:
                print(f"Email ID: {email_id}\nSubject: {subject}\nBody: {body[:100]}...")
                truncated_body = body[:2000]
                summary = summarizer(truncated_body, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
                summaries.append(f"Subject: {subject}\nFrom: {sender}\nDate: {date}\nSummary: {summary}\n")
            else:
                print(f"no body found for email ID {email_id}")
        except Exception as e:
            print(f"error processing email ID {email_id}: {e}")
    
    return summaries