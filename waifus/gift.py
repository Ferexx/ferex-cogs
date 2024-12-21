from .utils import strip_illegal_letters, take_letters, gift_letters, return_error, has_letters
from discord import Embed, Colour


async def gift_letters_command(interaction, waifu, letters):
    gifter = interaction.user.name
    gifted = waifu.name
    letters_to_gift = strip_illegal_letters(letters)

    if not letters_to_gift:
        await return_error(interaction, 'No valid letters provided')
        return
    if not has_letters(gifter, letters_to_gift):
        await return_error(interaction, "You don't have all of those letters!")
        return
    for letter in letters_to_gift:
        if letter not in gifted:
            await return_error(interaction, f'Waifu does not have the letter {letter} in their name')
            return

    take_letters(gifter, letters_to_gift)
    gift_letters(gifted, gifter, letters_to_gift)

    await interaction.response.send_message(embeds=[Embed(title='A gift!',
                                                          description=f"<@{interaction.user.id}> has gifted the letters `{letters_to_gift}` to <@{waifu.id}>",
                                                          color=Colour.gold())])
