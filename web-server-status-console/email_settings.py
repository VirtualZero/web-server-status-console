def email_settings():
    return {
        'smtp_server': 'email-smtp.us-east-1.amazonaws.com',            # Your SMTP server's name
        'port': 587,                                                    # SMTP TLS port number
        'username': 'LVYITZXYIQPJUVDU',                                 # Your email login username or email
        'password': '6kFDuDcUUESOyargOS9AMx2ZZrnu98sE',                 # Your email login password
        'sender': 'alerts@your-domain.com',                             # Your email sender address
        'recipients': [                                                 # Your email recipients, multiple recipients supported
            'example1@your-domain.com',
            'example2@your-domain.com',
            'example3@your-domain.com'
        ]
    }
