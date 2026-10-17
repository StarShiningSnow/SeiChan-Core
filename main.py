import discord,os,asyncio,dotenv,hybrid,line,map,route,topo,restart,sign

dotenv.load_dotenv()
client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

for m in (hybrid,line,map,route,topo,restart,sign):
    m.setup(tree)

@client.event
async def on_ready():
    asyncio.create_task(route.record_train())
    await tree.sync()

client.run(os.getenv("DC_TOKEN"))