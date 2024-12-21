import discord

from redbot.core import commands, app_commands, Config


class BotFavourites(commands.Cog):
    """
    Some fun commands to use in chat
    """

    def __init__(self, bot):
        self.bot = bot,
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'bot_favourites': []
        }
        self.config.register_global(**default_global)

    @app_commands.command(name='add_favourite',
                          description='Add a user to the bot\'s favourites')
    @app_commands.describe(user_to_add='User to add to favourites')
    async def add_favourite(self,
                            interaction: discord.Interaction,
                            user_to_add: discord.Member):
        favourites = await self.config.bot_favourites()
        if (user_to_add.id in favourites):
            await interaction.response.send_message(f'<@{user_to_add.id}> is already one of my favourites')
            return
        favourites.append(user_to_add.id)
        await self.config.bot_favourites.set(favourites)
        await interaction.response.send_message(f'<@{user_to_add.id}> added to my favourites')

    @app_commands.command(name='remove_favourite',
                          description='Remove a user from the bot\'s favourites')
    @app_commands.describe(user_to_remove='User to remove from favourites')
    async def remove_favourite(self,
                               interaction: discord.Interaction,
                               user_to_remove: discord.Member):
        favourites = await self.config.bot_favourites()
        if (user_to_remove.id not in favourites):
            await interaction.response.send_message(f'<@{user_to_remove.id}> is not one of my favourites')
            return
        favourites.remove(user_to_remove.id)
        await self.config.bot_favourites.set(favourites)
        await interaction.response.send_message(f'<@{user_to_remove.id}> removed from my favourites')

    @app_commands.command(name='list_favourites',
                          description='List my favourites')
    async def list_favourites(self,
                              interaction: discord.Interaction):
        favourites = await self.config.bot_favourites()
        reply = 'My favourite users: '
        for favourite in favourites:
            reply += f'<@{favourite}>, '
        await interaction.response.send_message(reply)
