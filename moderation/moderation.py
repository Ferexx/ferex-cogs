from redbot.core import app_commands, commands, Config
from discord import Interaction, Message, ui, TextStyle, Embed, ButtonStyle, Colour, RawReactionActionEvent
from discord.embeds import EmbedProxy
from discord.ui import View, Button
import discord
from math import floor


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
        }
        self.config.register_global(**default_global)
        self.ctx_menu = app_commands.ContextMenu(name='Report Message',
                                                 callback=self.report)
        self.bot.tree.add_command(self.ctx_menu)

    async def report(self,
                     interaction: Interaction,
                     message: Message):
        await interaction.response.send_modal(ReportModal(custom_id=f"report_modal_{message.id}"))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,
                                  payload: RawReactionActionEvent):
        if payload.emoji.name != '❗':
            return
        if not any(role.name == 'staff' for role in payload.member.roles):
            return
        message_channel = self.bot.get_channel(payload.channel_id)
        message = await message_channel.fetch_message(payload.message_id)
        await message.delete()
        for channel in message.guild.channels:
            if channel.name == 'reports':
                reports_channel = channel
                break
        attachments = ''
        for attachment in message.attachments:
            attachments += f"\n{attachment.proxy_url}"

        embed = Embed(title="❗ Flagged Message",
                      colour=Colour.blue())
        embed.add_field(name='Staff', value=f"<@{payload.user_id}>")
        embed.add_field(name='Author', value=f"<@{payload.message_author_id}>")
        embed.add_field(name='Channel', value=f"<#{payload.channel_id}>")
        embed.add_field(name='Removed Messages', value=f"{message.content}{attachments}", inline=False)
        if message.reference is not None:
            embed.add_field(name='Replied To', value=f"{message.reference.cached_message.content}")
        embed.add_field(name='Original Message Date', value=f"{message.created_at.strftime('%A, %b %d, %Y %X (%Z)')}", inline=False)
        embed.set_footer(text=f"Author ID: {payload.message_author_id} / Staff ID: {payload.user_id}")

        await reports_channel.send(embeds=[embed])


class ReportModal(ui.Modal, title='Report Message'):
    reason = ui.TextInput(label='Why are you reporting this message?', style=TextStyle.paragraph)

    async def on_submit(self,
                        interaction: Interaction):
        await interaction.response.defer()
        message_id = self.custom_id.split('_')[2]
        for channel in interaction.guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.last_message is None:
                continue
            try:
                message = await channel.fetch_message(message_id)
                break
            except:
                continue
        for attachment in message.attachments:
            message.content += attachment.proxy_url + '\n'

        for channel in interaction.guild.channels:
            if channel.name == 'reports':
                reports_channel = channel
                break

        for role in interaction.guild.roles:
            if role.name == 'staff':
                staff_role = role
                break

        await reports_channel.send(content=f"<@&{staff_role.id}>, new report from <@{interaction.user.id}>",
                                   embeds=[Embed()
                                           .add_field(name='Reported User', value=f"<@{message.author.id}>", inline=False)
                                           .add_field(name='Message Content', value=message.content, inline=False)
                                           .add_field(name='Link', value=message.jump_url, inline=False)
                                           .add_field(name='Reason', value=self.reason, inline=False)],
                                   view=ButtonView())
        await interaction.followup.send(content='Thanks for your report. Our mod team will investigate as soon as possible.', ephemeral=True)


class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Handle', style=ButtonStyle.success)
    async def handle(self,
                     interaction: Interaction,
                     button: Button):
        fields = interaction.message.embeds[0].fields
        found = False
        for field in fields:
            if field.name == 'Staff':
                field.value += f"\n<@{interaction.user.id}> marked as handled <t:{floor(interaction.created_at.timestamp())}:R>"
                found = True
                break
        if not found:
            fields.append(EmbedProxy({'name': 'Staff', 'value': f"<@{interaction.user.id}> marked as handled <t:{floor(interaction.created_at.timestamp())}:R>", 'inline': False}))
        embed = Embed(colour=Colour.green())
        for field in fields:
            embed.add_field(name=field.name, value=field.value, inline=False)

        await interaction.message.edit(content=interaction.message.content,
                                       embeds=[embed])
        await interaction.response.defer()

    @discord.ui.button(label='Ignore', style=ButtonStyle.danger)
    async def ignore(self,
                     interaction: Interaction,
                     button: Button):
        fields = interaction.message.embeds[0].fields
        found = False
        for field in fields:
            if field.name == 'Staff':
                field.value += f"\n<@{interaction.user.id}> marked as ignored <t:{floor(interaction.created_at.timestamp())}:R>"
                found = True
                break
        if not found:
            fields.append(EmbedProxy({'name': 'Staff', 'value': f"<@{interaction.user.id}> marked as ignored <t:{floor(interaction.created_at.timestamp())}:R>", 'inline': False}))
        embed = Embed(colour=Colour.red())
        for field in fields:
            embed.add_field(name=field.name, value=field.value, inline=False)

        await interaction.message.edit(content=interaction.message.content,
                                       embeds=[embed])
        await interaction.response.defer()

    @discord.ui.button(label='In Progress', style=ButtonStyle.primary)
    async def in_progress(self,
                          interaction: Interaction,
                          button: Button):
        fields = interaction.message.embeds[0].fields
        found = False
        for field in fields:
            if field.name == 'Staff':
                field.value += f"\n<@{interaction.user.id}> marked as in progress <t:{floor(interaction.created_at.timestamp())}:R>"
                found = True
                break
        if not found:
            fields.append(EmbedProxy({'name': 'Staff', 'value': f"<@{interaction.user.id}> marked as in progress <t:{floor(interaction.created_at.timestamp())}:R>", 'inline': False}))
        embed = Embed(colour=Colour.blue())
        for field in fields:
            embed.add_field(name=field.name, value=field.value, inline=False)

        await interaction.message.edit(content=interaction.message.content,
                                       embeds=[embed])
        await interaction.response.defer()
