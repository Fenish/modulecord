import sys
import discord
import importlib
import traceback

from pathlib import Path
from aioconsole import ainput
from discord.ext import commands
from cogs.utils.yamlhandler import YamlFile


class ModuleCord(commands.Bot):
    async def sync_commands(self) -> None:
        pass

    def __init__(self):
        super().__init__(intents=discord.Intents.all(),
                         case_insensitive=True,
                         command_prefix="m!")
        self.config = YamlFile("config/config.yml")
        self.locale = YamlFile(f"locales/{self.config['Locale'].lower()}.yml")
        self.repository = "https://api.github.com/repos/Fenish/modulecord-modules/contents/modules"

    async def close(self):
        await super().close()

    async def on_ready(self):
        await self.reload_cogs()
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

        await self.change_presence(activity=discord.Activity(
            type=act_type,
            name=name
        ), status=status)
        print(f"{self.user.name} Is Active")
        # await console()

    async def reload_cogs(self):
        loaded_cogs = client.extensions
        for cog in list(loaded_cogs):
            await client.unload_extension(cog)
        for file in Path('cogs').glob('**/*.py'):
            *tree, _ = file.parts
            try:
                await self.load_extension(f"{'.'.join(tree)}.{file.stem}")
            except discord.ext.commands.errors.NoEntryPointError:
                pass
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


client = ModuleCord()


@client.check
def block_dm(ctx):
    return ctx.guild


async def console():
    command = str(await ainput("> ")).strip()
    if command == "stop":
        return await client.close()
    elif command == "reload":
        print("[+] Reloading...")
        await client.reload_cogs()
        print("[+] Reload Complete.")
    elif command == "guilds":
        guilds = [g.name for g in client.guilds]
        print("====== # Guilds\n")
        print("\n".join(guilds))
    elif command == "options":
        print("====== # Options\n")
        for key in client.config:
            print(f"{key} = {client.config[key]}")
    await console()


if __name__ == "__main__":
    client.run(client.config["Token"])
