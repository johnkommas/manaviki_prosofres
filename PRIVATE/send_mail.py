#  Copyright (c) Ioannis E. Kommas 2023. All Rights Reserved
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()


def a_gmail(email_send, subj, word, path_to_file, output_file):
    """
        Sends an email with an attachment using Gmail.

        This function reads credentials from the environment and uses them to send an email through the
        smtp.gmail.com SMTP server. The email includes an HTML body and an attachment, both specified by
        the user.

        Parameters:
        email_send (str): The email address to send the email to.
        subj (str): The subject of the email.
        word (str): The content of the email body in HTML format.
        path_to_file (str): The path to the file to attach to the email.
        output_file (str): The name for the attached file in the email.

        Returns:
        None

        Side Effects:
        - Sends an email via the Gmail SMTP server.
        - Prints a notification message upon successful sending of the email.

    """
    email_user = os.getenv('email_user')
    email_password = os.getenv('email_password')
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_send
    msg["Subject"] = subj
    body = word
    msg.attach(MIMEText(body, "html"))
    attachment = open(path_to_file, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= " + output_file)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    print(" Το e-mail {} στάλθηκε επιτυχώς".format(email_send))


# ----------------MAIN PROGRAM--------------------
def send_mail(mail_lst, mail_names, word, path_to_file, output_file):
    """
    Sends an email to each recipient in mail_lst. The email's subject and body message
    are personalizable, and an attachment file is included.

    Args:
        mail_lst (list): List of recipients e-mail addresses.
        mail_names (list): List of subjects for the emails, one for each recipient.
        word (str): The body message of the email.
        path_to_file (str): The path to the file to be attached to the email.
        output_file (str): The name of the attachment file.

    This function iterates over each recipient from mail_lst, sending one email at a time.
    An attached file and a custom subject, body message is included in each email.

    Note:
        This function uses a helper function, a_gmail, which is not included in this code snippet.
        a_gmail is in charge of the actual email sending process.
    """
    for i in range(len(mail_lst)):
        c = "S: {}".format(mail_names[i])
        print("Αποστολή μηνύματος στον παραλήπτη {}".format(mail_names[i]))
        a_gmail(mail_lst[i], c, word, path_to_file, output_file)
