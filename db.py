#!/bin/env python3
#
# Telegram Auto Kick
#
# © 2015 Daniel Jankowski

import sqlite3

DATABASE = '/home/neo/Projekte/Python/telegram-autokick/banned_usernames.db'

class db_handler(object):

    def __init__(self, database):
        super().__init__()
        self.__database = database
        try:
            self.__con = sqlite3.connect(database)
            self.__cur = self.__con.cursor()
        except Exception as e:
            print(e)
            print('Error connecting to the database')

    def close_database(self):
        self.__con.commit()
        self.__con.close()

    def create_table(self):
        self.__cur.execute('CREATE TABLE IF NOT EXISTS banned_user(username TEXT, id INT)')

    def add_user(self, username):
        self.__cur.execute('INSERT INTO banned_user VALUES(\'' + username + '\', 0)')

    def add_user_id(self, user_id, username):
        self.__cur.execute('UPDATE banned_user SET id=' + str(user_id) + ' WHERE username=\'' + username + '\'')

    def del_user(self, username):
        self.__cur.execute('DELETE FROM banned_user WHERE username LIKE \'' + username + '\'')
        self.__cur.execute('DELETE FROM banned_user WHERE id LIKE \'' + username + '\'')

    def get_banned_usernames(self):
        self.__cur.execute('SELECT * FROM banned_user')
        data = self.__cur.fetchall()
        return data


def main():
    print('Edit the database')
    
    inp = ''
    while inp != "exit":
        inp = input('> ')
        if inp.startswith('add'):
            username = inp.lstrip('add ')
            db = db_handler(DATABASE)
            db.add_user(username)
            db.close_database()
            print('Added username')
        elif inp.startswith('del'):
            username = inp.lstrip('del ')
            db = db_handler(DATABASE)
            db.del_user(username)
            db.close_database()
            print('Deleted User')
        elif inp.startswith('show'):
            db = db_handler(DATABASE)
            liste = db.get_banned_usernames()
            print(liste)
            db.close_database()
    return

if __name__ == '__main__':
    main()
