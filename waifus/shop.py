import re
from .utils import strip_illegal_letters, return_error, has_letters, add_letters, take_letters
from discord import Embed, Colour


async def letters_shop(interaction, buying, selling):
    buying_letters = strip_illegal_letters(buying)
    selling_letters = strip_illegal_letters(selling)

    if len(selling_letters) / len(buying_letters) != 5:
        await return_error(interaction, 'The ratio is 5 letters to one number/symbol')
        return
    if re.search(r"[a-z]", buying_letters):
        await return_error(interaction, 'You cannot buy letters!')
        return
    if re.search(r"[0-9\._]", selling_letters):
        await return_error(interaction, 'You cannot sell numbers/symbols!')
        return
    if not has_letters(interaction.user.name, selling_letters):
        await return_error(interaction, "You don't have those letters!")
        return

    add_letters(interaction.user.name, buying_letters)
    take_letters(interaction.user.name, selling_letters)

    await interaction.response.send_message(embeds=[Embed(title='Shop',
                                                          description=f"<@{interaction.user.id}> exchanged `{selling}` for `{buying}`",
                                                          colour=Colour.green())])
