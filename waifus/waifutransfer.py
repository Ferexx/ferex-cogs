from .utils import get_or_register_waifu, db, db_conn, return_error
from discord import Embed, Colour


async def waifu_transfer(interaction, waifu, new_owner):
    waifu_from_db = get_or_register_waifu(waifu.name)
    if waifu_from_db.get('owner') != interaction.user.name:
        await return_error(interaction, "You don't own this waifu!")
        return

    db.execute('UPDATE waifus SET owner = ? WHERE userName = ?', [new_owner.name, waifu.name])
    db_conn.commit()

    await interaction.response.send_message(embeds=[Embed(title='Waifu transferred',
                                                          description=f"<@{interaction.user.id}> transferred <@{waifu.id}> to <@{new_owner.id}>",
                                                          colour=Colour.green())])
