from .utils import take_letters, strip_illegal_letters
from discord import Embed, Colour


async def take_letters_command(ctx, waifu, letters):
    letters_to_take = strip_illegal_letters(letters)
    if len(letters_to_take) == 0:
        await ctx.reply('No valid letters provided')
        return
    take_letters(waifu.name, letters_to_take)

    await ctx.channel.send(embeds=[Embed(title='Letters taken',
                                   description=f"<@{ctx.author.id}> took `{letters}` from <@{waifu.id}>",
                                   colour=Colour.red())])
