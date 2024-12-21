import os
import sqlite3
import re
from discord import Embed, Colour

db_conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/data.sqlite')
db = db_conn.cursor()


def get_or_register_waifu(user_name):
    waifu = db.execute("SELECT * FROM waifus WHERE userName = ?", [user_name]).fetchone()
    if waifu is not None:
        return {'user_name': waifu[0], 'owner': waifu[1], 'gift_count': waifu[2]}

    db.execute("INSERT INTO waifus (userName, owner) VALUES (?, ?)", [user_name, 'Nobody'])
    db.execute("INSERT INTO letters (userName, letters) VALUES (?, ?)", [user_name, ''])
    db.execute("INSERT INTO timely (userName, lastTimely) VALUES (?, ?)", [user_name, 0])
    db_conn.commit()

    return {'user_name': user_name, 'owner': 'Nobody', 'gift_count': 0}


def count_letters(letters_string):
    freq = {}
    if letters_string is None:
        return freq
    for letter in letters_string:
        if freq.get(letter) is not None:
            freq[letter] = freq.get(letter) + 1
        else:
            freq[letter] = 1
    return freq


def letters_map_to_string(letters_map):
    if not letters_map:
        return 'None'
    sorted_map = dict(sorted(letters_map.items()))
    return_string = ''
    for key, value in sorted_map.items():
        return_string += f"`{key.upper()}`: {value}\n"
    return return_string


def strip_illegal_letters(letters):
    letters = letters.lower()
    matching_chars = re.findall(r'[a-z0-9\._]', letters)
    return ''.join(matching_chars)


def take_letters(user_name, letters_to_take):
    current_letters = db.execute("SELECT letters FROM letters WHERE userName = ?", [user_name]).fetchone()[0]
    for letter in letters_to_take:
        current_letters = current_letters.replace(letter, '', 1)
    db.execute("UPDATE letters SET letters = ? WHERE userName = ?", [current_letters, user_name])
    db_conn.commit()


def add_letters(user_name, letters_to_add):
    current_letters = db.execute("SELECT letters FROM letters WHERE userName = ?", [user_name]).fetchone()[0]
    current_letters += letters_to_add
    db.execute("UPDATE letters SET letters = ? WHERE userName = ?", [current_letters, user_name])
    db_conn.commit()


def gift_letters(gifted, gifter, letters_to_gift):
    for letter in letters_to_gift:
        db.execute("INSERT INTO gifts (gifted, gifter, gift) VALUES (?, ?, ?)", [gifted, gifter, letter])
        current_gift_count = db.execute("SELECT giftCount FROM waifus WHERE userName = ?", [gifted]).fetchone()[0]
        db.execute("UPDATE waifus SET giftCount = ? WHERE userName = ?", [++current_gift_count, gifted])
        db_conn.commit()


def has_letters(user_name, letters):
    required_letters_count = count_letters(letters)
    user_letters = db.execute("SELECT letters FROM letters WHERE userName = ?", [user_name]).fetchone()[0]
    user_letters_count = count_letters(user_letters)
    has_letters = True
    for letter, count in required_letters_count.items():
        if user_letters_count.get(letter) is None:
            has_letters = False
            break
        if user_letters_count.get(letter) < count:
            has_letters = False
            break
    return has_letters


def get_user_letters(user_name):
    db_result = db.execute("SELECT letters FROM letters WHERE userName = ?", [user_name]).fetchone()[0]
    return count_letters(db_result)


async def return_error(interaction, message):
    await interaction.response.send_message(embeds=[Embed(title='Error',
                                                    description=message,
                                                    colour=Colour.red())],
                                            ephemeral=True)
