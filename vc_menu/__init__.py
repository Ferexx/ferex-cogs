from .vc_menu import VcMenu


async def setup(bot):
    cog = VcMenu(bot)
    await cog.initialise()
    await bot.add_cog(cog)
