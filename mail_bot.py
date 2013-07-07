import smtplib
import poplib
from email.mime.text import MIMEText

class Account:
    """Stores necessary info for sending and receiving email"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def sending_info(self, server, port=25, encryption = 'SSL'):
        self.smtp_server = server    
        self.smtp_port = port
        self.smtp_encryption = encryption

    def receiving_info(self, protocol, server, port, encryption = 'SSL'):
        self.receiving_server = server
        self.receiving_port = port
        self.receiving_encryption = encryption
        self.receiving_protocol = protocol                

def send_email(account, fromaddr, toaddr, subject, body, verbosity=1):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    server = smtplib.SMTP_SSL(account.smtp_server, account.smtp_port)
    server.set_debuglevel(verbosity)
    server.login(account.username, account.password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    return 'Email Sent'

def receive_emails(account, verbosity=1):
    M = poplib.POP3_SSL(account.receiving_server, account.receiving_port)
    M.set_debuglevel(verbosity)
    M.user(account.username)
    M.pass_(account.password)
    num_emails = len(M.list()[1])
    emails = [M.retr(i+1) for i in xrange(0, num_emails)]
    M.quit()
    if verbosity == 1:
        print emails
    return [email[1] for email in emails] # Remove extra crap like '+OK x bytes will follow', and keep the good parts

def match_emails(emails, criteria):
    """Returns a list of emails from the supplied list, whose headers match those in the "criteria" list"""
    for criterion in criteria:
        #emails = filter(lambda email: criterion in email, emails)
        emails = [email for email in emails if email.count(criterion) == 1]
    return emails

    

#def delete_emails(account, emails, verbosity=1):
    
