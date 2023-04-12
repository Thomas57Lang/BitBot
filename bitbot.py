import os
import discord
from dotenv import load_dotenv
import openai

load_dotenv()
discord_token = os.getenv('DISCORD')
openai.api_key = os.getenv('OPEN_AI')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
currmodel = 'gpt-3.5-turbo'

async def contact_gpt(content):
    #Pass message content to openai API
    completion = openai.ChatCompletion.create(
        model=currmodel, 
        messages=[
            {"role": "system", "content": "You are a chatbot running in a discord server."},
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message.content


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds)
    print(f'Bitbot is connected to {guild}')
    
@client.event
async def on_message(message):
    #print(f'Message detected - {message.content}')
    if message.author == client.user:
        return
    if message.content.startswith('bb!'):
        print('User invoked bitbot command')
        response = await contact_gpt(message.content)
        await message.channel.send(response)

client.run(discord_token)