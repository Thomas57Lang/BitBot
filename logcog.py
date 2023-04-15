from discord.ext import commands
from datetime import datetime

class LogCog(commands.Cog):    
    def __init__(self, bot):
        self.logpath = self.create_log()
        self.bot = bot

    def create_log(self):
        title = datetime.now().isoformat()
        logpath = f'Logs/{title}'
        log = open(logpath, 'w')
        log.write(f'{datetime.now()} --- Transcript Beginning ---')
        #log.write('{"role": "system", "content": "You are a chatbot running in a discord server. Your name is bb which is short for BitBot."}\n')
        log.close()
        print(f'New chat log created: {logpath}')
        return logpath

    def assistant_append_log(self, content):
        log = open(self.logpath, 'a')
        log.write('{"role": "assistant", "content": ' + content + '}\n')
        log.close()

    def user_append_log(self, content):
        log = open(self.logpath, 'a')
        log.write('{"role": "user", "content": ' + content + '}\n')
        log.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author != self.bot.user):
            self.user_append_log(message.content)
        else:
            self.assistant_append_log(message.content)

async def setup(bot):
    await bot.add_cog(LogCog(bot))
