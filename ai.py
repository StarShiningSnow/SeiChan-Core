import os

from google import genai

client = genai.Client(api_key=os.environ["AI_TOKEN"])


def setup(tree):
    @tree.command(
        description="連邦省情報官・星輝醬へ謁見し、雑談や政務の相談を行います"
    )
    async def ai(interaction, message: str):
        await interaction.response.defer()

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite", contents=message
        )

        await interaction.followup.send(response.text)
