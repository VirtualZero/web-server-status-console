from server_list import server_list
import requests
from time import sleep
from termcolor import colored
from terminaltables import AsciiTable
import datetime
import subprocess
from halo import Halo


def get_server_status():
    status_report = {}
    scan_counter = 1

    try:
        if server_list():
            while True:
                exec_cmd = subprocess.Popen('clear')
                exec_cmd.wait()
                print(f'Scanning ({scan_counter})...')
                scan_counter+=1

                for name, url in server_list().items():
                    if name != 'Name':
                        
                        
                        print(f'\nSending request to {name} at {url}...')

                        try:
                            server_response = requests.get(url, timeout=3)
                            status_report[name] = {
                                'url': url,
                                'status_code': server_response.status_code
                            }

                            if server_response.ok:
                                print(
                                    f'Status: \u2713 {colored("OK", "green")}'
                                    f'\nResponse Time: {server_response.elapsed}'
                                )

                            else:
                                print(
                                    f'Status: {colored("Error", "red")}' \
                                    f'\nResponse Time: {server_response.elapsed}'
                                )

                        except requests.exceptions.ConnectionError:
                            status_report[name] = {
                                'url': url,
                                'status_code': 'No Connection Made'
                            }

                            print(
                                f'Status: {colored("Error", "red")}'
                                f'\nCould not establish a connection.'
                            )
                        
                        except requests.exceptions.InvalidURL:
                            status_report[name] = {
                                'url': url,
                                'status_code': 'Invalid URL'
                            }

                            print(
                                f'Status: {colored("Error", "red")}'
                                f'\nInvalid URL.'
                            )

                        except requests.exceptions.MissingSchema:
                            status_report[name] = {
                                'url': url,
                                'status_code': 'Invalid URL'
                            }

                            print(
                                f'Status: {colored("Error", "red")}'
                                f'\nInvalid URL.'
                            )

                        except requests.exceptions.ReadTimeout:
                            status_report[name] = {
                                'url': url,
                                'status_code': 'Connection Timeout'
                            }

                            print(
                                f'Status: {colored("Error", "red")}'
                                f'\nConnection timed out.'
                            )

                        except requests.exceptions.Timeout:
                            status_report[name] = {
                                'url': url,
                                'status_code': 'Connection Timeout'
                            }

                            print(
                                f'Status: {colored("Error", "red")}'
                                f'\nConnection timed out after 3 seconds.'
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
                    color='cyan'
                )
                def wait():
                    sleep(10)

                wait()

        else:
            print('No server list.')

    except KeyboardInterrupt:
        print('\nGoodbye.')
        exit(0)


def main():
    get_server_status()


if __name__ == '__main__':
    main()
