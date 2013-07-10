#!/usr/bin/python
import logging
import logging.config
import ConfigParser
from mail import *

def main(account):
    emails = receive_emails(account, 0)
    #github_username = Config.get('github', 'username')
    criteria = ['Return-Path: <noreply@github.com>', 'Cc: %s <%s>' % (get_github_username(), account.fromaddr), '---', 'Reply to this email directly or view it on GitHub:']    
    matches = clean_duplicates(match_emails(emails, criteria))
    print matches
    add_IDs(matches)
    for email in matches:
        subj = extract_subject(email)
        body = extract_body(email)
        send_email(account, subj, body, 0)



def get_config(configfile='bot.conf'):
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    return Config

def get_account(configfile='bot.conf'):
    # Get the account info from bot.conf
    Config = get_config(configfile)
    email_username = Config.get('emailAccount', 'username')
    email_password = Config.get('emailAccount', 'password')    
    account = Account(email_username, email_password)    
    fromaddr =  Config.get('emailAccount', 'fromaddr')
    toaddr = Config.get('emailAccount', 'toaddr')
    smtp_server = Config.get('emailAccount', 'smtpServer')
    smtp_port = Config.get('emailAccount', 'smtpPort')
    account.sending_info(fromaddr, toaddr, smtp_server, smtp_port, 'SSL')
    pop_server = Config.get('emailAccount', 'popServer')
    pop_port = Config.get('emailAccount', 'popPort')
    account.receiving_info('POP', pop_server, pop_port, 'SSL')
    return account

def get_github_username(configfile='bot.conf'):
    Config = get_config(configfile)
    return Config.get('github', 'username')

if __name__=='__main__':
    account = get_account()    
    # Logging
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger('emailLogger')
    while True:
        main(account)
        break
