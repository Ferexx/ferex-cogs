from discord import Interaction, User, Message
from .waifuinfo import get_waifu_info
from .timely import get_timely
from .gift import gift_letters_command
from .balance import check_balance
from .award import award_letters
from .take import take_letters_command
from .give import give_letters
from .claim import claim_waifu
from .divorce import divorce_waifu
from .leaderboard import waifu_leaderboard
from .shop import letters_shop
from .trade import trade_letters
from .waifutransfer import waifu_transfer
from .picks import award_pick_if_correct_word, generate_pick_if_lucky

from redbot.core import commands, app_commands, Config
from redbot.core import checks


class Waifus(commands.Cog):
    """
    Commands for running the waifu game
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='06081999', force_registration=True)
        default_global = {
            'waifus': []
        }
        self.config.register_global(**default_global)
        self.activePick = {}

    @app_commands.command(name="timely",
                          description="Claim your timely reward")
    async def timely(self,
                     interaction: Interaction):
        await get_timely(interaction)

    @app_commands.command(name='waifuinfo',
                          description='Get info about a waifu')
    async def waifuinfo(self,
                        interaction: Interaction,
                        user: User = None):
        await get_waifu_info(interaction, user)

    @app_commands.command(name='gift',
                          description='Gift letters to a waifu')
    async def gift(self,
                   interaction: Interaction,
                   waifu: User,
                   letters: str):
        await gift_letters_command(interaction, waifu, letters)

    @app_commands.command(name='balance',
                          description='See how many letters you currently have')
    async def balance(self,
                      interaction: Interaction):
        await check_balance(interaction)

    @app_commands.command(name='give',
                          description='Give letters to another waifu')
    async def give(self,
                   interaction: Interaction,
                   waifu: User,
                   letters: str):
        await give_letters(interaction, waifu, letters)

    @app_commands.command(name='claim',
                          description='Claim another waifu')
    async def claim(self,
                    interaction: Interaction,
                    waifu: User):
        await claim_waifu(interaction, waifu)

    @app_commands.command(name='divorce',
                          description='Divorce an owned waifu')
    async def divorce(self,
                      interaction: Interaction,
                      waifu: User):
        await divorce_waifu(interaction, waifu)

    @app_commands.command(name='leaderboard',
                          description='Waifu leaderboard')
    async def leaderboard(self,
                          interaction: Interaction,
                          page: int = 0):
        await waifu_leaderboard(interaction, page)

    @app_commands.command(name='shop',
                          description='Exchange letters for numbers/symbols')
    async def shop(self,
                   interaction: Interaction,
                   buying: str,
                   selling: str):
        await letters_shop(interaction, buying, selling)

    @app_commands.command(name='trade',
                          description='Trade letters with another user')
    async def trade(self,
                    interaction: Interaction,
                    waifu: User,
                    offering: str,
                    wanting: str):
        await trade_letters(interaction, waifu, offering, wanting)

    @app_commands.command(name='waifutransfer',
                          description='Transfer a waifu to another user')
    async def waifutransfer(self,
                            interaction: Interaction,
                            waifu: User,
                            recipient: User):
        await waifu_transfer(interaction, waifu, recipient)

    @commands.guild_only()
    @commands.group(name='waifus')
    async def _waifus(self, ctx: commands.GuildContext):
        pass

    @checks.is_owner()
    @_waifus.command(name='award')
    async def award(self,
                    ctx: commands.GuildContext,
                    waifu: User,
                    letters: str):
        await award_letters(ctx, waifu, letters)

    @checks.is_owner()
    @_waifus.command(name='take')
    async def take(self,
                   ctx: commands.GuildContext,
                   waifu: User,
                   letters: str):
        await take_letters_command(ctx, waifu, letters)

    @commands.Cog.listener()
    async def on_message(self,
                         message: Message):
        if message.author.bot:
            return
        if not message.channel.name == 'chat':
            return
        if self.activePick:
            await award_pick_if_correct_word(message, self.activePick)
        else:
            self.activePick = await generate_pick_if_lucky(message)
