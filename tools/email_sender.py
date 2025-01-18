import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    def __init__(
        self, email: str = "leetoanbk@gmail.com", password: str = "leetoanbk1234"
    ):
        self.email = email
        self.password = password

    def send(self, to, subject, message):
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, to, msg.as_string())
        server.quit()
