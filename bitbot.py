import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from gtts import gTTS

class BitBot(commands.Bot):

    async def text_to_speech(self, content):
        voice = self.voice_clients[0]
        tts = gTTS(content)
        tts.save('hello.mp3')
        print('Attempting to talk in voice channel')
        voice.play(discord.FFmpegPCMAudio('hello.mp3'))

    async def bb_command(self, content):
        if (len(content) < 2):
            return "It appears you didn't include any commands."
        elif (content[:2] == '-h'):
            return "Available commands: \n -h For assistance using bb use this command to see a list of available commands. \n -i Generates an image based on the user provided prompt."
        elif (content[:2] == '-i'):
            return await self.get_cog("GPTCog").generate_image(content[2:])
        elif (content[:4] == 'join'):
            return "Attempting to join voice channel."
        elif (content[:5] == 'leave'):
            return "Attempting to leave voice channel."
        else:
            response = await self.get_cog("GPTCog").contact_gpt(content, 'user')
            if (len(self.voice_clients) > 0):
                await self.text_to_speech(response)
            return response

    async def ready(self):
        await self.load_extension("logcog")
        await self.load_extension("gptcog")
        await self.load_extension("weathercog")
        print(f'{self.user} has connected to Discord!')
        guild = discord.utils.get(self.guilds)
        print(f'Bitbot is connected to {guild}')

load_dotenv()
discord_token = os.getenv('DISCORD')
intents = discord.Intents.default()
intents.message_content = True
bb = BitBot(command_prefix='bb! ', intents=intents, case_insensitive=True)

@bb.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    voice = await channel.connect()


@bb.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# @bb.command()
# async def talk(ctx):
#     voice = ctx.message.guild.voice_client
#     tts = gTTS('hello I am bb. How can I help?')
#     tts.save('hello.mp3')
#     voice.play(discord.FFmpegPCMAudio('hello.mp3'))

@bb.event
async def on_ready():
    await bb.ready()
    
@bb.event
async def on_message(message):
    if message.author == bb.user:
        return
    if message.content.startswith('bb!'):
        print(f'{datetime.now()} -- User:{message.author} invoked bitbot command -- {message.content}')
        await bb.process_commands(message)
        response = await bb.bb_command(message.content[4:])
        await message.channel.send(response)

bb.run(discord_token)