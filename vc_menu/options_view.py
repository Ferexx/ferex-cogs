from discord import Interaction
from discord.ui import View, Button
import discord
from . import utils
from .name_change_modal import NameChangeModal
from .limit_change_modal import LimitChangeModal


class OptionsView(View):
    @discord.ui.button(label='Change Channel Name', row=0)
    async def change_name(self,
                          interaction: Interaction,
                          button: Button):
        if not interaction.user.voice:
            await interaction.response.send_message(content='You are not connected to a voice channel',
                                                    ephemeral=True)
        await interaction.response.send_modal(NameChangeModal())

    @discord.ui.button(label='Change Voice Limit', row=0)
    async def change_limit(self,
                           interaction: Interaction,
                           button: Button):
        if not interaction.user.voice:
            await interaction.response.send_message(content='You are not connected to a voice channel',
                                                    ephemeral=True)
        await interaction.response.send_modal(LimitChangeModal())

    @discord.ui.button(label='Toggle Cam Only', row=1)
    async def change_cam_only(self,
                              interaction: Interaction,
                              button: Button):
        if not interaction.user.voice:
            await interaction.response.send_message(content='You are not connected to a voice channel',
                                                    ephemeral=True)
        voice_channel = interaction.user.voice.channel
        if '📷' in voice_channel.name:
            await voice_channel.edit(name=voice_channel.name[4:])
        else:
            await voice_channel.edit(name=f"[📷] {voice_channel.name}")

        await interaction.response.send_message(content='Cam requirement changed',
                                                ephemeral=True)

    @discord.ui.button(label='Toggle Category', row=1)
    async def change_sfw(self,
                         interaction: Interaction,
                         button: Button):
        if not interaction.user.voice:
            await interaction.response.send_message(content='You are not connected to a voice channel',
                                                    ephemeral=True)
        voice_channel = interaction.user.voice.channel
        sfw_category = await interaction.guild.fetch_channel(utils.sfw_id)
        nsfw_category = await interaction.guild.fetch_channel(utils.nsfw_id)
        if voice_channel.category.id == utils.sfw_id:
            await voice_channel.edit(category=nsfw_category)
        else:
            await voice_channel.edit(category=sfw_category)
        await interaction.response.send_message(content='Channel category changed',
                                                ephemeral=True)
