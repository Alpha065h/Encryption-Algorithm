import tkinter as tk
from tkinter import filedialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class AudioSenderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Sender App")
        
        tk.Label(master, text="Select Audio File:").pack()
        self.file_path = tk.StringVar()
        tk.Entry(master, textvariable=self.file_path, state='readonly').pack(side=tk.LEFT)
        tk.Button(master, text="Browse", command=self.browse_file).pack(side=tk.RIGHT)
        
        tk.Label(master, text="Recipient's Email:").pack()
        self.recipient_email = tk.StringVar()
        tk.Entry(master, textvariable=self.recipient_email).pack()
        
        tk.Button(master, text="Send Audio", command=self.send_audio).pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        self.file_path.set(file_path)

    def send_audio(self):
        # Use a regular string as the key
        key = "1keyrection"

        with open(self.file_path.get(), 'rb') as audio_file:
            encrypted_audio = self.encrypt_audio(audio_file.read(), key)

        self.send_email(encrypted_audio)

    def encrypt_audio(self, data, key):
        # Simple method to concatenate the key with the data
        encrypted_data = key.encode() + data
        return encrypted_data

    def send_email(self, encrypted_audio):
        sender_email = "tsunasawada0011@gmail.com"  # Update with your email
        sender_password = "fbag tasi uotw rjwr"  # Update with your password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = self.recipient_email.get()
        msg['Subject'] = "Encrypted Audio File"

        msg.attach(MIMEText("This email contains an encrypted audio file."))

        audio_part = MIMEBase('application', 'octet-stream')
        audio_part.set_payload(encrypted_audio)
        encoders.encode_base64(audio_part)
        audio_part.add_header('Content-Disposition', 'attachment; filename="encrypted_audio.bin"')
        msg.attach(audio_part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.recipient_email.get(), msg.as_string())

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSenderApp(root)
    root.mainloop()
