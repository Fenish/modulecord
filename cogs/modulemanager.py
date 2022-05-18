import sys
import discord
import requests
import importlib
import pkg_resources

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
    async def module(self, ctx):
        await ctx.send("soon")

    @module.command()
    async def install(self, ctx):
        self.check_on_repository("autorole")

async def setup(bot):
    await bot.add_cog(ModuleManager(bot))
