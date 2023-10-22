import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        recipients_list.delete(0, tk.END)
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                recipients_list.insert(tk.END, row[0])

def send_emails():
    smtp_server = smtp_server_entry.get()
    smtp_port = int(smtp_port_entry.get())
    email_address = email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    message = message_text.get("1.0", tk.END)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, password)

        for recipient in recipients_list.get(0, tk.END):
            recipient_email = recipient.strip()
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(email_address, recipient_email, msg.as_string())

        server.quit()
        status_label.config(text="Emails sent successfully", foreground="green")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", foreground="red")

# Create the main application window
root = tk.Tk()
root.title("Mass Email Sender")

# Create and layout GUI elements
frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="SMTP Server:").grid(column=0, row=0, sticky=tk.W)
smtp_server_entry = ttk.Entry(frame)
smtp_server_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
smtp_server_entry.insert(0, 'smtp.gmail.com')

ttk.Label(frame, text="SMTP Port:").grid(column=0, row=1, sticky=tk.W)
smtp_port_entry = ttk.Entry(frame)
smtp_port_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))
smtp_port_entry.insert(0, '587')

ttk.Label(frame, text="Your Email:").grid(column=0, row=2, sticky=tk.W)
email_entry = ttk.Entry(frame)
email_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Password:").grid(column=0, row=3, sticky=tk.W)
password_entry = ttk.Entry(frame, show='*')
password_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Subject:").grid(column=0, row=4, sticky=tk.W)
subject_entry = ttk.Entry(frame)
subject_entry.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Message:").grid(column=0, row=5, sticky=tk.W)
message_text = tk.Text(frame, height=5)
message_text.grid(column=1, row=5, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Recipient List:").grid(column=0, row=6, sticky=tk.W)
recipients_list = tk.Listbox(frame, selectmode=tk.EXTENDED, height=5)
recipients_list.grid(column=1, row=6, sticky=(tk.W, tk.E))

browse_button = ttk.Button(frame, text="Browse CSV", command=browse_file)
browse_button.grid(column=2, row=6, sticky=tk.W)

send_button = ttk.Button(frame, text="Send Emails", command=send_emails)
send_button.grid(column=1, row=7, sticky=tk.W)

status_label = ttk.Label(frame, text="", foreground="green")
status_label.grid(column=0, row=8, columnspan=3, sticky=(tk.W, tk.E))

# Start the Tkinter main loop
root.mainloop()
