import io,discord,line,deep_translator,asyncio
from PIL import Image,ImageDraw,ImageFont

async def translate(text):
    return await asyncio.gather(*(asyncio.to_thread(deep_translator.MyMemoryTranslator(source="zh-TW",target=lang).translate,text) for lang in ("en-GB","ja-JP","ko-KR")))

def setup(tree):
    @tree.command()
    @discord.app_commands.choices(color=[discord.app_commands.Choice(name=n,value=c) for n,c in line.lines.items()])
    async def sign(interaction,color:str,number:str,station:str):
        await interaction.response.defer()
        en,jp,kr = await translate(station)
        route_font,station_font,multi_font = [ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf",size) for size in (120,100,45)]
        route = next(n.split()[0] for n,c in line.lines.items() if c==color)
        kr_x = 400+int(multi_font.getlength(jp))+60
        width = int(max(400+station_font.getlength(station),400+multi_font.getlength(en),kr_x+multi_font.getlength(kr))+60)
        img = Image.new("RGB",(width,800),color)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((60,230,330,570),radius=40,outline="white",width=20)
        for text,pos,font in [
            (route,(195,340),route_font),(number,(195,460),route_font),
            (station,(400,300),station_font),(en,(400,400),multi_font),
            (jp,(400,500),multi_font),(kr,(kr_x,500),multi_font)
        ]: draw.text(pos,text,font=font,fill="white",anchor="mm" if pos[0]==195 else "lm",stroke_width=1,stroke_fill="white")
        output = io.BytesIO()
        img.save(output,"PNG")
        output.seek(0)
        await interaction.followup.send(file=discord.File(output,"sign.png"))