from __future__ import print_function
import base64
import datetime
import email_messages

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
HTML_MESSAGE = email_messages.html_message # HTML formatted version of the email message
PLAIN_MESSAGE = email_messages.plain_message # plain text version of email message


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


def create_message(sender, to, subject, message_text_html, message_text_plain):
    """Create a message in HTML and plain text for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('alternative')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message_html = MIMEText(message_text_html, 'html') # HTML version
    message_plain = MIMEText(message_text_plain) # plain text version
    message.attach(message_plain)
    message.attach(message_html)
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
        body_html = HTML_MESSAGE.format(PAYEE)
        body_plain_txt = PLAIN_MESSAGE.format(PAYEE)
        msg = create_message(FROM_EMAIL, recipients, subject, body_html, body_plain_txt)
        send_message(service, "me", msg)
        print("email sent successfully")
    except:
        print("error, something went wrong.")
    print("--------------------------------------------------------------")


if __name__ == '__main__':
    main()
