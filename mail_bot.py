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

def send_email(account, fromaddr, toaddr, subject, body, verbosity=0):
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

def pop_connect(account, verbosity=0):
    connection = poplib.POP3_SSL(account.receiving_server, account.receiving_port)
    connection.set_debuglevel(verbosity)
    connection.user(account.username)
    connection.pass_(account.password)
    return connection

def pop_retrieve_all(connection, verbosity=0):
    num_emails = len(connection.list()[1]) # Get number of emails
    emails = [connection.retr(i+1) for i in xrange(0, num_emails)] # Get each one
    #if verbosity > 1:
    #    print emails
    return [email[1] for email in emails] # Remove extra crap like '+OK x bytes will follow', and keep the good parts

def receive_emails(account, verbosity=0):
    # Get POP connection
    connection = pop_connect(account, verbosity)
    emails = pop_retrieve_all(connection, verbosity)
    connection.quit() # End connection

    return emails

def delete_emails(account, unwanted_emails, verbosity=0):
    """Delete emails in unwanted_emails from server"""
    #print '\n\n\n\nUNWANTED:\n\n\n'+str(unwanted_emails)+'\n\n\n\n'
    # Let's see what emails are on the server    
    connection = pop_connect(account, verbosity)
    emails = pop_retrieve_all(connection)
    le = len(emails)
    unwanted_nums = [i for i in xrange(0, le) if emails[i] in unwanted_emails]
    print unwanted_nums
    # Let's connect to the server to start deleting    
    #map(connection.dele, unwanted_nums)
    for num in unwanted_nums:
        connection.dele(num+1) # Note that emails are 1-indexed
    connection.quit()

def match_emails(emails, criteria):
    """Returns a list of emails from the supplied list, whose headers match those in the "criteria" list"""
    for criterion in criteria:
        #emails = filter(lambda email: criterion in email, emails)
        emails = [email for email in emails if email.count(criterion) == 1]
    return emails


    
