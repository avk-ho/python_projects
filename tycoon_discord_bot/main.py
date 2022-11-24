import discord
from discord.ext import commands
from game_logic import *
from player import *
import secret

game = Gamelogic()

intents = discord.Intents.default()
intents.message_content = True

# bot = commands.Bot(intents=intents, command_prefix="!")




# bot.run(secret.BOT_TOKEN)