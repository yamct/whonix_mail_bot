import smtplib
import poplib
import logging
from email.mime.text import MIMEText
from email import parser

class Account:
    """Stores necessary info for sending and receiving email"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def sending_info(self, fromaddr, toaddr, server, port=25, encryption = 'SSL'):
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.smtp_server = server    
        self.smtp_port = port
        self.smtp_encryption = encryption

    def receiving_info(self, protocol, server, port, encryption = 'SSL'):
        self.receiving_server = server
        self.receiving_port = port
        self.receiving_encryption = encryption
        self.receiving_protocol = protocol                

def send_email(account, subject, body, verbosity=0):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = account.fromaddr
    msg['To'] = account.toaddr
    server = smtplib.SMTP_SSL(account.smtp_server, account.smtp_port)
    server.set_debuglevel(verbosity)
    server.login(account.username, account.password)
    logger = logging.getLogger('emailLogger') 
    print body
    try:
        server.sendmail(account.fromaddr, account.toaddr, msg.as_string())
        server.quit()        
        #logger.info('Sent email with body: \n%s' % (body))
        logger.info('Sent email')
    except smtplib.SMTPDataError:        
        logger.error('Failure to send email')


def pop_connect(account, verbosity=0):
    connection = poplib.POP3_SSL(account.receiving_server, account.receiving_port)
    connection.set_debuglevel(verbosity)
    connection.user(account.username)
    connection.pass_(account.password)    
    return connection

def pop_retrieve_all(connection, verbosity=0):
    num_emails = len(connection.list()[1]) # Get number of emails
    emails = [connection.retr(i+1) for i in xrange(0, num_emails)] # Get each one
    return [email[1] for email in emails] # Remove extra crap like '+OK x bytes will follow', and keep the good parts

def receive_emails(account, verbosity=0):
    # Get POP connection
    connection = pop_connect(account, verbosity)
    emails = pop_retrieve_all(connection, verbosity)
    connection.quit() # End connection
    logger = logging.getLogger('emailLogger')
    logger.info('Received %d emails' % (len(emails)))
    return emails

# Not working
def delete_emails(account, unwanted_emails, verbosity=0):
    """Delete emails in unwanted_emails from server"""
    # Let's see what emails are on the server    
    connection = pop_connect(account, verbosity)
    emails = pop_retrieve_all(connection)
    le = len(emails)
    unwanted_nums = [i for i in xrange(0, le) if emails[i] in unwanted_emails]
    print unwanted_nums
    # Let's connect to the server to start deleting    
    for num in unwanted_nums:
        connection.dele(num+1) # Note that emails are 1-indexed
    connection.quit()

def match_emails(emails, criteria):
    """Returns a list of emails from the supplied list, whose headers match those in the "criteria" list"""
    for criterion in criteria:
        emails = [email for email in emails if email.count(criterion) == 1]
    logger = logging.getLogger('emailLogger')
    logger.info('Received %d *useful* emails' % (len(emails)))
    return emails

def extract_subject(email):
    try:
        subject_header = filter(lambda header: 'Subject: ' in header, email)[0]
    except IndexError:
        return ''
    start = subject_header.index(' ')
    return subject_header[start+1:]

def extract_body(email):    
    email[email.index('Reply to this email directly or view it on GitHub:')] = "Do not reply, please respond directly on GitHub:"
    email = '\n'.join(email)
    start = email.index('>\n\n')
    email = email[start+3:]
    end = email.index('\n----==')
    return email[:end]


def clean_duplicates(emails):
    """Don't send emails that have already been sent"""
    try:
        fp = open('sent', 'r+')
        already_sent = fp.readlines()
        already_sent = [email.strip('\n') for email in already_sent]
    except IOError:
        fp = open('sent', 'w+')
        already_sent = []
    finally:
        fp.close()
    unsent = []
    for email_id in already_sent: # ignore already sent emails
        for email in emails:
            if email_id.strip('\n') in email:
                emails.remove(email)
                break
    logger = logging.getLogger('emailLogger')
    logger.info('Received %d *new* useful emails' % (len(emails)))
    return emails

def add_IDs(emails):
    """Add IDs of emails to sent"""
    emails = clean_duplicates(emails)
    fp = open('sent', 'r+')
    already_sent = fp.readlines()
    already_sent = [email.strip('\n') for email in already_sent]
    print already_sent
    for email in emails:
        already_sent += [header for header in email if 'Message-ID: <' in header] # add Message-ID to list of already sent
    print already_sent
    for ID in already_sent:
        fp.write(ID + '\n')
    fp.close()
                
        
    
