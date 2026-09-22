import asyncio
import io
import json
import os

import aiohttp
import discord
from PIL import Image, ImageDraw, ImageFont

line_colors = {
    "南北線": "#E3002C",
    "央海線": "#79BCE8",
    "環山線": "#FD92A3",
    "英格蘭環線": "#FFDB00",
    "東環線": "#0070BD",
    "半島線": "#F8B61C",
    "東域線": "#008659",
}
train_tracks = {}
tracking = False
LAN_IP = os.environ["LAN_IP"]
WAN_IP = os.environ["WAN_IP"]


async def track_trains():
    async with (
        aiohttp.ClientSession() as session,
        session.get(f"http://{LAN_IP}:3876/api/trains.rt") as response,
    ):
        async for line in response.content:
            if line.startswith(b"data:"):
                for train in json.loads(line[5:])["trains"]:
                    name = train["name"].split(" ")[0]
                    if name.endswith("線"):
                        point = train["cars"][0]["leading"]["location"]
                        track = train_tracks.setdefault(
                            train["id"], {"name": name, "points": []}
                        )
                        track["points"].append((point["x"], point["z"]))


def start():
    global tracking
    if not tracking:
        tracking = True
        asyncio.create_task(track_trains())


async def render():
    async with (
        aiohttp.ClientSession() as session,
        session.get(f"http://{LAN_IP}:3876/api/network") as response,
    ):
        data = await response.json(content_type=None)
    stations = {}
    for s in data["stations"]:
        name = s["name"].split(" ")[0]
        if name.endswith("站"):
            stations.setdefault(name, []).append(s["location"])
    img = Image.new("RGB", (2505, 2505), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 20)
    for track in train_tracks.values():
        if track["name"] in line_colors:
            points = [(x + 1212.5, z + 912.5) for x, z in track["points"]]
            color = line_colors[track["name"]]
            draw.line(points, fill=color, width=8)
            x, y = points[-1]
            draw.ellipse(
                (x - 6, y - 6, x + 6, y + 6),
                fill="white",
                outline=color,
                width=3,
            )
    for name, locations in stations.items():
        x = sum(p["x"] for p in locations) / len(locations) + 1212.5
        y = sum(p["z"] for p in locations) / len(locations) + 912.5
        draw.ellipse(
            (x - 7, y - 7, x + 7, y + 7), fill="white", outline="black", width=3
        )
        box = draw.textbbox((x + 13, y - 26), name, font=font)
        draw.rectangle(box, fill="white")
        draw.text((x + 13, y - 26), name, fill="black", font=font)
    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    return buffer


class Refresh(discord.ui.View):
    @discord.ui.button(label="更新", style=discord.ButtonStyle.primary)
    async def refresh(self, interaction, button):
        await interaction.response.defer()
        await interaction.message.edit(
            attachments=[discord.File(await render(), "route.png")], view=self
        )


def setup(tree):
    @tree.command(description="地下鉄運行状況")
    async def route(interaction):
        embed = discord.Embed(
            title="地下鉄運行状況",
            color=discord.Color.blurple(),
            url=f"http://{WAN_IP}:3876",
        )
        embed.set_image(url="attachment://route.png")
        embed.set_footer(text="⚙️ • 連邦省情報局")
        await interaction.response.send_message(
            embed=embed, file=discord.File(await render(), "route.png"), view=Refresh()
        )
