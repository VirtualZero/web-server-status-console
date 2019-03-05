def server_list():
    return {
        'WebSite1': 'http://your-domain.com',   # 'App Name': 'URL'
        'WebSite2': 'http://your-domain.com',   # 'App Name': 'URL'
        'WebSite3': 'http://your-domain.com',   # 'App Name': 'URL'
    }


def email_settings():
    return {
        # Your SMTP server's name
        'smtp_server': 'email-smtp.us-east-1.amazonaws.com',
        # SMTP TLS port number
        'port': 587,
        # Your email login username or email
        'username': 'LVYITZXYIQPJUVDU',
        # Your email login password
        'password': '6kFDuDcUUESOyargOS9AMx2ZZrnu98sE',
        # Your email sender address
        'sender': 'alerts@your-domain.com',
        # Your email recipients, multiple recipients supported
        'recipients': [
            'example1@your-domain.com',
            'example2@your-domain.com',
            'example3@your-domain.com'
        ]
    }


def ec2_access_keys():
    return {
        'access_key': 'ACCESS_KEY',
        'secret_access_key': 'YOUR_SECRET_ACCESS_KEY'
    }


def ec2_reboot_status():
    return 1


def ec2_instance_id():
    return 'i-12345678987654'


def scan_interval():
    #Scan web servers every N minutes, must be Integer
    return 1


def email_interval():
    # Send error emails every N minutes, must be Integer
    return 1
