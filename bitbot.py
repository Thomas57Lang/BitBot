import os
import discord
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv('DISCORD')
gpt_token = os.getenv('OPEN_AI')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(discord_token)