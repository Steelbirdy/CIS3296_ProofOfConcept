import os

import discord
import dotenv
from discord import app_commands
from discord.ext import commands

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''


class MyBot(commands.Bot):
    async def setup_hook(self):
        # Get the ID of the testing server from the environment variable
        guild_id = os.getenv('BOT_GUILD')
        guild = discord.Object(id=int(guild_id))

        # Copy global slash commands to a testing server
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


bot = MyBot(command_prefix='?', description=description, intents=discord.Intents.default())


@bot.tree.command(name='exec')
@app_commands.describe(code='The python code to execute')
async def exec_(interaction: discord.Interaction, code: str):
    """Executes Python code"""

    # Remove any Markdown formatting
    code = code.strip('`')

    try:
        result = eval(code)
        content = f'Output: ```python\n{result}\n```'
    except Exception as error:
        content = f'Error: ```python\n{repr(error)}\n```'
    await interaction.response.send_message(content)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


if __name__ == '__main__':
    dotenv.load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    bot.run(token=bot_token)
