#!/bin/env python3
#
# Telegram Auto Kick
#
# © 2015 Daniel Jankowski

import subprocess
import os
import re
import json
import sqlite3
import db
from threading import Thread,Event

DATABASE = '/home/neo/Projekte/Python/telegram-autokick/banned_usernames.db'
GROUP_NAME = 'Linux_statt_Windows'

class kicker(Thread):

    def __init__(self):
        super().__init__()
        self.stop_event = Event()
        self.__db = db.db_handler(DATABASE)
        self.__db.create_table()
        self.__db.close_database()

    def add_username(self, username):
        self.__db.add_user(username)

    def remove_shit(self, data):
        data = re.sub('\r', '', data)
        data = re.sub('\x1b\[K', '', data)
        data = re.sub('>\s*', '', data)
        data = re.sub('All done\. Exit\n', '', data)
        data = re.sub('halt\n*', '', data)
        data = re.sub('\n*$', '', data)
        return json.loads(data)

    def run(self):
        while not self.stop_event.is_set():
            # get data from telegram-cli
            cmd = ['telegram-cli','-b','-W','-D','--json','-e chat_info ' + GROUP_NAME]
            s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            data = s.communicate()[0].decode('utf-8')
            data = self.remove_shit(data)
       
            # processing data
            members = data['members']
                        
            self.__db = db.db_handler(DATABASE)
            banned_users = self.__db.get_banned_usernames()
            self.__db.close_database()
            
            banned_usernames = []
            banned_ids = []
            for user in banned_users:
                banned_usernames.append(user[0])
                banned_ids.append(user[1])

            for member in members:
                if 'username' in member:
                    if member['username'] in banned_usernames:
                        if member['id'] not in banned_ids:
                            self.__db = db.db_handler(DATABASE)
                            self.__db.add_user_id(member['id'], member['username'])
                            self.__db.close_database()
                if member['id'] in banned_ids:
                    cmd = ['telegram-cli','-b','-W','-D','--json','-e chat_del_user ' + GROUP_NAME + ' ' + member['print_name']]
                    s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    data = s.communicate()[0].decode('utf-8')
                    data = self.remove_shit(data)

            self.stop_event.wait(1.0)

    def stop(self):
        self.stop_event.set()


def main():
    print('Telegram Auto Kick')
    
    bot = kicker()
    bot.start()

    inp = ''
    while inp != "exit":
        inp = input()
    bot.stop()
    bot.join()
    return


if __name__ == '__main__':
    main()
