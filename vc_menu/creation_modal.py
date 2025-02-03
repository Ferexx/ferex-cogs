from discord import Interaction, PermissionOverwrite
from discord.ui import Modal, TextInput
from . import utils


class CreationModal(Modal, title='Create VC'):
    vc_title = TextInput(label='Voice Chat Title', placeholder='Your voice chat title')
    vc_capacity = TextInput(label='Voice Chat Capacity', placeholder='Max users')

    async def on_submit(self,
                        interaction: Interaction):
        if 'NSFW' in self.title:
            the_category = next((x for x in interaction.guild.channels if x.id == utils.nsfw_id), None)
        else:
            the_category = next((x for x in interaction.guild.channels if x.id == utils.sfw_id), None)

        if not the_category:
            await interaction.response.send_message(content='Could not find the category to create the VC in, please contact a staff member', ephemeral=True)
            return

        if 'Cam' in self.title:
            the_title = f'[📷] {self.vc_title.value}'
        else:
            the_title = self.vc_title.value

        the_permissions = default_permissions(interaction)

        try:
            created_channel = await interaction.guild.create_voice_channel(
                    name=the_title,
                    category=the_category,
                    overwrites=the_permissions,
                    user_limit=self.vc_capacity.value
            )
            if interaction.user.voice:
                await interaction.user.move_to(created_channel)
            await interaction.response.send_message(content='VC created', ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content='I ran into an issue making your VC, please try again later', ephemeral=True)


def default_permissions(interaction: Interaction):
    muted = next(filter(lambda role: (role.name == 'muted'), interaction.guild.roles))
    admin = next(filter(lambda role: (role.name == 'admin'), interaction.guild.roles))
    senior_mod = next(filter(lambda role: (role.name == 'senior mod'), interaction.guild.roles))
    unverified = next(filter(lambda role: (role.name == 'unverified'), interaction.guild.roles))
    is_donator = any(True for _ in filter(lambda role: (role.name == 'donator'), interaction.user.roles))

    permissions_dict = {
        muted: PermissionOverwrite(view_channel=False),
        unverified: PermissionOverwrite(view_channel=False),
        admin: PermissionOverwrite(manage_channels=True),
        senior_mod: PermissionOverwrite(manage_channels=True),
    }
    if is_donator:
        permissions_dict[interaction.user] = PermissionOverwrite(manage_roles=True, manage_channels=True)
    else:
        permissions_dict[interaction.user] = PermissionOverwrite(manage_channels=True)

    return permissions_dict
