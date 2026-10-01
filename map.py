import asyncio
import io
import os

import aiohttp
import discord
from PIL import Image

LAN_IP = os.environ["LAN_IP"]
WAN_IP = os.environ["WAN_IP"]


def setup(tree):
    @tree.command(description="連邦省情報局により最新の帝国領土測量図が更新されました")
    async def map(interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:

            async def get(x, z):
                url = f"http://{LAN_IP}:8100/maps/world/tiles/1/x{x}/z{z}.png"
                async with session.get(url) as r:
                    return x, z, await r.read()

            tiles = await asyncio.gather(
                *(get(x, z) for x in range(-6, -1) for z in range(-5, 0))
            )
        output = Image.new("RGBA", (2505, 2505))
        for x, z, data in tiles:
            img = Image.open(io.BytesIO(data))
            output.paste(img.crop((0, 0, 501, 501)), ((x + 6) * 501, (z + 5) * 501))
        buffer = io.BytesIO()
        output.save(buffer, "PNG")
        buffer.seek(0)
        await interaction.followup.send(file=discord.File(buffer, "map.png"))
