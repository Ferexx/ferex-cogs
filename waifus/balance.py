import re
from .utils import get_user_letters
from discord import Embed


def build_field(letters, title, regex):
    built_string = ""
    for letter, value in letters.items():
        if re.search(regex, letter):
            built_string += f"`{letter.upper()}`: {value}\n"
    return {'name': title, 'value': built_string, 'inline': True}


async def check_balance(interaction):
    user_letters = get_user_letters(interaction.user.name)
    all_letters = '0123456789abcdefghijklmnopqrstuvwxyz._'

    for letter in all_letters:
        if user_letters.get(letter) is None:
            user_letters[letter] = '-'

    user_letters = dict(sorted(user_letters.items()))
    numbers_field = build_field(user_letters, 'Num/Symbols', r"[0-9\._]")
    letters_field = build_field(user_letters, 'Letters (A-M)', r"[a-m]")
    letters_cont_field = build_field(user_letters, 'Letters (N-Z)', r"[n-z]")

    await interaction.response.send_message(embeds=[Embed(title='Letter Balance',
                                                          description='------------------------------------------------')
                                                    .add_field(**numbers_field)
                                                    .add_field(**letters_field)
                                                    .add_field(**letters_cont_field)])
