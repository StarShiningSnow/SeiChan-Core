import os,sys,asyncio

def setup(tree):
    @tree.command()
    async def restart(interaction):
        if interaction.user.id != int(os.getenv("ADMIN_ID")):
            return await interaction.response.send_message("omg u srsly tryin to access this without permission? failure! 😭 ur mom gonna whip u w/ the rattan chair ngl, pack ur bags rn u ain't got the power rip")
        await interaction.response.send_message("ok lor u got the power, happy now? 🙄 system restarting rn, ur screen gonna go black w/ the speed of light fr, don't scream ah! bro bffr just wait 10 seconds idc go drink some water smh")
        await asyncio.sleep(1)
        os.execv(sys.executable,[sys.executable,*sys.argv])