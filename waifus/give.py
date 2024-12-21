from .utils import return_error, has_letters, add_letters, take_letters, strip_illegal_letters
from discord import Embed, Colour


async def give_letters(interaction, receiver, letters):
    letters_to_give = strip_illegal_letters(letters)
    if len(letters_to_give) == 0:
        return_error(interaction, 'No valid letters provided')
        return

    if not has_letters(interaction.user.name, letters_to_give):
        return_error(interaction, "You don't have all of those letters!")
        return

    add_letters(receiver.name, letters_to_give)
    take_letters(interaction.user.name, letters_to_give)

    await interaction.response.send_message(embeds=[Embed(title='Letters given',
                                                          description=f"<@{interaction.user.id}> has given `{letters_to_give}` to <@{receiver.id}>",
                                                          colour=Colour.blue())])
