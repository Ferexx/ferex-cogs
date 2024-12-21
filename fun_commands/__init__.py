from .fun_commands import FunCommands


async def setup(bot):
    await bot.add_cog(FunCommands(bot))
