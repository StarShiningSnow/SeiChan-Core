import io,discord,map,route
from PIL import Image

def setup(tree):
    @tree.command()
    async def hybrid(interaction):
        base = await map.draw_map()
        overlay = await route.draw_route()
        img = Image.blend(base,Image.new("RGB",base.size,"white"),0.5)
        img.paste(overlay,(0,0),overlay)
        output = io.BytesIO()
        img.save(output,"PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(output,"hybrid.png"))