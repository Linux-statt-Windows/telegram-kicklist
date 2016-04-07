#!/bin/env python3
#
# Telegram Auto Kicklist
#
# A small tool, that generates a list with kicked/banned users, their id
# and reason from a telegram group for exactly that purpose.
#
# Messages must look like:
#
#    "@username - reason"
#
# This tool automatically grabs the user id behind the username, so username-
# changes will be detected.
#
# © 2016 Daniel Jankowski


import json
import urllib.parse
import urllib.request

import utils


# send message
def send_message(token, group_id, msg):
    # check, if message is sent
    try:
        text = 'chat=' + str(group_id) + '&text=' + urllib.parse.urlencode(msg)
        rqst = urllib.request.urlopen('https://api.telegram.org/bot' + token + '/sendMessage', text.encode('utf-8'))
    except Exception as e:
        log_warn('Unable to send message')
        print(str(e))
    return


# fetch json object from api
def fetch__data(token):
    # fetch data
    try:
        data = urllib.request.urlopen('https://api.telegram.org/bot' + token + '/getUpdates').read()
    except Exception as e:
        log_err('Failed to fetch data')
        print(str(e))
        return False

    # check for encoding errors
    try:
        data = json.loads(data.decode('utf-8'))
    except Exception as e:
        log_err('Failed to convert data into json object')
        print(str(e))
        return False

    # return data, if valid
    return data
