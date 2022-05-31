import discord
from discord import ui
from discord.ext import menus


class PaginatorMenu(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        if self._source.get_max_pages() != 1:
            self.next_page.disabled = (
                self.current_page + 1 == self._source.get_max_pages()
            )
            self.page_number.label = (
                f"{self.current_page + 1}/{self._source.get_max_pages()}"
            )
        else:
            self.clear_items()
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if "view" not in value:
            value.update({"view": self})
        return value

    async def interaction_check(self, interaction):
        await interaction.response.defer()
        self.next_page.disabled = (
            self.current_page + 1 == self._source.get_max_pages() - 1
        )
        return interaction.user == self.ctx.author

    @ui.button(label="←", style=discord.ButtonStyle.blurple, disabled=True, row=2)
    async def before_page(self, button, interaction):
        self.page_number.label = f"{self.current_page}/{self._source.get_max_pages()}"
        self.before_page.disabled = "1/" in self.page_number.label
        await self.show_checked_page(self.current_page - 1)

    @ui.button(label="1/", style=discord.ButtonStyle.green, disabled=True, row=2)
    async def page_number(self, button, interaction):
        self.stop()

    @ui.button(label="→", style=discord.ButtonStyle.blurple, disabled=True, row=2)
    async def next_page(self, button, interaction):
        self.page_number.label = (
            f"{self.current_page + 2}/{self._source.get_max_pages()}"
        )
        self.before_page.disabled = "1/" in self.page_number.label
        await self.show_checked_page(self.current_page + 1)


class PaginatorSource(menus.ListPageSource):
    def __init__(self, embed, entries, *, per_page, base_text=""):
        super().__init__(entries=entries, per_page=per_page)
        self.embed = embed
        self.base_text = base_text

    async def format_page(self, menu, entries):
        embed = self.embed
        embed.description = self.base_text + "\n\n"
        embed.description += "\n".join([str(x) for x in entries])
        return embed
