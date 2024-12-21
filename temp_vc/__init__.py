from .temp_vc import TempVc


async def setup(bot):
    await bot.add_cog(TempVc(bot))
