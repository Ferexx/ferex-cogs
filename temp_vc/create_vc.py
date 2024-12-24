from discord import Interaction, PermissionOverwrite, Embed, ButtonStyle
from discord.ui import View, Button
import discord


async def send_vc_embed(ctx):
    await ctx.channel.send(embeds=[Embed(title='How to make a custom VC',
                                         description='Simply click the "Create a VC" button at the bottom of this post to create your own temporary VC! Once made, you will have the permissions to change the VC\'s name and size. If you are a donator you will have full control of the permissions of your VC.')],
                           view=CreationView())


async def create_vc(interaction: Interaction,
                    vc_name: str = None):
    if vc_name is None:
        vc_name = f'{interaction.user.name}\'s VC'

    muted = next(filter(lambda role: (role.name == 'muted'), interaction.guild.roles))
    admin = next(filter(lambda role: (role.name == 'admin'), interaction.guild.roles))
    senior_mod = next(filter(lambda role: (role.name == 'senior mod'), interaction.guild.roles))
    unverified = next(filter(lambda role: (role.name == 'unverified'), interaction.guild.roles))
    is_donator = any(True for _ in filter(lambda role: (role.name == 'donator'), interaction.user.roles))
    category = next(filter(lambda channel: (channel.name == 'mercurial vcs'), interaction.guild.channels))

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

    try:
        created_channel = await interaction.guild.create_voice_channel(
                name=vc_name,
                category=category,
                overwrites=permissions_dict
        )
        if interaction.user.voice:
            await interaction.user.move_to(created_channel)
        await interaction.response.send_message(content='VC created', ephemeral=True)
    except Exception:
        await interaction.response.send_message(content='I ran into an issue making your VC, please try again later', ephemeral=True)


class CreationView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Create a VC', style=ButtonStyle.success)
    async def create(self,
                     interaction: Interaction,
                     button: Button):
        await create_vc(interaction)
