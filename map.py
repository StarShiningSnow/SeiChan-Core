import io,os,discord,aiohttp
from PIL import Image

async def draw_map():
    img = Image.new("RGB",(4509,2505))
    async with aiohttp.ClientSession() as session:
        for x,z in ((x,z) for x in range(-8,1) for z in range(-5,0)):
            async with session.get(f"http://{os.getenv('LAN_IP')}:8100/maps/world/tiles/1/x{x}/z{z}.png") as r:
                img.paste(Image.open(io.BytesIO(await r.read())).crop((0,0,501,501)),((x+8)*501,(z+5)*501))
    return img

def setup(tree):
    @tree.command()
    async def map(interaction):
        await interaction.response.defer()
        img = await draw_map()
        output = io.BytesIO()
        img.save(output,"PNG")
        output.seek(0)
        await interaction.followup.send(file=discord.File(output,"map.png"))