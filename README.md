# Reminder Email Bot

This is a Bot that was created to email members in the family gym plan to e-transfer the monthly amount to the payee 

This Bot was created using Python, HTML, CSS, Gmail API, and hosted using AWS EC2. The Bot runs on the 15th at 8am every month to ensure members are notified. To do this, a cronjob is created on the EC2 instance which can be viewed in example.crontab 

**Note:** Emails and recipients have been removed from the script for protection of the members. You will need to add them in yourself for the script to properly run 

## Tech Stack
* Python
* HTML
* CSS
* AWS EC2
* Gmail API

## Dependencies
* Gmail API 

**Installing dependencies**
```bash
$  pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
View more about getting started with the Gmail API at: https://developers.google.com/gmail/api/quickstart/python

## To Run
Make sure you've updated the recipients, emails and authenticated your email address. Once everything is updated, in the current directory, run
```bash
$  python3 remind_email.py
```
To have the output of the script saved into a log file
```bash
$  python3 remind_email.py >> remind_email_log.txt
```

## Screenshots
When the email is sent, this is what should show up in the inbox

HTML Version

![HTML Email](https://github.com/EltonK888/reminder_email_bot/blob/master/screenshots/email_image.PNG?raw=true) 


If HTML doesn't work on the email client, the plain text version should show 


![Plain Text Email](https://github.com/EltonK888/reminder_email_bot/blob/master/screenshots/email_image_plain.PNG?raw=true)
