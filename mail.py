"""Simplifies creation and sending complex email."""

from mimetypes import guess_type
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP
    
    
def make(from_email, to_email, subject, 
         text=None, html=None, attachment=None):
    if text:
        text_msg =  MIMEText(text, 'plain', 'utf-8')
    if html:
        html_msg = MIMEText(html, 'html', 'utf-8')
    if attachment:
        ctype, encoding = guess_type(attachment['name'])
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype != 'application':
            maintype, subtype = 'application', 'octet-stream'
        attached_msg = MIMEApplication(attachment['data'], subtype)
        attached_msg.add_header('Content-Disposition', 'attachment', 
                                filename = attachment['name'])
    
    if text and html:
        alter_msg = MIMEMultipart('alternative')
        alter_msg.attach(text_msg)
        alter_msg.attach(html_msg)
        msg = alter_msg
    elif text:
        msg = text_msg
    elif html:
        msg = html_msg
    else:
        msg = MIMEText('', 'plain')
        
    if attachment:
        content_msg = msg
        msg = MIMEMultipart()
        msg.attach(content_msg)
        msg.attach(attached_msg)
        
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    return msg
    
    
def send(msg):
    s = SMTP('localhost')
    s.send_message(msg)
    s.quit()