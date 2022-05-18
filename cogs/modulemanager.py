from discord.ext import commands


class ModuleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def modules(self, ctx):
        await ctx.send("Coming Soon")


async def setup(bot):
    await bot.add_cog(ModuleManager(bot))