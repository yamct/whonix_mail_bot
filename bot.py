from mail import *

def find_headers(emails):
    common_headers = emails[0]
    for email in emails:
        for header in common_headers:
            if header not in email:
                common_headers.remove(header)
    return common_headers
        
if __name__=='__main__':
    criteria = ['Return-Path: <noreply@github.com>', 'Cc: WhonixTest <whonixtest@rambler.ru>', '---', 'Reply to this email directly or view it on GitHub:']
#, 'Mime-Version: 1.0', 'Content-Type: multipart/alternative;', ' charset=UTF-8', 'Content-Transfer-Encoding: 7bit', 'Precedence: list', 'X-GitHub-Recipient: WhonixTest', 'X-GitHub-Recipient-Address: whonixtest@rambler.ru', 'X-KLMS-AntiSpam-Envelope-From: noreply@github.com', 'X-KLMS-AntiSpam-Method: none', '', '', '', 'Mime-Version: 1.0', 'Content-Type: text/plain;', ' charset=UTF-8', 'Content-Transfer-Encoding: 7bit', '', '', '---', 'Reply to this email directly or view it on GitHub:', '', 'Mime-Version: 1.0', 'Content-Type: text/html;', ' charset=UTF-8', 'Content-Transfer-Encoding: 7bit', '', '', '']
    # You need to first create an account here
    emails = receive_emails(account, 0)
    for email in emails:
        print 'EMAIL:\n'
        print email        
    #print(find_headers(emails))
    matches = match_emails(emails, criteria)
    for match in matches:
        print match
        print '\n\n\n\n'
    #trash = [email for email in emails if email not in matches]
    contents = [(extract_subject(email), extract_body(email)) for email in matches]
    for email_content in contents:
        print 'sent'
        send_email(account, 'whonixtest@rambler.ru', 'yamct@rambler.ru', email_content[0], email_content[1], 0)
    
    
