import os

import discord
import dotenv

import ai
import line
import map
import route

dotenv.load_dotenv()

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

map.setup(tree)
ai.setup(tree)
line.setup(tree)
route.setup(tree)


@client.event
async def on_ready():
    await tree.sync()
    route.start()


client.run(os.environ["DC_TOKEN"])
