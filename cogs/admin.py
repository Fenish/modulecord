import time
import discord

from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = "Admin"

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        begin = int(time.time_ns())
        embed = discord.Embed(color=0xaae6e2,
                              description="Reloading bot 🔄")
        message = await ctx.send(embed=embed)
        reload_message, error_message = await self.bot.reload_cogs()
        delta = int((int(time.time_ns()) - begin) / 1000000)
        embed.description = None
        embed.title = "🎉 Reload Complete"
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"{delta}Ms")
        for key in reload_message:
            embed.add_field(name=key, value="\n".join(reload_message[key]), inline=True)
        if error_message:
            embed.add_field(name="⚠️ Error Output", value=f"```py\n{error_message}\n```", inline=False)
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))