from discord import Interaction
from discord.ui import Modal, TextInput


class LimitChangeModal(Modal, title='Change VC Limit'):
    new_limit = TextInput(label='Voice Chat Limit', placeholder='New member limit')

    async def on_submit(self,
                        interaction: Interaction):
        try:
            await interaction.user.voice.channel.edit(user_limit=self.new_limit.value)
            await interaction.response.send_message(content='Limit changed',
                                                    ephemeral=True)
        except:
            await interaction.response.send_message(content='Invalid limit entered',
                                                    ephemeral=True)
