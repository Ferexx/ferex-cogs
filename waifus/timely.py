from math import floor
from random import randint
from discord import Embed
from time import time
from .utils import db, db_conn, add_letters, return_error


def is_too_recent(lastTime):
    return lastTime + (60 * 60) > time()


def get_time_remaining(lastTime):
    current_time_plus_one_hour = time() + (60 * 60)
    time_since_last_timely = time() - lastTime
    return str(floor(current_time_plus_one_hour - time_since_last_timely))


async def get_timely(interaction):
    user_name = interaction.user.name
    db_result = db.execute("SELECT lastTimely FROM timely WHERE userName = ?", [user_name])
    lastTime = floor(db_result.fetchone()[0])

    if is_too_recent(lastTime):
        await return_error(interaction, "You've already claimed your timely letter, you can get it again <t:" + get_time_remaining(lastTime) + ":R>")
        return

    new_letter_unicode = randint(65, 90)
    new_letter = chr(new_letter_unicode)
    add_letters(user_name, new_letter)

    db.execute("UPDATE timely SET lastTimely = ? WHERE userName = ?", [time(), user_name])
    db_conn.commit()

    await interaction.response.send_message(embeds=[Embed(title='You got a new letter!',
                                                          description=new_letter)])
