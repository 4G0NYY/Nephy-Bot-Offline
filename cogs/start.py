import discord
from discord.ext import commands
from discord import app_commands
# from utils.data import data as db
import utils.data as db
from utils.data import Sanitizer
from better_profanity import profanity


class Start(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.sanitizer = Sanitizer()

    @app_commands.command(name="add_channel")
    @commands.is_owner()
    async def add_channel(self, interaction: discord.Interaction, channel_id: str):
        """Add a channel for novels to be initialized in."""

        if isinstance(interaction.channel, discord.Thread):
            return await interaction.response.send_message(
                content="**This cannot be done in a Thread!**"
            )

        channel = self.bot.get_channel(int(channel_id))
        if channel is None:
            return await interaction.response.send_message(
                content="This isn't a valid channel ID"
            )

        await db.dbase.appendChannel(interaction, int(channel_id))

        return await interaction.response.send_message(
            content="Channel added to list of available chats!"
        )


# ---------------------------------------------------------
# REQUIRED: Cog setup function
# ---------------------------------------------------------
async def setup(bot):
    await bot.add_cog(Start(bot))
