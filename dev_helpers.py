def find_headers(emails):
    common_headers = emails[0]
    for email in emails:
        for header in common_headers:
            if header not in email: common_headers.remove(header)
    return common_headers
