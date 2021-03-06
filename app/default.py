import os
import json
import socket
import shutil
from .app import *


def convert_hostnames(file_path):
    with open(file_path, 'r+') as json_file:
        data = json.loads(json_file.read())
        data_accounts = data['accounts']
        length, loop, timeout = 0, 0, 0

        for name, value in data_accounts.items():
            length += len(value)

        for name, value in data_accounts.items():
            for i in range(len(value)):
                account = data_accounts[name][i]
                try:
                    if timeout == 3: break
                    log_replace('[Y1][{}/{}] Converting hostnames'.format(app_format(loop+1, align='>', width=len(str(length)), chars='0'), length), log_datetime=True, status='[Y1]INFO')
                    host = ''
                    host = socket.gethostbyname(account['hostname'])
                    if not host:
                        raise socket.gaierror
                    elif host != account['host']:
                        log('[G1]{:.<19} [Y1]{:.<20}{:.>36}'.format((account['host'] if account['host'] else '(empty)')+' ', host+' [G1]', ' '+account['hostname']), status='[G1]INFO')
                        data_accounts[name][i]['host'] = host
                        timeout = 0
                except socket.gaierror:
                    log('[R1][{}/{}] Converting hostnames timeout'.format(app_format(timeout+1, align='>', width=len(str(length)), chars='0'), app_format('3', align='>', width=len(str(length)), chars='0')), status='[R1]INFO')
                    timeout = timeout + 1
                finally:
                    loop = loop + 1

        json_file.seek(0)
        json.dump(data, json_file, indent=2)
        json_file.truncate()

    return data_accounts

def generate_accounts(data_accounts):
    data_authentications = json.loads(open(real_path('/../database/authentications.json')).read())['authentications']

    accounts = []

    for i in range(len(data_authentications)):
        for name in data_accounts:
            for x in range(len(data_accounts[name])):
                account = data_accounts[name][x]
                accounts.append({
                    'name': name,
                    'host': account['host'],
                    'hostname': account['hostname'],
                    'username': account['username'].replace('{username}', data_authentications[i]['username']),
                    'password': account['password'].replace('{password}', data_authentications[i]['password'])
                })

    accounts = [dict(tuples) for tuples in {tuple(dictionaries.items()) for dictionaries in accounts}]

    return accounts

def main():
    file_names = [
        'config/config.json',
        'config/payload.txt',
        'config/server-name-indication.txt',
        'database/accounts.json',
        'database/authentications.json',
        'database/servers.json'
    ]

    for file_name in file_names:
        try:
            open(real_path('/../' + file_name))
        except FileNotFoundError:
            shutil.copyfile(real_path('/default/' + file_name), real_path('/../' + file_name))
        finally: pass

main()
