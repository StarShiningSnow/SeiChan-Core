import io

import discord
from PIL import Image, ImageDraw, ImageFont

lines = {
    "BR 棕線": "#C48C31",
    "R 紅線": "#E3002C",
    "PK 粉線": "#FD92A3",
    "G 綠線": "#008659",
    "O 橘線": "#F8B61C",
    "BL 藍線": "#0070BD",
    "Y 黃線": "#FFDB00",
    "LG 淺綠線": "#A1D884",
    "M 洋紅線": "#E60080",
    "LB 淺藍線": "#79BCE8",
    "C 青線": "#00FFFF",
    "P 紫線": "#8246AF",
}


def setup(tree):
    @tree.command(description="地下鉄の路線図を描く")
    @discord.app_commands.choices(
        line=[discord.app_commands.Choice(name=line, value=line) for line in lines]
    )
    async def line(interaction, line: str, stations: str):
        stations_list = stations.split()
        color = lines[line]

        width = 220 * (len(stations_list) - 1) + 120
        height = 220

        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 25)

        y = 100
        draw.line((60, y, 60 + 220 * (len(stations_list) - 1), y), fill=color, width=20)

        for i, station in enumerate(stations_list):
            x = 60 + 220 * i
            if i in (0, len(stations_list) - 1):
                draw.ellipse(
                    (x - 25, y - 25, x + 25, y + 25),
                    fill=color,
                    outline=color,
                    width=10,
                )
            else:
                draw.ellipse(
                    (x - 15, y - 15, x + 15, y + 15),
                    fill="white",
                    outline=color,
                    width=8,
                )
            draw.text((x, y + 40), station, fill="black", font=font, anchor="ma")

        buffer = io.BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)

        await interaction.response.send_message(file=discord.File(buffer, "line.png"))
