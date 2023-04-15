from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.weather_tok = os.getenv('WEATHER')
        self.bot = bot
        self.baseurl = 'http://api.weatherapi.com/v1'

    async def curr_weather(self, zip):
        current_url = self.baseurl + f'/current.json?q={zip}&key={self.weather_tok}'
        response = await requests.get(current_url)
        return response
    
    @commands.command()
    async def current_weather(self, ctx):
        return await self.curr_weather(ctx.message)
        
async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
