from .utils import get_or_register_waifu, return_error, db, db_conn, take_letters, has_letters
from discord import Embed, Colour


async def claim_waifu(interaction, waifu):
    claimer = interaction.user.name
    to_be_claimed = waifu.name

    if claimer == to_be_claimed:
        await return_error(interaction, 'You cannot claim yourself')
        return
    to_be_claimed_info = get_or_register_waifu(to_be_claimed)
    if claimer == to_be_claimed_info.get('owner'):
        await return_error(interaction, 'You already own this waifu')
        return

    required_letters = to_be_claimed
    if to_be_claimed_info.get('owner') != 'Nobody':
        gifts = list(map(lambda result: result[0], db.execute('SELECT gift FROM gifts WHERE gifted = ?', [to_be_claimed]).fetchall()))
        for gift in gifts:
            required_letters += gift

    if has_letters(claimer, required_letters):
        db.execute('UPDATE waifus SET owner = ? WHERE userName = ?', [claimer, to_be_claimed])
        db_conn.commit()
        take_letters(claimer, required_letters)
        await interaction.response.send_message(embeds=[Embed(title='Waifu acquired',
                                                              description=f"<@{interaction.user.id}> claimed <@{waifu.id}> as their waifu!",
                                                              colour=Colour.gold())])
    else:
        await return_error(interaction, "You don't have enough letters!")
