from .utils import get_or_register_waifu, return_error, db, db_conn
from discord import Embed


async def divorce_waifu(interaction, waifu):
    divorcer = interaction.user.name
    to_be_divorced = waifu.name

    divorcee_as_waifu = get_or_register_waifu(to_be_divorced)
    if divorcee_as_waifu.get('owner') != divorcer:
        await return_error(interaction, "You don't own that waifu!")
        return

    db.execute("UPDATE waifus SET owner = ? WHERE userName = ?", ['Nobody', to_be_divorced])
    db_conn.commit()

    await interaction.response.send_message(embeds=[Embed(title='Divorce!',
                                                          description=f"<@{interaction.user.id}> has divorced <@{waifu.id}>... All good things must come to an end")])
