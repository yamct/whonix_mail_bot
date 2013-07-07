import smtplib
import poplib

def send_email(fromaddr, toaddr, username, password, content, server, port, verbosity=1):
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddr.split())))
    msg += content
    server = smtplib.SMTP_SSL(server,port)
    server.set_debuglevel(verbosity)
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()
    return 'Email Sent'

def receive_emails(username, password, server, port, protocol='POP', encryption='SSL',verbosity=1):
    M = poplib.POP3_SSL(server, port)
    M.set_debuglevel(verbosity)
    M.user(username)
    M.pass_(password)
    num_messages = len(M.list()[1])
    messages = [M.retr(i+1) for i in xrange(0, num_messages)]
    print messages          
    return messages

def delete_emails(username, password, server, port, protocol='POP', encryption='SSL',verbosity=1):

