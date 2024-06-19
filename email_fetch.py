import googleapiclient.discovery

def connect_to_email(creds):
    try:
        service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print("failed to connect to Gmail API: ", e)
        return None

def fetch_emails(service, folder="INBOX", max_emails=25):
    try:
        results = service.users().messages().list(userId='me', labelIds=[folder], maxResults=max_emails).execute()
        messages = results.get('messages', [])
        return [msg['id'] for msg in messages]
    except Exception as e:
        print("error fetching emails: ", e)
        return []