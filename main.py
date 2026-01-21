import discord
from discord.ext import commands
from utils import data as db
from utils import chat
import json
import os

PATH = os.path.dirname(os.path.realpath(__file__))

with open(f"{PATH}/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["BOT_TOKEN"]

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = True

COMMAND_PREFIX = "nr!"


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.PATH = PATH
        self.ongoing = {}
        self.config = config

    async def setup_hook(self):
        for filename in os.listdir(f"{PATH}/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await db.dbase.c_tables()

    async def on_ready(self):
        print(f"Nephy is online! Discord.py version: {discord.__version__}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        cleaned = message.content.replace(self.user.mention, self.user.name) if self.user else message.content

        reply = await chat.SetupChat(self, message.author.id, "<DM>").setup(message, cleaned)
        await message.channel.send(reply)

        await self.process_commands(message)


bot = Bot(
    command_prefix=COMMAND_PREFIX,
    intents=INTENTS,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
    owner_ids=[1119528660345573408],
)

bot.remove_command("help")


if __name__ == "__main__":
    bot.run(TOKEN)
