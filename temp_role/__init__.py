from .temp_role import TempRole


async def setup(bot):
    await bot.add_cog(TempRole(bot))
