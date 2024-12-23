from random import random, randint
from .utils import add_letters
from discord import Embed
import asyncio

pick_words = ['pick', 'pluck', 'yoink', 'snag', 'gobble', 'scoop']


async def clear_pick(message, activePick):
    await asyncio.sleep(5)
    await message.delete()
    activePick = {}


async def award_pick_if_correct_word(message, activePick):
    if message.content == activePick.get('word'):
        await message.delete()
        if not activePick.get('claimed'):
            activePick['claimed'] = True
            await activePick.get('message').delete()

            add_letters(message.author.name, activePick.get('letter').lower())

            sent_message = await message.channel.send(embeds=[Embed(description=f"<@{message.author.id}> picked `{activePick.get('letter')}`")])

            asyncio.create_task(clear_pick(sent_message, activePick))


async def generate_pick_if_lucky(message):
    if (random() < 0.2):
        new_letter_unicode = randint(65, 90)
        new_letter = chr(new_letter_unicode)
        random_word = ',' + pick_words[randint(0, len(pick_words) - 1)]

        sent_message = await message.channel.send(content=f"A random {new_letter} appeared! Pick it by typing `{random_word}`")
        return {
                'letter': new_letter,
                'word': random_word,
                'message': sent_message,
                'claimed': False
                }
