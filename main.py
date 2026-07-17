import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WORKER = os.getenv("WORKER")
ADMIN = os.getenv("ADMIN")

ROLE_ID = 123456789012345678


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    await bot.tree.sync()

    print(
    "Bot online"
    )



@bot.tree.command(
name="getkey",
description="Get Axiom key"
)
async def getkey(
interaction:discord.Interaction
):


    allowed=False


    for role in interaction.user.roles:

        if role.id == ROLE_ID:

            allowed=True



    if not allowed:

        await interaction.response.send_message(
        "No access",
        ephemeral=True
        )

        return



    r=requests.post(

    WORKER,

    json={
    "action":"get"
    }

    )


    data=r.json()



    if data["success"]:


        await interaction.response.send_message(

        f"Your key:\n```{data['key']}```",

        ephemeral=True

        )


    else:

        await interaction.response.send_message(

        "No active key",

        ephemeral=True

        )





@bot.tree.command(
name="newkey"
)
async def newkey(
interaction:discord.Interaction
):


    r=requests.post(

    WORKER,

    json={

    "action":"create",

    "admin":ADMIN

    }

    )


    await interaction.response.send_message(

    r.text,

    ephemeral=True

    )



bot.run(TOKEN)
