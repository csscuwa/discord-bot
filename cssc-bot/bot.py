import discord
from discord.ext import commands

import dotenv
import os

dotenv.load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="the CSSC Door"))
    await bot.load_extension('cogs.door')

@bot.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.news:
        await message.publish()
        return

bot.run(token)