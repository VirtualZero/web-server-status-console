import requests
from time import sleep
from termcolor import colored
from terminaltables import AsciiTable
import datetime
import subprocess
from halo import Halo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from settings import (
    server_list,
    email_settings,
    scan_interval,
    email_interval
)


def check_email_interval():
    last_email_sent_path = os.path.dirname(
        os.path.realpath(__file__)
    )

    if not os.path.isfile(f'{last_email_sent_path}/.last_email_sent.txt'):
        open('.last_email_sent.txt', 'a').close()

        return True

    with open('.last_email_sent.txt', "r") as last_email_sent:
        last_email_sent_time = last_email_sent.read()

        if not last_email_sent_time:
            return True

        try:
            datetime_object = datetime.datetime.strptime(
                last_email_sent_time,
                '%Y-%m-%d %H:%M:%S.%f'
            )

            if datetime_object + datetime.timedelta(
                minutes=email_interval()
            ) > datetime.datetime.now():

                return False

        except ValueError:
            return True

        except:
            return True

        return True


def update_last_email_sent_time():
    last_email_sent_path = os.path.dirname(
        os.path.realpath(__file__)
    )

    if not os.path.isfile(f'{last_email_sent_path}/.last_email_sent.txt'):
        open('.last_email_sent.txt', 'a').close()

    with open('.last_email_sent.txt', "w") as last_email_sent:
        last_email_sent.write(str(datetime.datetime.now()))

    return True


def prepare_email_content():
    email_content = ''

    with open('.last_email_sent.txt', 'r') as last_email_sent:
        last_email_sent_time = last_email_sent.read()

    try:
        last_email_datetime_object = datetime.datetime.strptime(
            last_email_sent_time,
            '%Y-%m-%d %H:%M:%S.%f'
        )

        with open('errors.log', 'r') as errors_log:
            for line in errors_log:
                if '\t' in line:
                    log_datetime_string = line.split('\t')[0]
                    log_datetime_object = datetime.datetime.strptime(
                        log_datetime_string,
                        '%A, %m/%d/%y %I:%M %p'
                    )

                    if log_datetime_object > last_email_datetime_object:
                        if not email_content:
                            email_content = line

                        else:
                            email_content = f'{email_content}{line}'

    except ValueError:
        update_last_email_sent_time()
        with open('errors.log', 'r') as errors_log:
            for line in errors_log:
                pass
            
            email_content = line
            return email_content

    except:
        update_last_email_sent_time()
        with open('errors.log', 'r') as errors_log:
            for line in errors_log:
                pass

            email_content = line
            return email_content

    return email_content                    


@Halo(
    text='Sending Error Email...',
    spinner='dots',
    text_color='white',
    color='red'
)
def send_error_email(name, url, status_code):
    if check_email_interval():
        mail_settings = email_settings()

        if mail_settings['recipients']:
            for index, recipient in enumerate(mail_settings['recipients']):
                email_content = prepare_email_content()
                body = f'Some errors occurred while scanning web servers.\n'\
                    f'Here are the details:\n'\
                    f'{email_content}'

                message = MIMEMultipart()
                message['From'] = mail_settings['sender']
                message['To'] = mail_settings['recipients'][index]
                message['Subject'] = 'Error Scanning Web Server'

                message.attach(MIMEText(body, 'plain'))
                message_string = message.as_string()

                server = smtplib.SMTP(
                    mail_settings['smtp_server'],
                    mail_settings['port']
                )

                server.ehlo()
                server.starttls()
                server.ehlo()

                try:
                    server.login(
                        mail_settings['username'],
                        mail_settings['password']
                    )

                except:
                    error_status_message = colored(
                        "\u2718", "red"
                    ) + ' Error sending alert email: AUTHENTICATION ERROR'
                    print(error_status_message)
                    return False

                try:
                    server.sendmail(
                        mail_settings['sender'],
                        mail_settings['recipients'][index],
                        message_string
                    )

                    server.quit()

                    update_last_email_sent_time()

                except:
                    error_status_message = colored(
                        "\u2718", "red"
                    ) + ' Error sending alert email'
                    print(error_status_message)
                    return False

        else:
            error_status_message = colored(
                "\u2718", "red"
            ) + ' Error sending alert email: NO RECIPIENTS'
            print(error_status_message)

    return True


