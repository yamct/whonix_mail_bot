from mail import *

if __name__=='__main__':
    criteria = ['Return-Path: <noreply@github.com>','Cc: WhonixTest <whonixtest@rambler.ru>', 'From: yamct <notifications@github.com>','Precedence: list', 'X-GitHub-Recipient: WhonixTest', 'X-KLMS-AntiSpam-Envelope-From: noreply@github.com', '---', 'Reply to this email directly or view it on GitHub:']
    # You need to first create an account here
    emails = receive_emails(account, 0)
    matches = match_emails(emails, criteria)
    #trash = [email for email in emails if email not in matches]
    contents = [(extract_subject(email), extract_body(email)) for email in matches]
    for email_content in contents:
        send_email(account, 'whonixtest@rambler.ru', 'yamct@rambler.ru', email_content[0], email_content[1], 0)
    
    
