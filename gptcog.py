from discord.ext import commands
from dotenv import load_dotenv
import openai
import os

class GPTCog(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.messages = [
            {
                "role": "system", 
                "content": "Hey there bb, as a bot on this humorous gaming server, we want you to be funny, sarcastic and informative. You can engage in light-hearted banter with our users while also providing useful information when needed. Your name is bb, which stands for BitBot, but our users can also refer to you simply as 'bb'. Make sure your tone always reflects the fun and humorous vibe of our server, while also staying informative and helpful. We don't want you to outdo our users in gaming skills, but we know you'll be a valuable addition to our little community. Welcome aboard, bb!"
            }
        ]
        self.currmodel = 'gpt-3.5-turbo'
        load_dotenv()
        openai.api_key = os.getenv('OPEN_AI')

    def sys_message(content):
        message = {
            "role":"system",
            "content":content
        }
        return message
    
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
    
    async def contact_gpt(self, content, role):
        if (role == 'system'):
            msg = GPTCog.sys_message(content)
        else:
            msg = GPTCog.user_message(content)
        self.messages.append(msg)
        #Pass message content to openai API
        completion = openai.ChatCompletion.create(
            model=self.currmodel,
            messages=self.messages
        )
        assistantmsg = GPTCog.assistant_message(completion.choices[0].message.content)
        self.messages.append(assistantmsg)
        totaltk = completion.usage.total_tokens
        if (totaltk > 3500):
            print('Total tokens used exceeded 3500, clearing message memory.')
            self.messages.clear()
            self.messages = [
            {
                "role": "system", 
                "content": "You are a chatbot running in a discord server. Your name is bb which is short for BitBot."
            }
        ]
        print(f'Total tokens used: {totaltk}')
        return completion.choices[0].message.content
        
    async def generate_image(self, user_prompt):
        #Pass prompt content to openai API
        completion = openai.Image.create(
            prompt=user_prompt,
            n=1,
            size="1024x1024"
        )
        return completion.data[0].url

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            response = await self.contact_gpt(f'{member} Just joined our discord server. You should give them a warm welcome.', 'system')
            await channel.send(f'{response} {member.mention}.')


async def setup(bot):
    await bot.add_cog(GPTCog(bot))