def write_to_error_log(name, url, status_code):
    check_for_error_log()

    with open('errors.log', 'a') as error_log:
        error_time = datetime.datetime.now().strftime(
            '%A, %D %I:%M %p'
        )

        error_log.write(
            f'\n{error_time}\t{name}\t{str(status_code)}\t{url}'
        )

    return True


def get_server_status():
    status_report = {}
    scan_counter = 1

    try:
        if server_list():         
            while True:
                exec_cmd = subprocess.Popen('clear')
                exec_cmd.wait()

                error_status_message = colored(
                    "\u2718", "red"
                ) + ' ERROR'

                print(f'Scanning ({scan_counter})...')

                scan_counter+=1

                for name, url in server_list().items():
                        
                    print(
                        f'\nSending request to \033[4m{name}\033[0m at {url}...'
                    )

                    try:
                        server_response = requests.get(url, timeout=3)
                        status_report[name] = {
                            'url': url,
                            'status_code': server_response.status_code
                        }

                        if server_response.ok:
                            status_message = colored("\u2714", "green") + ' OK'
                            print(
                                f'Status: {status_message}'
                                f'\nResponse Time: {server_response.elapsed}'
                            )

                        else:
                            print(
                                f'Status: {colored("Error", "red")}' \
                                f'\nResponse Time: {server_response.elapsed}'
                            )

                            write_to_error_log(
                                name,
                                url,
                                server_response.status_code
                            )

                            send_error_email(
                                name,
                                url,
                                server_response.status_code
                            )

                            
                    except requests.exceptions.ConnectionError:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'No Connection Made'
                        }

                        print(
                            f'Status: {error_status_message}'
                            f'\nCould not establish a connection.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Could not establish a connection.'
                        )

                        send_error_email(
                            name, 
                            url, 
                            'Could not establish a connection.'
                        )

                        
                    except requests.exceptions.InvalidURL:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'Invalid URL'
                        }

                        print(
                            f'Status: {error_status_message}'
                            f'\nInvalid URL.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Invalid URL.'
                        )

                        send_error_email(
                            name,
                            url,
                            'Invalid URL.'
                        )


                    except requests.exceptions.MissingSchema:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'Invalid URL'
                        }

                        print(
                            f'Status: {error_status_message}'
                            f'\nInvalid URL.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Invalid URL.'
                        )

                        send_error_email(
                            name,
                            url,
                            'Invalid URL.'
                        )


                    except requests.exceptions.ReadTimeout:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'Connection Timeout'
                        }


                        print(
                            f'Status: {error_status_message}'
                            f'\nConnection timed out after 3 seconds.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Connection timed out after 3 seconds.'
                        )

                        send_error_email(
                            name,
                            url,
                            'Connection timed out after 3 seconds.'
                        )


                    except requests.exceptions.Timeout:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'Connection Timeout'
                        }

                        print(
                            f'Status: {error_status_message}'
                            f'\nConnection timed out.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Connection timed out.'
                        )

                        send_error_email(
                            name,
                            url,
                            'Connection timed out.'
                        )


                    except:
                        status_report[name] = {
                            'url': url,
                            'status_code': 'Unknown Error'
                        }

                        print(
                            f'Status: {error_status_message}'
                            f'\nUnknown Error.'
                        )

                        write_to_error_log(
                            name,
                            url,
                            'Unknown Error.'
                        )


                table_data = [
                    [
                        colored('Name', 'white'),
                        colored('Status Code', 'white'),
                        colored('URL', 'white')
                    ]
                ]

                table = AsciiTable(table_data)

                for report in status_report.items():
                    table_data.append(
                        [
                            report[0],
                            report[1]['status_code'],
                            report[1]['url']
                        ]
                    )

                report_time = datetime.datetime.now().strftime(
                    '\nLast scan completed on %A, %D at %I:%M %p'
                )

                print(report_time)
                print(f'{table.table}\n')

                @Halo(
                    text='Waiting...', 
                    spinner='dots',
                    text_color='white',
                    color='white'
                )
                def wait():
                    sleep(scan_interval() * 60)

                wait()

        else:
            print('\nNo server list.\n')
            exit(0)

    except KeyboardInterrupt:
        print('\nGoodbye.')
        exit(0)


def check_for_error_log():
    error_log_path = os.path.dirname(
        os.path.realpath(__file__)
    )

    if not os.path.isfile(f'{error_log_path}/errors.log'):
        open('errors.log', 'a').close()


def main():    
    get_server_status()


if __name__ == '__main__':
    main()
