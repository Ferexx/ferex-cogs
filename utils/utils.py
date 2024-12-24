from redbot.core import commands, app_commands, Config
from discord import Interaction, Embed, Invite, Member
from math import floor
from .invites import log_join, log_leave


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
        }
        self.config.register_global(**default_global)
        self.invites = {}
        self.vanity_invite = None
        self.bot.loop.create_task(self.initialise_invites())

    async def initialise_invites(self):
        await self.bot.wait_until_ready()

        first_invites = await self.bot.guilds[0].invites()
        for invite in first_invites:
            self.invites[invite.code] = invite.uses
        try:
            vanity_invite = await self.bot.guilds[0].vanity_invite()
            if vanity_invite:
                self.vanity_invite = {
                    'code': vanity_invite.code,
                    'uses': vanity_invite.uses
                }
        except:
            pass

    @app_commands.command(name='countdown',
                          description="Returns a time in Discord's countdown format")
    @app_commands.describe(minutes="In how many minutes should this countdown reach 0")
    async def countdown(self,
                        interaction: Interaction,
                        minutes: int):
        time = floor(interaction.created_at.timestamp()) + (minutes * 60)
        await interaction.response.send_message(f"<t:{time}:R>\nCopy and paste this: `<t:{time}:R>`")

    @app_commands.command(name='invitesleaderboard',
                          description='Print the most used invites in order')
    async def invites_leaderboard(self,
                                  interaction: Interaction):
        invites = await interaction.guild.invites()
        invites.sort(key=lambda invite: invite.uses, reverse=True)
        built_string = ''
        for invite in invites:
            if invite.uses > 0:
                built_string += f"<@{invite.inviter.id}> - {invite.uses} uses\n"

        await interaction.response.send_message(embeds=[Embed(title='Invite Leaderboard',
                                                              description=built_string)])

    @commands.Cog.listener()
    async def on_invite_create(self,
                               invite: Invite):
        self.invites[invite.code] = invite.uses

    @commands.Cog.listener()
    async def on_member_join(self,
                             member: Member):
        await log_join(self.invites, self.vanity_invite, member)

    @commands.Cog.listener()
    async def on_member_remove(self,
                               member: Member):
        await log_leave(member)
