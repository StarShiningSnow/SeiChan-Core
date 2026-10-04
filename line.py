import io,discord
from PIL import Image,ImageDraw,ImageFont

lines = {
    "BR 棕線":"#C48C31","R 紅線":"#E3002C","PK 粉線":"#FD92A3","G 綠線":"#008659",
    "O 橘線":"#F8B61C","BL 藍線":"#0070BD","Y 黃線":"#FFDB00","LG 淺綠線":"#A1D884",
    "M 洋紅線":"#E60080","LB 淺藍線":"#79BCE8","C 青線":"#00FFFF","P 紫線":"#8246AF",
}

def setup(tree):
    @tree.command()
    @discord.app_commands.choices(line=[discord.app_commands.Choice(name=n,value=c) for n,c in lines.items()])
    async def line(interaction,line:str,stations:str):
        station = stations.split()
        width = 150*(len(station)-1)+150
        img = Image.new("RGB",(width,150),"white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf",25)
        draw.line((50,100,50+150*(len(station)-1),100),fill=line,width=20)
        for i,name in enumerate(station):
            x = 50+150*i
            if i in (0,len(station)-1):
                draw.ellipse((x-20,80,x+20,120),fill=line)
            else:
                draw.ellipse((x-15,85,x+15,115),fill="white",outline="black",width=5)
            draw.text((x,50),name,font=font,fill="black",anchor="mm")
        output = io.BytesIO()
        img.save(output,"PNG")
        output.seek(0)
        await interaction.response.send_message(file=discord.File(output,"line.png"))