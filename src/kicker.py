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


import re
import json
import colorama

from threading import Thread, Event

import db
import telegram


class Kicker(Thread):

    def __init__(self, token, db_path, group_id):
        super().__init__()
        self.stop_event = Event()
        self.__token = token
        self.__db_handler = db.db_handler(db_path)
        self.__group_id = group_id

    def __shutdown(self):
        # close database connection
        self.__db_handler.close_database()
        self.__db_handler = None
        return

    def run(self):
        while not self.stop_event.is_set():
            # get data from telegram
            data = telegram.fetch_data(self.__token)

            # data validation
            if data is False:
                self.stop_event.wait(5.0)
                break

            # parse results
            for msg in data['result']:
                if 'text' in msg['message']:
                    entry = msg['message']['text']

                    # check for correct message format 
                    if not re.match('^@([a-zA-Z0-9_]*)\s\-\s(.*)$', entry):
                        telegram.send_message(self.__token, self.__group_id, 'Fehler beim Verarbeiten der Nachrichten.')
                        break

                    # get entry attributes
                    username = re.sub('\s\-\s(.*)$', '', entry)
                    reason = re.sub('^@([a-zA-Z0-9_]*)\s\-\s', '', entry)
                    
                    # add entry, if user does not exist in database
                    if not db.check_username(username):
                        db.add_user(username, reason)

            # wait before next loop execution
            self.stop_event.wait(30.0)

        # shut down, when stop event is set
        self.__shutdown()
