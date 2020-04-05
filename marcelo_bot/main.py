from discord.ext import commands
from marcelo_bot.music import Music
import os


TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='~')

bot.add_cog(Music(bot))
bot.run(TOKEN)