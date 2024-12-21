import discord

from redbot.core import commands, app_commands, Config
import random


class FunCommands(commands.Cog):
    """
    Some fun commands to use in chat
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'tallies': {}
        }
        self.config.register_global(**default_global)

    @app_commands.command(name='competence',
                          description='Find out how competent you are today')
    async def competence(self,
                         interaction: discord.Interaction):
        favourites = await self.bot[0].get_cog("BotFavourites").config.bot_favourites()
        competence = random.uniform(0, 100)
        if interaction.user.id in favourites:
            competence = 100.00
        await interaction.response.send_message(f'<@{interaction.user.id}> is {competence:.2f}% competent today')

    @app_commands.command(name='ppsize',
                          description='Find out how long your pp really is')
    async def ppsize(self,
                     interaction: discord.Interaction):
        message = '<:head:1024096164104122421>'
        favourites = await self.bot[0].get_cog('BotFavourites').config.bot_favourites()
        count = random.randint(0, 30)
        if interaction.user.id in favourites:
            count = 30
        message += '<:body:1024096166306140262>' * count
        message += '<:butt:1024096168725586176>'
        await interaction.response.send_message(message)

    @app_commands.command(name='tally',
                          description='Add a tally to a user, or check how many tallies you have received')
    @app_commands.describe(user='User to add a tally to, leave blank to check how many tallies you have received')
    async def tally(self,
                    interaction: discord.Interaction,
                    user: discord.Member = None):
        if user is None:
            user = interaction.user
        allTallies = await self.config.tallies()
        talliesReceived = 0
        if user.id in allTallies:
            talliesReceived = allTallies.get(user.id)
        if user is interaction.user:
            await interaction.response.send_message(f'<@{interaction.user.id}> has {talliesReceived} tallies')
        else:
            if user.id in await self.bot[0].get_cog("BotFavourites").config.bot_favourites():
                await interaction.response.send_message(f'I like <@{user.id}>, you can\'t tally them')
                return
            allTallies.update({f'{user.id}': talliesReceived + 1})
            await self.config.tallies.set(allTallies)
            await interaction.response.send_message(f'Tally added to <@{user.id}>', ephemeral=True)
