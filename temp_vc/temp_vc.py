from discord import Interaction, Member, VoiceChannel, ButtonStyle
from discord.ui import View, Button
import discord
from .create_vc import send_vc_embed, create_vc

from redbot.core import commands, Config, app_commands


class TempVc(commands.Cog):
    """
    Commands to create and manage temporary VCs
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'temp_vc_category_id': 0
        }
        self.config.register_global(**default_global)

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        if not before.channel:
            return
        if len(before.channel.members) == 0 and before.channel.category.name == 'mercurial vcs':
            await before.channel.delete()

    @commands.command()
    async def create_vc(self,
                        ctx):
        await send_vc_embed(ctx)

    @app_commands.command(name='cv',
                          description='Create a temporary VC')
    @app_commands.describe(vc_name='The name to give to the VC')
    async def cv(self,
                 interaction: Interaction,
                 vc_name: str = None):
        await create_vc(interaction, vc_name)

    @app_commands.command(name='ownership',
                          description='Transfer ownership of a temporary VC')
    @app_commands.describe(new_owner='The member to transfer ownership to')
    async def ownership(self,
                        interaction: Interaction,
                        new_owner: Member):
        if not isinstance(interaction.channel, VoiceChannel):
            await interaction.response.send_message('This command can only be run in a VC\'s side channel')
            return
        if interaction.channel.category.name != 'mercurial vcs':
            await interaction.response.send_message('This command can only be run on mercurial VCs')
            return
        current_owner = None
        try:
            current_owner = next(filter(lambda overwrite: (isinstance(overwrite, Member)), interaction.channel.overwrites))
        except Exception:
            await interaction.response.send_message('This command can only be run on mercurial VCs')
            return
        if current_owner != interaction.user:
            await interaction.response.send_message('This command can only be run by the VC owner')

        await interaction.channel.set_permissions(current_owner, overwrite=None)
        await interaction.channel.set_permissions(new_owner, manage_channels=True)

        await interaction.response.send_message(f'Ownership transferred to <@{new_owner.id}>')

    @app_commands.command(name='letmein',
                          description='Ask the VC owner to make space in the VC for you')
    async def letmein(self,
                      interaction: Interaction):
        if not isinstance(interaction.channel, VoiceChannel):
            await interaction.response.send_message(content='This command can only be run in a VC\'s side channel', ephemeral=True)
            return
        if len(interaction.channel.members) < interaction.channel.user_limit:
            await interaction.response.send_message('There is already space in this VC')
            return
        current_owner = None
        try:
            current_owner = next(filter(lambda overwrite: (isinstance(overwrite, Member)), interaction.channel.overwrites))
        except Exception:
            await interaction.response.send_message('This command can only be run on a VC owned by a member')
            return

        await interaction.channel.send(content=f'<@{current_owner.id}>, <@{interaction.user.id}> is requesting to join the VC, do you want to let them in?',
                                       view=ButtonView())
        await interaction.response.send_message(content='Request sent', ephemeral=True)


class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Accept', style=ButtonStyle.success)
    async def confirm(self,
                      interaction: Interaction,
                      button: Button):
        current_owner = next(filter(lambda overwrite: (isinstance(overwrite, Member)), interaction.channel.overwrites))
        if interaction.user.id != current_owner.id:
            await interaction.response.send_message('Only the VC owner can accept this request', ephemeral=True)
            return
        await interaction.channel.edit(user_limit=interaction.channel.user_limit+1)
        await interaction.response.send_message('VC size increased')
