import io,os,discord,aiohttp,json
from PIL import Image,ImageDraw,ImageFont

lines = {
    "貳環線":"#C48C31","南北線":"#E3002C","環山線":"#FD92A3","東域線":"#008659",
    "半島線":"#F8B61C","東環線":"#0070BD","英格蘭環線":"#FFDB00","LG 淺綠線":"#A1D884",
    "M 洋紅線":"#E60080","央海線":"#79BCE8","C 青線":"#00FFFF","P 紫線":"#8246AF",
}
trains = {}

async def record_train():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{os.getenv('LAN_IP')}:3876/api/trains.rt") as r:
            async for line in r.content:
                if line.startswith(b"data:"):
                    for train in json.loads(line[5:])["trains"]:
                        name = train["name"]
                        if "線" not in name: continue
                        name = name[:name.index("線")+1]
                        if name not in lines: continue
                        loc = train["cars"][0]["leading"]["location"]
                        trains.setdefault(train["id"],{"name":name,"path":[]})
                        trains[train["id"]]["path"].append((loc["x"],loc["z"]))

async def draw_route():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{os.getenv('LAN_IP')}:3876/api/network") as r:
            data = await r.json(content_type=None)
    img = Image.new("RGBA",(2505,2505),(255,255,255,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf",25)
    stations = {}
    for item in data["stations"]:
        name = item["name"]
        if "站" not in name: continue
        name = name[:name.index("站")+1]
        if name in stations: continue
        stations[name] = (item["location"]["x"],item["location"]["z"])
    for train in trains.values():
        points = [(x+3000,z+2500) for x,z in train["path"]]
        draw.line(points,fill=lines[train["name"]],width=20)
    for name,(x,z) in stations.items():
        draw.ellipse((x+3000-20,z+2500-20,x+3000+20,z+2500+20),fill="white",outline="black",width=10)
        draw.text((x+3000+30,z+2500-30),name,fill="black",font=font)
    return img

def setup(tree):
    @tree.command()
    async def route(interaction):
        img = await draw_route()
        bg = Image.new("RGB",img.size,"white")
        bg.paste(img,mask=img.getchannel("A"))
        output = io.BytesIO()
        bg.save(output,"PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(output,"route.png"))