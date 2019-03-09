# Web Server Status Console
Powered by [Virtualzero](https://virtualzero.net)

Web Server Status Console is a Python script used to alert an administrator if a web server is misbehaving. The script makes requests to a dictionary of URLs on custom-defined intervals and sends an alert email to the administrator if the response status code is 400+ or if another issue is encountered.

#### Installation
Clone the repository:
```bash
git clone https://github.com/VirtualZero/web-server-status-console.git
```

#### Environment

Install Miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```

```bash
./Miniconda3-latest-Linux-x86_64.sh
```

Create Environment
```bash
conda create --name 'web-server-status-console' python=3.7
```

Activate Environment
```bash
source activate web-server-status-console
```

Install Dependencies
```bash
cd web-server-status-console && pip install -r requirements.txt
```

#### Getting Started
Add the URLs to monitor to the server_list dictionary in settings.py. The dictionary keys should be an identifying name while the values must be URLs.
```python
def server_list():
    return {
        'WebSiteName1': 'http://your-domain.com', 
        'WebSiteName2': 'http://your-domain.com',
        'WebSiteName3': 'http://your-domain.com',
    }
```

The script uses SMTP to send alert emails in the event of an undesired status code or other error. Any SMTP service can be used with the script. Update the email_settings dictionary in settings.py with your SMTP service credentials. Email recipients are also configured in the email_settings dictionary by updating the recipients list. An example using AWS SES is shown below. 
```python
def email_settings():
    return {
        'smtp_server': 'email-smtp.us-east-1.amazonaws.com',
        'port': 587,
        'username': 'LVYITZXYIQPJUVDU',
        'password': '6kFDuDcUUESOyargOS9AMx2ZZrnu98sE',
        'sender': 'alerts@your-domain.com',
        'recipients': [
            'example1@your-domain.com',
            'example2@your-domain.com',
            'example3@your-domain.com'
        ]
    }
```

The scan interval is configurable within settings.py. The scan interval must be an integer indicating the number of minutes between scans.
```python
def scan_interval():
    return 15
```

The email interval is configurable within settings.py. The email interval controls how often alert emails are sent. After the defined amount of time has past, the script will send an alert email containing all errors that occured within the defined amount of time. The email interval must be an integer indicating the number of minutes between alert emails.
```python
def email_interval():
    return 60
```

#### Error Logging
The script will record any errors encountered during exucution in errors.log. The error log will be created in the script's directory upon initial execution.

#### Example Usage
```bash
python3 run.py
```