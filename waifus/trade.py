from .utils import strip_illegal_letters, return_error, has_letters, take_letters, add_letters
import discord
from discord import Embed, Colour, Interaction, ButtonStyle
from discord.ui import View, Button


async def trade_letters(interaction, user, offer_letters, wanted_letters):
    outgoing_letters = strip_illegal_letters(offer_letters)
    incoming_letters = strip_illegal_letters(wanted_letters)

    if not has_letters(interaction.user.name, outgoing_letters):
        await return_error(interaction, "You don't have all of those letters")
        return
    if not has_letters(user.name, incoming_letters):
        await return_error(interaction, "That user doesn't have all of those letters")
        return

    await interaction.response.send_message(content=f"<@{user.id}>",
                                            embeds=[Embed(title='A trade is offered!',
                                                          description=f"<@{user.id}>, <@{interaction.user.id}> is offering their `{outgoing_letters}` for your `{incoming_letters}`. Do you accept?"
                                                          )],
                                            view=ButtonView())


class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Accept', style=ButtonStyle.success)
    async def confirm(self,
                      interaction: Interaction,
                      button: Button):
        if interaction.message.mentions[0].id != interaction.user.id:
            await return_error(interaction, 'This trade is not intended for you!')
            return
        split_desc = interaction.message.embeds[0].description.split(' ')
        outgoing_letters = strip_illegal_letters(split_desc[5])
        incoming_letters = strip_illegal_letters(split_desc[8])

        take_letters(interaction.user.name, incoming_letters)
        add_letters(interaction.user.name, outgoing_letters)

        take_letters(interaction.message.interaction_metadata.user.name, outgoing_letters)
        add_letters(interaction.message.interaction_metadata.user.name, incoming_letters)

        await interaction.message.edit(embeds=[Embed(title='A trade is offered!',
                                                     description=f"<@{interaction.user.id}> accepted the trade!",
                                                     colour=Colour.green())],
                                       view=None)

    @discord.ui.button(label='Decline', style=ButtonStyle.danger)
    async def deny(self,
                   interaction: Interaction,
                   button: Button):
        await interaction.message.edit(embeds=[Embed(title='A trade is offered!',
                                                     description=f"<@{interaction.user.id}> declined the trade",
                                                     colour=Colour.red())],
                                       view=None)
