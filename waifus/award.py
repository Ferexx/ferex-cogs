from .utils import strip_illegal_letters, add_letters
from discord import Embed, Colour


async def award_letters(ctx, receiver, letters):
    letters_to_award = strip_illegal_letters(letters)
    if len(letters_to_award) == 0:
        await ctx.reply('No valid letters provided')
        return

    add_letters(receiver.name, letters)

    await ctx.channel.send(embeds=[Embed(title='Award',
                                         description=f"<@{ctx.author.id}> awarded `{letters_to_award}` to <@{receiver.id}>",
                                         colour=Colour.green())])
