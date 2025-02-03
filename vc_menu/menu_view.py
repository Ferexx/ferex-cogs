from discord import ButtonStyle, Interaction, Embed
from discord.ui import View, Button
import discord
from .creation_modal import CreationModal
from .options_view import OptionsView
from .utils import can_manage_vc


class MenuView(View):
    @discord.ui.button(label='Create SFW Voice Chat', style=ButtonStyle.success, row=0)
    async def sfw_voice(self,
                        interaction: Interaction,
                        button: Button):
        await interaction.response.send_modal(CreationModal(title='SFW Voice Chat Creation'))

    @discord.ui.button(label='Create NSFW Voice Chat', style=ButtonStyle.success, row=0)
    async def nsfw_voice(self,
                         interaction: Interaction,
                         button: Button):
        await interaction.response.send_modal(CreationModal(title='NSFW Voice Chat Creation'))

    @discord.ui.button(label='Create SFW Cam Only Voice Chat', style=ButtonStyle.success, row=1)
    async def sfw_cam(self,
                      interaction: Interaction,
                      button: Button):
        await interaction.response.send_modal(CreationModal(title='SFW Cam Chat Creation'))

    @discord.ui.button(label='Create NSFW Cam Only Voice Chat', style=ButtonStyle.success, row=1)
    async def nsfw_cam(self,
                       interaction: Interaction,
                       button: Button):
        await interaction.response.send_modal(CreationModal(title='NSFW Cam Chat Creation'))

    @discord.ui.button(label='Open Voice Chat Options', style=ButtonStyle.secondary, row=2)
    async def options(self,
                      interaction: Interaction,
                      button: Button):
        if not await can_manage_vc(interaction):
            return
        await interaction.response.send_message(embeds=[Embed().add_field(name='Change Channel Name', value='This will change the name of your voice channel', inline=False)
                                                               .add_field(name='Change Voice Limit', value='This will change how many people can connect to your channel', inline=False)
                                                               .add_field(name='Toggle Cam Only', value='This will change whether people must have their cam turned on while in your VC', inline=False)
                                                               .add_field(name='Toggle NSFW', value='Change whether the VC is marked as SFW or NSFW')],
                                                view=OptionsView(),
                                                ephemeral=True)

    @discord.ui.button(label='Delete current Voice Chat', style=ButtonStyle.danger, row=3)
    async def delete(self,
                     interaction: Interaction,
                     button: Button):
        if not await can_manage_vc(interaction):
            return
        await interaction.user.voice.channel.delete()
        await interaction.response.send_message(content="Channel deleted", ephemeral=True)
