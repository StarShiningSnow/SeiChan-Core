import os,dotenv,discord

dotenv.load_dotenv()

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()

client.run(os.environ["DC_TOKEN"])