import discord
from discord.ext import commands
from player import Player
from game_logic import Gamelogic, Round, Turn, Play
import secret

intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot(intents=intents, command_prefix="!")




if __name__ == "__main__":
    pass

    # bot.run(secret.BOT_TOKEN)