import io,discord,route
from PIL import Image,ImageDraw,ImageFont

def setup(tree):
    @tree.command()
    async def topo(interaction):
        stations = await route.get_stations()
        img = Image.new("RGB",(2505,2505),"white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf",25)
        edges = {}
        station_lines = {}
        for train in route.trains.values():
            sequence = []
            for x,z in train["path"]:
                station = min(stations,key=lambda n: (stations[n][0]-x)**2+(stations[n][1]-z)**2)
                sx,sz = stations[station]
                if (sx-x)**2+(sz-z)**2>40**2: continue
                if sequence and sequence[-1] == station: continue
                sequence.append(station)
                station_lines.setdefault(station,set()).add(train["name"])
            for a,b in zip(sequence,sequence[1:]):
                edge = tuple(sorted((a,b)))
                edges.setdefault(edge,set()).add(train["name"])
        points = dict(stations)
        for _ in range(3):
            for a,b in edges:
                x1,z1 = points[a]
                x2,z2 = points[b]
                dx,dz = x2-x1,z2-z1
                if abs(dx)>abs(dz)*2: points[b] = (x2,z1)
                elif abs(dz)>abs(dx)*2: points[b] = (x1,z2)
        for (a,b),lines in edges.items():
            x1,z1 = points[a]
            x2,z2 = points[b]
            dx,dz = x2-x1,z2-z1
            lines = sorted(lines)
            length = max((dx**2+dz**2)**0.5,1)
            for i,line in enumerate(lines):
                shift = (i-(len(lines)-1)/2)*20
                ox,oz = -dz/length*shift,dx/length*shift
                draw.line((x1+3000+ox,z1+2500+oz,x2+3000+ox,z2+2500+oz),fill=route.lines[line],width=20)
        ends = {station for edge in edges for station in edge if sum(station in e for e in edges) == 1}
        for name,(x,z) in points.items():
            lines = station_lines.get(name,set())
            color = route.lines[next(iter(lines))] if len(lines) == 1 else "black"
            fill = color if name in ends and len(lines) == 1 else "white"
            if len(lines)>1:
                for r,fill in ((20,"black"),(13,"white"),(7,"black")):
                    draw.ellipse((x+3000-r,z+2500-r,x+3000+r,z+2500+r),fill=fill)
            else: draw.ellipse((x+3000-20,z+2500-20,x+3000+20,z+2500+20),fill=fill,outline=color,width=10)
            draw.text((x+3000+30,z+2500-30),name,fill="black",font=font)
        output = io.BytesIO()
        img.save(output,"PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(output,"topo.png"))