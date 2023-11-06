from PRIVATE import send_mail
from dotenv import load_dotenv
import os

load_dotenv()


# Επόμενο 5

def run(path_to_file, file_name, html_file):
    """
        Prepares and sends an email. The email server and recipients are specified using
        environment variables ("main_mail", "store_mail" and "subject").

        The mail content includes a HTML fixture and attachment file.

        Args:
            path_to_file (str): The path to the attachment file.
            file_name (str): The name of the attachment file.
            html_file (str): The path to a HTML file for the email content body.

        Note:
            The environment variables "main_mail", "store_mail" and "subject"
            should be set before running this function.
    """

    mail_lst = [os.getenv("main_mail"),
                os.getenv("store_mail")
                ]
    mail_names = [os.getenv("subject"),
                  os.getenv("subject"),
                  ]

    # -------------------- OPEN HTML FILE FOR THE BODY MAIL --------------------
    with open(html_file, 'r') as html_file:
        word = html_file.read()

    # -------------------- SEND MAIL --------------------
    send_mail.send_mail(mail_lst, mail_names, word, path_to_file, file_name)
