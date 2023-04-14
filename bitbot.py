import os
from datetime import datetime
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

def create_log():
    title = datetime.now().isoformat()
    path = f'Logs/{title}'
    log = open(path, 'w')
    log.write('{"role": "system", "content": "You are a chatbot running in a discord server. Your name is bb which is short for BitBot."}\n')
    log.close()
    return path

def assistant_append_log(content, path):
    log = open(path, 'a')
    log.write('{"role": "assistant", "content": ' + content + '}\n')
    log.close()

def user_append_log(content, path):
    log = open(path, 'a')
    log.write('{"role": "user", "content": ' + content + '}\n')
    log.close()
    return

def user_message(content):
    message = {
        "role":"user",
        "content":content
    }
    return message

def assistant_message(content):
    message = {
        "role":"assistant",
        "content":content
    }
    return message

async def bb_command(content):
    if (len(content) < 2):
        return "It appears you didn't include any commands."
    elif (content[:2] == '-h'):
        return "Available commands: \n -h For assistance using bb use this command to see a list of available commands. \n -i Generates an image based on the user provided prompt."
    elif (content[:2] == '-i'):
        return await generate_image(content[2:])
    else:
        return await contact_gpt(content)

async def contact_gpt(content):
    #Append content to log
    usermsg = user_message(content)
    user_append_log(content, logpath)
    messages.append(usermsg)
    #Pass message content to openai API
    completion = openai.ChatCompletion.create(
        model=currmodel,
        messages=messages
    )
    #Append assistant message to log
    assistantmsg = assistant_message(completion.choices[0].message.content)
    assistant_append_log(completion.choices[0].message.content, logpath)
    messages.append(assistantmsg)
    totaltk = completion.usage.total_tokens
    print(f'Total tokens used: {totaltk}')
    return completion.choices[0].message.content

async def generate_image(user_prompt):
    #Pass prompt content to openai API
    completion = openai.Image.create(
        prompt=user_prompt,
        n=1,
        size="1024x1024"
    )
    return completion.data[0].url

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds)
    print(f'Bitbot is connected to {guild}')
    global logpath
    global messages
    messages = [
        {
            "role": "system", 
            "content": "You are a chatbot running in a discord server. Your name is bb which is short for BitBot."
        }
    ]
    logpath = create_log()
    print(f'New chat log created: {logpath}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('bb!'):
        print(f'{datetime.now()} -- User:{message.author} invoked bitbot command -- {message.content}')
        response = await bb_command(message.content[4:])
        await message.channel.send(response)

client.run(discord_token)
#logpath = create_log()
#append_log('Test', logpath)