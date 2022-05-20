import os
import sys
import discord
import requests
import importlib
import pkg_resources

from urllib import request
from discord.ext import commands
from subprocess import Popen, PIPE, STDOUT


class ModuleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_on_repository(self, module):
        module_name = module + ".py"
        req = requests.get(self.bot.repository)
        json = req.json()
        for key in json:
            if key["name"] == module_name:
                return key
        return {}

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def module(self, ctx):
        await ctx.send("soon")

    @module.command()
    @commands.is_owner()
    async def install(self, ctx, module):
        embed = discord.Embed(title="🧩 Module Manager",
                              description=f"Checking for module `{module}`",
                              colour=0xb153ff)
        status_msg = await ctx.send(embed=embed)
        embed.colour = 0xff5357
        github_module = self.check_on_repository(module)
        if github_module:
            if not os.path.exists("modules"):
                os.makedirs("modules")
            if not os.path.exists(f"modules/{module}"):
                embed.description = f"Installing `{module}`"
                embed.colour = 0x86ff71
                await status_msg.edit(embed=embed)
                request.urlretrieve(github_module["download_url"], f"modules/{module}.py")
                embed.description = "Module installed successfully you can reload bot for apply changes"
            else:
                embed.description = "Module already installed"
        else:
            embed.description = "Module not found"

        installed_module = importlib.import_module(f"modules.{module}")
        try:
            required = installed_module.modules
            installed = {pkg.key for pkg in pkg_resources.working_set}
            missing = required - installed
            depencies = []
            for k in missing:
                depencies.append(f"- **{k}**")

            if missing:
                embed.description = "Installing depencies\n\n{}".format("\n".join(depencies))
                embed.colour = 0xf4f959
                await status_msg.edit(embed=embed)

                python = sys.executable
                p = Popen([python, '-m', 'pip', 'install', *missing], stdout=PIPE,
                          stderr=STDOUT, shell=True, encoding="utf-8")
                p.wait()

            embed.colour = 0x86ff71
            embed.description = "Module installed successfully you can reload bot for apply changes"
        except AttributeError:
            pass
        return await status_msg.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(ModuleManager(bot))
