from __future__ import print_function
import base64
import datetime

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mimetypes
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import recipients_emails


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
TO_EMAILS = recipients_emails.RECIPIENTS  # list of emails to send message to
FROM_EMAIL = recipients_emails.FROM_EMAIL # the email address sending the message
PAYEE = recipients_emails.PAYEE  # the payee's email
DATE = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S") # get current time that the script will run


def create_credentials():
    """
    Creates and returns credentials that the user logs in with
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'html')  # text type html for message formatting
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except:
        print('An error occurred')


def main():
    """
    Sends an email to all emails in TO_EMAILS
    """
    print("-------This script was run on %s--------" % DATE)
    try:
        creds = create_credentials()  # creates a token with credentials for the bot

        service = build('gmail', 'v1', credentials=creds)  # creates the service to interact with the Gmail API

        recipients = ", ".join(TO_EMAILS)
        subject = "Gym Family Plan"
        body = """
        Hi everyone!
        <br>
        <br>
        It is that time of the month again where we must fork over <b>$31.00</b> to Felix Kenji Yan for our Iron Fitness Family Plan membership.
        <br>
        <br>
        <b>Please e-transfer $31.00 to the provided email address: {}</b>
        <br>
        <br>
        If you would like to cancel your membership, please let everyone know in the group chat and Felix will take care of the administration issues.
        <br>
        <br>
        From,
        <br>
        <br>
        Reminder Bot
        <br>
        <br>
        Beep Boop I am a bot created by Elton Kok. If there is an issue please let him know.
        <br>
        View my source code on github at https://github.com/EltonK888/reminder_email_bot
        """.format(PAYEE)
        msg = create_message(FROM_EMAIL, recipients, subject, body)
        send_message(service, "me", msg)
        print("email sent successfully")
    except:
        print("error, something went wrong.")
    print("--------------------------------------------------------------")


if __name__ == '__main__':
    main()
