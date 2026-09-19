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
                *(get(x, z) for x in range(-2, 3) for z in range(-2, 3))
            )

        output = Image.new("RGBA", (2505, 2505))

        for x, z, data in tiles:
            img = Image.open(io.BytesIO(data))
            output.paste(img.crop((0, 0, 501, 501)), ((x + 2) * 501, (z + 2) * 501))

        buffer = io.BytesIO()
        output.save(buffer, "PNG")
        buffer.seek(0)

        embed = discord.Embed(
            title="🗺️ 帝国領土全域図",
            color=discord.Color.pink(),
            url=f"http://{WAN_IP}:8100",
        )
        embed.set_image(url="attachment://map.png")
        embed.set_footer(text="⚙️ • 連邦省情報局")

        await interaction.followup.send(
            file=discord.File(buffer, "map.png"), embed=embed
        )
