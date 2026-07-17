import discord
from discord.ext import commands
import requests
import os


TOKEN = os.getenv("TOKEN")
WORKER = os.getenv("WORKER")
ADMIN = os.getenv("ADMIN")


# Roles
KEY_ROLE_ID = 1527529264738603151
OWNER_ROLE_ID = 1527529191698858125


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# READY
# =========================

@bot.event
async def on_ready():

    await bot.tree.sync()

    print("----------------------")
    print(f"Logged in as {bot.user}")
    print("Commands synced")
    print("----------------------")



# =========================
# GET CURRENT KEY
# =========================

@bot.tree.command(
    name="getkey",
    description="Get the current Axiom key"
)
async def getkey(interaction: discord.Interaction):


    # Check role
    has_role = any(
        role.id == KEY_ROLE_ID
        for role in interaction.user.roles
    )


    if not has_role:

        await interaction.response.send_message(
            "❌ You do not have permission to use this command.",
            ephemeral=True
        )

        return



    # Acknowledge interaction
    await interaction.response.defer(
        ephemeral=True
    )


    try:

        response = requests.post(
            WORKER,
            json={
                "action":"get"
            },
            timeout=10
        )


        data = response.json()



        if data.get("success"):


            await interaction.followup.send(
                f"🔑 **Axiom Key**\n\n```{data['key']}```\n\n⏳ Expires every 3 hours.",
                ephemeral=True
            )


        else:


            await interaction.followup.send(
                "❌ No active key.",
                ephemeral=True
            )



    except Exception as e:


        await interaction.followup.send(
            f"❌ Error contacting API:\n```{e}```",
            ephemeral=True
        )





# =========================
# CREATE NEW KEY
# =========================

@bot.tree.command(
    name="newkey",
    description="Create a new Axiom key"
)
async def newkey(interaction: discord.Interaction):


    # Owner role check
    has_owner_role = any(
        role.id == OWNER_ROLE_ID
        for role in interaction.user.roles
    )


    if not has_owner_role:


        await interaction.response.send_message(
            "❌ Only the owner can create new keys.",
            ephemeral=True
        )


        return



    await interaction.response.defer(
        ephemeral=True
    )



    try:


        response = requests.post(

            WORKER,

            json={

                "action":"create",

                "admin":ADMIN

            },

            timeout=10

        )



        data = response.json()



        if data.get("success"):


            await interaction.followup.send(

                f"✅ **New Axiom Key Created**\n\n```{data['key']}```\n\nExpires in 3 hours.",

                ephemeral=True

            )



        else:


            await interaction.followup.send(

                "❌ Failed creating key.",

                ephemeral=True

            )



    except Exception as e:


        await interaction.followup.send(

            f"❌ Error:\n```{e}```",

            ephemeral=True

        )





# =========================
# START
# =========================

if not TOKEN:

    print("Missing TOKEN environment variable")

    exit()



if not WORKER:

    print("Missing WORKER environment variable")

    exit()



if not ADMIN:

    print("Missing ADMIN environment variable")

    exit()



bot.run(TOKEN)
