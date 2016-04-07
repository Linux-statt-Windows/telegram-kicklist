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


import os
import re
import argparse

from utils import *
from kicker import * 


CONFIG_PATH = './kicklist.conf'


def parse_config(path):
    attrs = {}

    # check, if path exists
    if not os.path.exists(path):
        return False
    
    with open(path, 'r') as fp:
        # get config keys
        for line in fp.readlines():
            if line.startswith('token'):
                attrs['token'] = re.sub(r'^(.*)\s?=\s?(.*)$', r'\2', line)
            if line.startswith('db'):
                attrs['db'] = re.sub(r'^(.*)\s?=\s?(.*)$', r'\2', line)
            if line.startswith('group_id'):
                attrs['group_id'] = re.sub(r'^(.*)\s?=\s?(.*)$', r'\2', line)

    # check completion of config keys
    if has_keys(attrs, ['token', 'db', 'group_id']):
        return attrs

    # print error, when keys are not complete
    log_err('Your config is not complete or correct. Please check it.')
    return False 


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', type=str, help='Telegram Bot token.')
    parser.add_argument('-c', '--config', type=str, help='Path to your config file.')
    args = parser.parse_args()

    attrs = {}
    # check for config path and read config
    if args.config:
        attrs = parse_config(args.config)
    else:
        attrs = parse_config(CONFIG_PATH)

    # check if config is parsed correctly
    if attrs is False:
        return False
    
    # check for new access token
    if args.token:
        attrs['token'] = args.token

    # start kicklist thread to collect your data
    kicker = Kicker(attrs['token'], attrs['db'], attrs['group_id'])
    kicker.start()

    # TODO: generate static list from database
    generator = Generator()
    generator.start()

    # TODO: upload list to nodebb or something else
    uploader = Uploader()
    uploader.start()
    return


if __name__ == '__main__':
    main()
