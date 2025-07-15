import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandSyncFlags
import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("TOKEN")

intents = disnake.Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True
)

sync_flags = CommandSyncFlags.default()
bot = commands.InteractionBot(intents=intents)



@bot.event
async def on_ready():
    print(f"{bot.user} HAS BEEN STARTED")


def load_cogs():
    for dirpath, _, filenames in os.walk("./cogs"):
        if "__pycache__" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_path = os.path.relpath(os.path.join(dirpath, filename), start=".").replace(os.sep, ".")[:-3]

                if cog_path in bot.cogs:
                    print(f"⚠️ {cog_path} ALREADY HAS LOADED")
                    continue
                try:
                    bot.load_extension(cog_path)
                    print(f"✅ {cog_path} HAS BEEN LOADED")
                except Exception as e:
                    print(f"❌ ERROR IN {cog_path}: {e}")


if __name__ == "__main__":
    load_cogs()
    bot.run(TOKEN)
