from .bot_favourites import BotFavourites


async def setup(bot):
    await bot.add_cog(BotFavourites(bot))
