from discord import Embed, Interaction, VoiceState, Member, VoiceChannel
from discord.abc import GuildChannel
import asyncio
from redbot.core import commands, Config, app_commands
from .menu_view import MenuView
from . import utils


class VcMenu(commands.Cog):
    cam_timers = {}
    vc_logs_channel = None

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'sfw_vc_category_id': 0,
            'nsfw_vc_category_id': 0,
            'cam_timeout': 60,
            'ban_time': 3600,
            'vc_logs_channel_id': 0,
        }
        self.config.register_global(**default_global)

    async def initialise(self):
        utils.sfw_id = await self.config.sfw_vc_category_id()
        utils.nsfw_id = await self.config.nsfw_vc_category_id()
        try:
            self.vc_logs_channel = await self.bot.fetch_channel(await self.config.vc_logs_channel_id())
        except:
            print('Could not find VC logs channel')

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: Member,
                                    before: VoiceState,
                                    after: VoiceState):
        if before.channel and (before.channel.category.name == "SFW voice" or before.channel.category.name == "NSFW voice"):
            channel = await self.bot.fetch_channel(before.channel.id)
            if len(channel.members) == 0:
                await before.channel.delete()
        if not after.channel:
            self.cancel_disconnect_timer(member.id)
            return
        if not after.self_video and '📷' in after.channel.name:
            staff_role = next(filter(lambda role: (role.name == "staff"), member.guild.roles))
            if staff_role in member.roles:
                return
            await self.warn_member(member.id)
            self.cam_timers[member.id] = asyncio.create_task(self.disconnect_member(member))
            return
        if after.self_video or '📷' not in after.channel.name:
            self.cancel_disconnect_timer(member.id)

    @commands.Cog.listener()
    async def on_guild_channel_update(self,
                                      before: GuildChannel,
                                      after: GuildChannel):
        if not isinstance(after, VoiceChannel):
            return
        if '📷' not in before.name and '📷' in after.name:
            for member in after.members:
                await self.warn_member(member.id)
                self.cam_timers[member.id] = asyncio.create_task(self.disconnect_member(member))
        if '📷' in before.name and '📷' not in after.name:
            for member in after.members:
                self.cancel_disconnect_timer(member.id)

    async def warn_member(self,
                          member_id: int):
        cam_timeout = await self.config.cam_timeout()
        await self.vc_logs_channel.send(content=f"<@{member_id}>", embeds=[Embed(description=f"You have joined a VC that is designated as cam-only. Please turn on your cam within {cam_timeout} seconds or you will be disconnected.")])

    def cancel_disconnect_timer(self,
                                member_id: int):
        if member_id in self.cam_timers:
            self.cam_timers[member_id].cancel()
            del self.cam_timers[member_id]

    async def disconnect_member(self,
                                member: Member):
        await asyncio.sleep(await self.config.cam_timeout())
        await member.move_to(None)
        await self.vc_logs_channel.send(content=f"<@{member.id}>", embeds=[Embed(description="You were disconnected for failing to turn on your cam in time.")])
        del self.cam_timers[member.id]

    @commands.group(invoke_without_command=False)
    async def vc(self,
                 ctx):
        return

    @vc.command()
    async def set_ban_time(self,
                           ctx,
                           time: int):
        await self.config.ban_time.set(time)
        await ctx.send('Ban time set (time in seconds)')

    @vc.command()
    async def menu(self,
                   ctx):
        await ctx.channel.send(embeds=[Embed(title='VC Menu by Ferex', description='*Create a VC simply by clicking one of the two buttons below*\n\n**SFW Voice Chat**\nThis will create a Voice Chat in the SFW Section.\n\n**NSFW Voice Chat**\nThis will create a Voice Chat in the NSFW Section.\n\n**Open Voice Chat Options for more commands.**')],
                               view=MenuView())

    @vc.command()
    async def set_cam_timeout(self,
                              ctx,
                              timeout: int):
        await self.config.cam_timeout.set(timeout)
        await ctx.send('Cam timeout set')

    @vc.command()
    async def set_sfw_category(self,
                               ctx,
                               category_id: int):
        if not next((x for x in ctx.guild.channels if x.id == category_id), None):
            await ctx.send('That category ID does not match any category')
            return
        await self.config.sfw_vc_category_id.set(category_id)
        utils.sfw_id = category_id
        await ctx.send('SFW VC Category set')

    @vc.command()
    async def set_nsfw_category(self,
                                ctx,
                                category_id: int):
        if not next((x for x in ctx.guild.channels if x.id == category_id), None):
            await ctx.send('That category ID does not match any category')
            return
        await self.config.nsfw_vc_category_id.set(category_id)
        utils.nsfw_id = category_id
        await ctx.send('NSFW VC Category set')

    @vc.command()
    async def set_logs_channel(self,
                               ctx,
                               channel_id: int):
        try:
            vc_channel = await ctx.guild.fetch_channel(channel_id)
            await self.config.vc_logs_channel_id.set(channel_id)
            self.vc_logs_channel = vc_channel
            await ctx.send('VC Logs channel set')
        except Exception as e:
            print(e)
            await ctx.send('That channel ID does not match any channel')

    @app_commands.command(name='tempban',
                          description='Temporarily ban a user from your VC')
    @app_commands.describe(member='The member to ban')
    async def tempban(self,
                      interaction: Interaction,
                      member: Member):
        if not await utils.can_manage_vc(interaction):
            return

        voice_channel = interaction.user.voice.channel
        if member.voice:
            await member.move_to(None)
        await voice_channel.set_permissions(member, connect=False)
        asyncio.create_task(self.unban_member(voice_channel, member))
        await interaction.response.send_message(content='Member banned',
                                                ephemeral=True)

    async def unban_member(self,
                           channel: GuildChannel,
                           member: Member):
        await asyncio.sleep(await self.config.ban_time())
        await channel.set_permissions(member, connect=True)


