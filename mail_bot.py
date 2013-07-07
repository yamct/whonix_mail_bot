import smtplib
import poplib


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

def send_email(account, fromaddr, toaddr, content, verbosity=1):
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddr.split())))
    msg += content
    server = smtplib.SMTP_SSL(account.smtp_server, account.smtp_port)
    server.set_debuglevel(verbosity)
    server.login(account.username, account.password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()
    return 'Email Sent'

def receive_email(account, verbosity=1):
    M = poplib.POP3_SSL(account.receiving_server, account.receiving_port)
    M.set_debuglevel(verbosity)
    M.user(account.username)
    M.pass_(account.password)
    num_messages = len(M.list()[1])
    messages = [M.retr(i+1) for i in xrange(0, num_messages)]
    M.quit()
    if verbosity == 1:
        print messages
    return messages

def delete_emails(account, verbosity=1):
    
