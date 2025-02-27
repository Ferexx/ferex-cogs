from discord import Member, VoiceState, Role, Message
from discord.ext import tasks
import sqlite3
import os
from math import floor
from datetime import datetime

from redbot.core import commands, Config


class TempRole(commands.Cog):
    """
    Commands to create and manage a temporary role
    """
    time_joined_vc = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'temp_role_id': 0,
            'messages_per_week': 0,
            'vc_minutes_per_week': 0
        }
        self.config.register_global(**default_global)
        self.db_conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/data.sqlite')
        self.db = self.db_conn.cursor()
        self.daily_checks.start()

    def cog_unload(self):
        self.daily_checks.cancel()

    @tasks.loop(hours=24)
    async def daily_checks(self):
        await self.clear_inactive_members()
        voice_logs = self.db.execute("SELECT * FROM voice_logs").fetchall()
        message_logs = self.db.execute("SELECT * FROM message_logs").fetchall()

        messages_per_week = await self.config.messages_per_week()
        vc_minutes_per_week = await self.config.vc_minutes_per_week()
        role_id = await self.config.temp_role_id()

        for i, voice_log in enumerate(voice_logs):
            total_voice_minutes = sum(voice_log[-7:])
            message_log = message_logs[i]
            total_messages = sum(message_log[-7:])

            member = await self.bot.guilds[0].fetch_member(voice_log[0])
            role = self.bot.guilds[0].get_role(role_id)

            if total_voice_minutes >= vc_minutes_per_week and total_messages >= messages_per_week:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

        today = datetime.now().strftime("%A")
        self.db.execute(f"UPDATE voice_logs SET {today} = 0")
        self.db.execute(f"UPDATE message_logs SET {today} = 0")
        self.db_conn.commit()

    async def clear_inactive_members(self):
        self.db.execute("DELETE FROM voice_logs WHERE Monday = 0 AND Tuesday = 0 AND Wednesday = 0 AND Thursday = 0 AND Friday = 0 AND Saturday = 0 AND Sunday = 0")
        self.db.execute("DELETE FROM message_logs WHERE Monday = 0 AND Tuesday = 0 AND Wednesday = 0 AND Thursday = 0 AND Friday = 0 AND Saturday = 0 AND Sunday = 0")
        self.db_conn.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: Member,
                                    before: VoiceState,
                                    after: VoiceState):
        if not before.channel and after.channel:
            if len(before.channel.members) > 1:
                self.start_tracking_vc_time(member.id)
        if before.channel and not after.channel:
            if len(before.channel.members) > 1:
                self.stop_tracking_vc_time(member.id)
        if before.channel and after.channel:
            if len(before.channel.members) > 1 and len(after.channel.members) < 2:
                self.stop_tracking_vc_time(before.channel.members)
            if len(before.channel.members) < 2 and len(after.channel.members) > 1:
                self.start_tracking_vc_time(before.channel.members)

    async def start_tracking_vc_time(self,
                                     members):
        for member in members:
            self.time_joined_vc[member.id] = datetime.now()

    async def stop_tracking_vc_time(self,
                                    members):
        for member in members:
            await self.add_user_to_db(member.id)

        today = datetime.now().strftime('%A')
        existing_time = self.db.execute(f"SELECT {today} FROM voice_logs WHERE uid = ?", [id]).fetchone()[0]
        new_time = floor((datetime.now() - self.time_joined_vc[id]).total_seconds() / 60)
        total_time = int(existing_time) + new_time

        self.db.execute(f"UPDATE voice_logs SET {today} = ? WHERE uid = ?", [total_time, id])
        self.db_conn.commit()

    @commands.Cog.listener()
    async def on_message(self,
                         message: Message):
        if message.author.bot:
            return
        await self.daily_checks()
        id = message.author.id
        await self.add_user_to_db(id)

        today = datetime.now().strftime('%A')
        existing_messages = self.db.execute(f"SELECT {today} FROM message_logs WHERE uid = ?", [id]).fetchone()[0]
        total_messages = int(existing_messages) + 1

        self.db.execute(f"UPDATE message_logs SET {today} = ? WHERE uid = ?", [total_messages, id])
        self.db_conn.commit()

    async def add_user_to_db(self,
                             id):
        try:
            self.db.execute("INSERT INTO voice_logs (uid, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) VALUES (?, 0, 0, 0, 0, 0, 0, 0)", [id])
            self.db.execute("INSERT INTO message_logs (uid, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) VALUES (?, 0, 0, 0, 0, 0, 0, 0)", [id])
            self.db_conn.commit()
        except:
            return

    @commands.group(invoke_without_command=False)
    async def temp_role(self,
                        ctx):
        return

    @temp_role.command()
    async def set_role(self,
                       ctx,
                       role: Role):
        await self.config.temp_role_id.set(role.id)
        await ctx.send('Role set')

    @temp_role.command()
    async def set_messages(self,
                           ctx,
                           messages: int):
        await self.config.messages_per_week.set(messages)
        await ctx.send('Minimum messages per week set')

    @temp_role.command()
    async def set_vc_minutes(self,
                             ctx,
                             minutes: int):
        await self.config.vc_minutes_per_week.set(minutes)
        await ctx.send('Minimum VC minutes per week set')
