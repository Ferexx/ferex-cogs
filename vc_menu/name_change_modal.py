from discord import Interaction
from discord.ui import Modal, TextInput


class NameChangeModal(Modal, title='Change VC Name'):
    new_title = TextInput(label='Voice Chat Title', placeholder='Your new title')

    async def on_submit(self,
                        interaction: Interaction):
        voice_channel = interaction.user.voice.channel
        if '📷' in voice_channel.name:
            self.new_title.value = f"[📷] {self.new_title.value}"
        await voice_channel.edit(name=self.new_title.value)
        await interaction.response.send_message(content='Title changed',
                                                ephemeral=True)
