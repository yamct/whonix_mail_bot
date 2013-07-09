import logging
import logging.config
from mail import *

def find_headers(emails):
    common_headers = emails[0]
    for email in emails:
        for header in common_headers:
            if header not in email: common_headers.remove(header)
    return common_headers
        
if __name__=='__main__':
    # You need to first create an account here
    account = Account(USERNAME, PASSWORD)    
    account.sending_info(smtp.yourdomainn.ame, port_number, 'SSL')
    account.receiving_info('POP', smtp.yourdomainn.ame, port_number, 'SSL')
    # Logging
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger('emailLogger')

    emails = receive_emails(account, 0)
    criteria = ['Return-Path: <noreply@github.com>', 'Cc: WhonixTest <whonixtest@rambler.ru>', '---', 'Reply to this email directly or view it on GitHub:']    
    matches = clean_duplicates(match_emails(emails, criteria))
    add_IDs(matches)
    for email in matches:
        subj = extract_subject(email)
        body = extract_body(email)
        send_email(account, 'whonixtest@rambler.ru', 'whonixtest@rambler.ru', subj, body, 0)
    
    
