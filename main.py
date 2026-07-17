import discord
from discord.ext import commands
import requests
import os


TOKEN = os.getenv("TOKEN")
WORKER = os.getenv("WORKER")
ADMIN = os.getenv("ADMIN")


# Role allowed to use /getkey
ALLOWED_ROLE_ID = 1527529264738603151


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Slash commands synced")


# ==========================
# GET KEY COMMAND
# ==========================

@bot.tree.command(
    name="getkey",
    description="Get the active Axiom key"
)
async def getkey(interaction: discord.Interaction):

    has_role = False

    for role in interaction.user.roles:
        if role.id == ALLOWED_ROLE_ID:
            has_role = True


    if not has_role:
        await interaction.response.send_message(
            "❌ You do not have permission to use this command.",
            ephemeral=True
        )
        return


    try:

        response = requests.post(
            WORKER,
            json={
                "action": "get"
            },
            timeout=10
        )


        data = response.json()


        if data.get("success"):

            await interaction.response.send_message(
                f"🔑 Your Axiom Key:\n\n```{data['key']}```\n\nExpires every 3 hours.",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ No active key currently.",
                ephemeral=True
            )


    except Exception as e:

        await interaction.response.send_message(
            f"❌ API Error:\n{e}",
            ephemeral=True
        )



# ==========================
# CREATE NEW KEY
# ==========================

@bot.tree.command(
    name="newkey",
    description="Generate a new Axiom key"
)
async def newkey(interaction: discord.Interaction):


    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "❌ Admin only.",
            ephemeral=True
        )

        return



    try:

        response = requests.post(
            WORKER,
            json={
                "action":"create",
                "admin":ADMIN
            },
            timeout=10
        )


        data=response.json()


        if data.get("success"):

            await interaction.response.send_message(
                f"✅ New Key Created:\n```{data['key']}```",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ Failed creating key.",
                ephemeral=True
            )


    except Exception as e:

        await interaction.response.send_message(
            f"❌ Error:\n{e}",
            ephemeral=True
        )



# ==========================
# START BOT
# ==========================

if not TOKEN:
    print("Missing TOKEN environment variable")
    exit()


bot.run(TOKEN)
