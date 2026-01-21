import discord
import os
from utils.data import dbase
from utils.local_llm import LocalLLMClient
from utils.nephy_ai import Nephy  # your new local AI persona class

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
PATH = os.path.dirname(THIS_PATH)


class SetupChat:
    def __init__(self, bot, user_id, chat_name):
        self.bot = bot
        self.user_id = user_id
        self.chat_name = chat_name

        # Load config from bot
        self.config = bot.config if hasattr(bot, "config") else {}

        # Initialize Nephy (local model)
        self.nephy = Nephy(self.config)


    async def setup(
        self,
        message: discord.Message,
        msg: str = "hey",
        thread: bool = False,
        ping: bool = False,
        channel: discord.abc.Messageable = None
    ):

        # Check if user exists in DB
        check_id = await dbase(user_id=self.user_id, chat_name=self.chat_name).getUserID
        resume = True if check_id else False

        # Old model selection logic (ignored now)
        # We always use local model
        model = "local"

        if not resume:
            # Create metadata for new user/chat
            await dbase(self.user_id, self.chat_name).appendUserMetadata()
            await dbase(self.user_id, self.chat_name).appendSettings()
            await dbase(self.user_id, self.chat_name).appendPrivateSettings()
            await dbase(self.user_id, self.chat_name).appendChatMetadata(
                message, message.channel.id
            )

        return await self.chat(
            model=model,
            userInput=msg,
            ping=ping,
            channel=channel,
            message=message
        )


    async def chat(self, model, userInput, ping, message, channel):
        # Ping mode (bot was mentioned)
        if ping:
            # You can customize this if you want special behavior
            reply = self.nephy.generate_response(userInput)
            return reply

        # Normal chat
        reply = self.nephy.generate_response(userInput)
        return reply

