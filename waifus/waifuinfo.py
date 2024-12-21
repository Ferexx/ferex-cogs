from .utils import letters_map_to_string, count_letters, get_or_register_waifu, db
from discord import Embed


async def get_waifu_info(interaction, user):
    if user is None:
        user = interaction.user
    user_as_waifu = get_or_register_waifu(user.name)

    owned_waifus = list(map(lambda db_result: db_result[0], db.execute("SELECT userName FROM waifus WHERE owner = ?", [user_as_waifu['user_name']]).fetchall()))
    gifts = count_letters(list(map(lambda result: result[0], db.execute("SELECT gift FROM gifts WHERE gifted = ?", [user_as_waifu['user_name']]).fetchall())))

    await interaction.response.send_message(embeds=[Embed(title=f"Waifu \"{user_as_waifu['user_name']}\"")
                                                    .add_field(name='Claimed by', value=user_as_waifu['owner'])
                                                    .add_field(name=f"Waifus({len(owned_waifus)})", value='\n'.join(owned_waifus) if len(owned_waifus) > 0 else 'Nobody')
                                                    .add_field(name='Gifts', value=letters_map_to_string(gifts), inline=False)])
