#!/usr/bin/python3
""" CheckMK local check for Mailstore """
import os
import configparser
import sys
import urllib.error
from datetime import datetime, timedelta
import requests
from mgmt import ServerClient as ms_api

# Config-File
CONFIG_FILE = 'mailstore.cfg'
# Version-Check-URL is static
URL = 'https://my.mailstore.com/Downloads/Server/'
conf = configparser.RawConfigParser()
# Defaults
conf.read_dict({'server': {'host': 'localhost',
                           'port': 8463,
                           'username': 'admin',
                           'password': 'admin',
                           'ignoressl': False},
                'checks': {'version': True,
                           'licenses': True,
                           'profiles': True}})

conf_file = os.path.join(os.path.dirname(sys.argv[0]), CONFIG_FILE)

if not os.path.isfile(conf_file):
    print("INFO: " + conf_file + " doesn't exist - using defaults")
    with open(conf_file, "w", encoding="utf-8") as configfile:
        conf.write(configfile)
else:
    try:
        conf.read(conf_file)
    except EnvironmentError:
        e = sys.exc_info()[1]
        sys.exit(1)

try:
    api = ms_api(username=conf['server']['username'],
             password=conf['server']['password'],
             host=conf['server']['host'],
             port=conf['server']['port'],
             ignoreInvalidSSLCerts=conf['server'].getboolean('ignoressl'))
except (urllib.error.URLError, ConnectionRefusedError) as e:
    print(f"Can't connect to Mailstore: {e}")
    sys.exit(1)


def check_version():
    '''
    Check if Mailstore-Update is available
    https://help.mailstore.com/en/server/Administration_API_-_Function_Reference#GetServerInfo
    '''
    req = requests.get(URL, allow_redirects=False).headers
    download_url = req['Location']
    filename = download_url.split('/')[-1]
    version = filename.lstrip('MailstoreServerSetup-').rstrip('.exe')
    serverinfo = api.GetServerInfo()['result']
    current = serverinfo['version']
    if current < version:
        print(f'1 "MS:VERSION" version={current} newer version available: {version}')
    else:
        print(f'0 "MS:VERSION" version={current} up to date')


def check_licenses():
    '''
    Check for License-Infos
    https://docs.checkmk.com/latest/en/localchecks.html#metrics
    https://help.mailstore.com/en/server/Administration_API_-_Function_Reference#GetLicenseInformation
    '''
    licenses = api.GetLicenseInformation()['result']
    users = licenses['namedUsers']
    maxusers = licenses['maxNamedUsers']
    if users >= maxusers:
        stat = 1
    else:
        stat = 0
    print(f'{stat} "MS:LICENSE" licensecount={users};{maxusers};;;{maxusers}')


def check_profiles():
    '''
    Check for Profiles
    https://help.mailstore.com/en/server/Administration_API_-_Function_Reference#GetProfiles
    '''
    status = ""
    profs = api.GetProfiles()
    for prof in profs['result']:
        res = worker_results(prof['id'])
        if res:
            status += res
    count = len(profs['result'])
    if not status:
        stat = 0
    else:
        if status.startswith('WARN'):
            stat = 1
        else:
            stat = 2
    text = f'{stat} "MS:PROFILES" profilecount={count} {status}'
    print(text)


def worker_results(profileid):
    '''
    Helper for Profile-Check
    Get Worker-Results from the last 24h and set CRIT
    if last profile-run wasn't successfull
    '''
    string = ''
    timezoneid = "W. Europe Standard Time"
    yest = datetime.now()-timedelta(days=1)
    fromincluding = yest.strftime("%Y-%m-%dT%H:%M:%S")
    toexcluding = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    worker = api.GetWorkerResults(
        fromincluding, toexcluding, timezoneid, profileid)
    if worker["statusCode"] == "succeeded":
        for res in reversed(worker["result"]):
            if res["result"] == "succeeded":
                string = ''
                break
            elif res["result"] == "completedWithWarnings":
                string = f'WARN: "{res["profileName"]}@{res["completeTime"]}" '
                break
            else:
                string = f'FAIL: "{res["profileName"]}@{res["completeTime"]}" '
    return string


# print("<<<mailstore>>>")
if conf['checks'].getboolean('version'):
    check_version()
if conf['checks'].getboolean('licenses'):
    check_licenses()
if conf['checks'].getboolean('profiles'):
    check_profiles()
