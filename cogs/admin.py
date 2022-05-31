import time
import discord

from discord.ext import commands
from discord.ext.commands import Context


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = "Admin"

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: Context):
        begin = int(time.time_ns())
        embed = discord.Embed(
            color=0xAAE6E2, description=self.bot.locale["Admin"]["reloading"] + " 🔄"
        )
        message = await ctx.send(embed=embed)
        reload_message, error_message = await self.bot.reload_cogs()
        delta = int((int(time.time_ns()) - begin) / 1000000)
        embed.description = None
        embed.title = "🎉 " + self.bot.locale["Admin"]["reload_complete"]
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"{delta}Ms")
        for key in reload_message:
            embed.add_field(name=key, value="\n".join(reload_message[key]), inline=True)
        if error_message:
            embed.add_field(
                name=f"⚠️ {self.bot.locale['Admin']['reload_error']}",
                value=f"```py\n{error_message}\n```",
                inline=False,
            )
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
