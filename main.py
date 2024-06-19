import tkinter as tk
from tkinter import filedialog, ttk
from email_auth import authenticate
from email_fetch import connect_to_email, fetch_emails
from email_summarize import summarize_emails
from email_save import save_summaries

LABEL_MAPPING = {
    "inbox": "INBOX",
    "sent": "SENT",
    "drafts": "DRAFT",
    "spam": "SPAM",
    "trash": "TRASH",
    "important": "IMPORTANT",
    "starred": "STARRED",
    "unread": "UNREAD"
}

def summarize_emails_action(event=None):
    user_folder = folder_entry.get().lower()
    folder = LABEL_MAPPING.get(user_folder, user_folder)
    max_emails = 25
    creds = authenticate()

    service = connect_to_email(creds)
    if not service:
        return
    
    email_ids = fetch_emails(service, folder, max_emails)
    summaries = summarize_emails(service, email_ids)
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        save_summaries(summaries, file_path)
    
    folder_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Brief Mail")
tk.Label(root, text="Folder: ").grid(row=0, column=0, padx=10, pady=10)
folder_entry = tk.Entry(root, width=30)
folder_entry.grid(row=0, column=1, padx=10, pady=10)

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")
summarize_button = ttk.Button(root, text="Brief Mail", command=summarize_emails_action, style="TButton")
summarize_button.grid(row=1, column=0, columnspan=2, padx=10, pady=20)
root.bind('<Return>', summarize_emails_action)

root.mainloop()