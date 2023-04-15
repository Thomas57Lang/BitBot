import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

class BitBot(commands.Bot):

    async def bb_command(self, content):
        if (len(content) < 2):
            return "It appears you didn't include any commands."
        elif (content[:2] == '-h'):
            return "Available commands: \n -h For assistance using bb use this command to see a list of available commands. \n -i Generates an image based on the user provided prompt."
        elif (content[:2] == '-i'):
            return await self.get_cog("GPTCog").generate_image(content[2:])
        else:
            return await self.get_cog("GPTCog").contact_gpt(content, 'user')

    async def ready(self):
        await self.load_extension("logcog")
        await self.load_extension("gptcog")
        print(f'{self.user} has connected to Discord!')
        guild = discord.utils.get(self.guilds)
        print(f'Bitbot is connected to {guild}')

load_dotenv()
discord_token = os.getenv('DISCORD')
intents = discord.Intents.default()
intents.message_content = True
bb = BitBot(command_prefix='bb! ', intents=intents, case_insensitive=True)

@bb.event
async def on_ready():
    await bb.ready()
    
@bb.event
async def on_message(message):
    if message.author == bb.user:
        return
    if message.content.startswith('bb!'):
        print(f'{datetime.now()} -- User:{message.author} invoked bitbot command -- {message.content}')
        response = await bb.bb_command(message.content[4:])
        await message.channel.send(response)

bb.run(discord_token)