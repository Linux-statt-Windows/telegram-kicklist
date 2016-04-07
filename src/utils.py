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


import colorama

from colorama import Fore, Back


# check if all keys exist in dictionary
def has_keys(dic, keys):
    for key in keys:
        if key not in dic.keys(): return False
    return True


#####################
#   LOG-FUNCTIONS   #
#####################

def log(text):
    print(Fore.GREEN + '==> ' + Fore.WHITE + text)

def log_warn(text):
    print(Fore.YELLOW + '==> Warning:' + Fore.WHITE + text)

def log_err(text):
    print(Fore.RED + '==> Error: ' + Fore.WHITE + text)

