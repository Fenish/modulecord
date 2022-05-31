import sys
import traceback
from pathlib import Path

import discord
from discord.ext import commands

from cogs.utils.filehandler import YamlFile, Locale


class ModuleCord(commands.Bot):
    async def sync_commands(self) -> None:
        pass

    def __init__(self):
        self.locale = {}
        self.config = YamlFile("config/config.yml")
        super().__init__(
            intents=discord.Intents.all(),
            case_insensitive=True,
            command_prefix=self.config["Prefix"],
        )

        self.repository = (
            "https://api.github.com/repos/Fenish/modulecord-modules/contents/modules"
        )
        self.repodepencies = (
            "https://raw.githubusercontent.com/Fenish/"
            "modulecord-modules/main/requirements.json"
        )

        try:
            act_type = self.config["Presence"]["Type"]
            name = self.config["Presence"]["Text"]
            status = self.config["Presence"]["Status"]

            name = name.replace("<prefix>", self.command_prefix)

            for activity_type in discord.ActivityType:
                if act_type.lower() in str(activity_type):
                    act_type = activity_type
                    break

            for status_name in discord.Status:
                if status.lower() == str(status_name):
                    status = status_name
                    break

            if isinstance(act_type, str):
                raise ValueError("Type")

            if isinstance(status, str):
                raise ValueError("Status")

        except KeyError as e:
            print("##################################################")
            print("There is an error on config.yml")
            print("No Key Found")
            print(f"KEY: {e}")
            print("##################################################")
            return

        except ValueError as e:
            print("##################################################")
            print("There is an error on config.yml")
            print("Invalid Value")
            print(f"Key: {e}")
            print("##################################################")
            return
        self.activity = discord.Activity(type=act_type, name=name)
        self.status = status

    async def close(self):
        await super().close()

    async def setup_hook(self) -> None:
        await self.application_info()

    async def on_ready(self):
        await self.reload_cogs()
        print(f"{self.user.name} Is Active")

    async def reload_cogs(self):
        reload_message = {}
        error_message = None
        loaded_cogs = client.extensions
        self.config = YamlFile("config/config.yml")
        for cog in list(loaded_cogs):
            await client.unload_extension(cog)
        for file in Path("cogs").glob("**/*.py"):
            *tree, _ = file.parts
            reload_message.setdefault(tree[-1].capitalize(), [])
            try:
                await self.load_extension(f"{'.'.join(tree)}.{file.stem}")
                reload_message[tree[-1].capitalize()].append(
                    f"✅ {file.stem.capitalize()}"
                )
            except discord.ext.commands.errors.NoEntryPointError:
                reload_message[tree[-1].capitalize()].append(
                    f"✅ {file.stem.capitalize()}"
                )
            except Exception as e:
                reload_message[tree[-1].capitalize()].append(
                    f"❌ {file.stem.capitalize()}"
                )
                error_message = f"Ignoring exception in cog {file.stem}:\n{e}"
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

        language = self.config["Locale"].lower().capitalize()
        self.locale = Locale(language)
        return reload_message, error_message


client = ModuleCord()


@client.check
def block_dm_for_members(context):
    async def predicate(ctx) -> bool:
        if not await ctx.bot.is_owner(ctx.author):
            return ctx.guild
        return True

    return client.check(predicate)


if __name__ == "__main__":
    client.run(client.config["Token"])
