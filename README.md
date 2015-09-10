### Telegram Autokick

Kicks banned users automatically out of groups.

Features
--------

- SQLite3-database
- automatically stores the user-id, so name changes will not prevent the ban


Install
-------

- **Requierments:**
  - telegram-cli
  - python3
- establish telegram-cli to work *Hint: You need to be the administrator of the group in order to remove any user!*
- `git clone git@github.com:dj95/telegram-autokick.git`
- `cd telegram-autokick`
- `chmod +x *.py`


Usage
-----

- Start with `./autokick.py` in cloned directory
- Use the db.py to edit your database
  - `add <username/print_name>` adds an username OR print_name to the database
  - `del <username/print_name>` deletes an entry to the given username OR print_name(please look, which of them you've added to the database earlier!)
  - `show` prints out all banned usernames or print_names and ids
  - `exit` exit the database-tool


Todo
----

- Stability-improvements(some kind of unicode problems seem to be there)
- Get rid of too much regex in the remove_shit() function to remove strange characters from the telegram-cli output


License
-------

© 2015 Daniel Jankowski

Licensed under the GNU Lesser General Public License Version 3. See [LICENSE](./LICENSE) for more details.
