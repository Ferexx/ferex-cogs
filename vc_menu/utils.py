sfw_id = None
nsfw_id = None


async def can_manage_vc(interaction):
    if not interaction.user.voice:
        await interaction.response.send_message(content='You are not connected to a VC',
                                                ephemeral=True)
        return False
    permissions = interaction.user.voice.channel.permissions_for(interaction.user)
    if not permissions.manage_channels:
        await interaction.response.send_message(content='You cannot manage this channel',
                                                ephemeral=True)
        return False
    return True
