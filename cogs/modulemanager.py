import os
import sys
import discord
import requests
import pkg_resources

from urllib import request
from discord.ext import commands
from discord.ext.commands import Context
from subprocess import Popen, PIPE, STDOUT
from cogs.utils.filehandler import JsonFromUrl
from cogs.utils.paginator import PaginatorMenu, PaginatorSource


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

    def get_modules(self) -> list:
        module_repo = JsonFromUrl(self.bot.repository)
        module_list = []
        for module in module_repo:
            module_list.append(module.get("name").replace(".py", "").capitalize())
        return module_list

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def module(self, ctx: Context):
        await ctx.send("soon")

    @module.command()
    @commands.is_owner()
    async def search(self, ctx: Context, module_to_search):
        founded = []
        _m = self.get_modules()
        locale = self.bot.locale["ModuleManager"]

        for index, module in enumerate(_m):
            if module_to_search.lower() in module.lower():
                emoji = ":small_orange_diamond: "
                if index % 2 == 0:
                    emoji = ":small_blue_diamond: "
                founded.append(emoji + module)

        embed = discord.Embed(title="🧩 " + locale["title"],
                              colour=0x5bb8fd)
        embed.set_thumbnail(url="https://img.icons8.com/?id=46678&format=png&size=256")

        base_text = locale["search_found"].replace("{amount}", f"{len(founded)}")
        if len(founded) == 0:
            base_text = ""
            founded.append(locale["search_not_found"].replace("{prefix}", ctx.prefix))
            embed.colour = 0xff5357

        source = PaginatorSource(embed=embed, entries=founded, per_page=10, base_text=base_text)
        menu = PaginatorMenu(source)
        await menu.start(ctx)

    @module.command()
    @commands.is_owner()
    async def list(self, ctx: Context):
        modules_list = []
        _m = self.get_modules()
        locale = self.bot.locale["ModuleManager"]
        for index, module in enumerate(_m):
            emoji = ":small_orange_diamond: "
            if index % 2 == 0:
                emoji = ":small_blue_diamond: "
            modules_list.append(emoji + module)
        embed = discord.Embed(title="🧩 " + locale["title"],
                              colour=0x5bb8fd)
        embed.set_thumbnail(url="https://img.icons8.com/?id=46678&format=png&size=256")
        
        base_text = locale["list_description"].replace("{amount}",
                                                       str(len(modules_list))).replace("{prefix}",
                                                                                       ctx.prefix)
        source = PaginatorSource(embed=embed, entries=modules_list, per_page=10, base_text=base_text)
        menu = PaginatorMenu(source)
        await menu.start(ctx)

    @module.command()
    @commands.is_owner()
    async def install(self, ctx: Context, module):
        module = module.lower()
        locale = self.bot.locale["ModuleManager"]
        checking_module = locale["checking"].replace(
            "{module}", module
        )
        installing_module = locale["installing"].replace(
            "{module}", module
        )
        embed = discord.Embed(title="🧩 " + locale["title"],
                              description=checking_module,
                              colour=0xb153ff)
        status_msg = await ctx.send(embed=embed)

        embed.colour = 0xff5357
        github_module = self.check_on_repository(module)
        if github_module:
            if not os.path.exists("cogs/modules"):
                os.makedirs("cogs/modules")
            if not os.path.exists(f"cogs/modules/{module}.py"):
                embed.description = installing_module
                embed.colour = 0x86ff71
                await status_msg.edit(embed=embed)
                request.urlretrieve(github_module["download_url"], f"cogs/modules/{module}.py")

                repo_requirements = JsonFromUrl(self.bot.repodepencies)
                if repo_requirements.get(module):
                    required = set(repo_requirements[module])
                    installed = {pkg.key for pkg in pkg_resources.working_set}
                    missing = required - installed
                    depencies = []
                    for k in missing:
                        depencies.append(f"- **{k}**")

                    if missing:
                        installing_depencies = locale["installing_depencies"].replace(
                            "{depencies}", str("\n".join(depencies))
                        )

                        embed.description = installing_depencies
                        embed.colour = 0xf4f959
                        await status_msg.edit(embed=embed)
                        embed.colour = 0x86ff71
                        python = sys.executable
                        p = Popen([python, '-m', 'pip', 'install', *missing], stdout=PIPE,
                                  stderr=STDOUT, shell=False, encoding="utf-8")
                        p.wait()
                embed.description = locale["installed"]

            else:
                embed.description = locale["already_installed"]
        else:
            embed.description = locale["not_found"]
        return await status_msg.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(ModuleManager(bot))
