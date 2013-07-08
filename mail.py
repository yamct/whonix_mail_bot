import smtplib
import poplib
from email.mime.text import MIMEText
from email import parser
#import cPickle

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

def send_email(account, fromaddr, toaddr, subject, body, verbosity=0, mime_text=''):
    if mime_text == '':
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
        #emails = filter(lambda email: criterion in email, emails)
        emails = [email for email in emails if email.count(criterion) == 1]
        #print emails
        #print '\n\n'
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
    """try:
        pickle_file = open('pickle', 'r')
        already_sent = cPickle.load(pickle_file)
        pickle_file.close()
    except:
        already_sent= []
    """
    try:
        fp = open('sent', 'r+')
        already_sent = fp.readlines()
    except IOError:
        fp = open('sent', 'w+')
        already_sent = []
    finally:
        fp.close()
    unsent = []
    for email_id in already_sent: # ignore already sent emails
        for email in emails:
            print email[12]
            print email_id.strip('\n')
            print email_id.strip('\n') == email[12]
            #print email_id.strip('\n')
            if email_id.strip('\n') in email:
                emails.remove(email)
                break
            

        #emails = [email for email in emails if email_id.strip('\n') not in email]
        #print unsent
    print emails    
    assert emails == []
    return emails

def add_IDs(emails):
    """Add IDs of emails to sent"""
    emails = clean_duplicates(emails)
    """try:
        pickle_file = open('pickle', 'r+')
        already_sent = cPickle.load(pickle_file)
    except EOFError:
        already_sent = []
    """
    fp = open('sent', 'w+')
    already_sent = fp.readlines()
    for email in emails: 
        already_sent += [header for header in email if 'Message-ID: <' in header] # add Message-ID to list of already sent
    for ID in already_sent:
        fp.write(ID + '\n')
    fp.close()
    #cPickle.dump('pickle', pickle_file)
    #pickle_file.close()    
                
        
    
