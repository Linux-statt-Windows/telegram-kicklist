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


from threading import Thread, Event

import db


class Generator(Thread):

    def __init__(self):
        super().__init__()
        self.stop_event = Event()

    def __shutdown(self):
        return

    def run(self):
        while not self.stop_event.is_set():
            self.stop_event.wait(1.0)

        # shut down, when stop event is set
        self.__shutdown()
