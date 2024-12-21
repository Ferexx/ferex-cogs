from .utils import db, return_error
from discord import Embed


async def waifu_leaderboard(interaction, page):
    if page is None:
        page = 0

    ordered_waifus = db.execute("SELECT * FROM waifus ORDER BY giftCount DESC").fetchall()
    if page < 0 or page >= len(ordered_waifus) / 10:
        await return_error(interaction, 'Invalid page number')
        return

    if len(ordered_waifus) <= 10 or page == 0:
        min = 0
        max = 9
    else:
        max = page * 10
        min = max - 11

    embed = Embed(title='Waifu leaderboard')
    for i in range(min, max + 1):
        embed.add_field(name=f"**#{i + 1}: {ordered_waifus[i][0]}**", value=f"Claimed by: {ordered_waifus[i][1]}\nGifts: `{ordered_waifus[i][2]}`")

    await interaction.response.send_message(embeds=[embed])
