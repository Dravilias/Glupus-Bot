import discord
from discord.ext import commands
import database
import tracker
import config

# permisions
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# prefix
bot = commands.Bot(command_prefix="!", intents = intents)

# on ready
@bot.event
async def on_ready():
    database.setup()
    print(f"[BOT] online as {bot.user}")

# on message
@bot.event
async def on_message(message):
    # ignoring bot messages
    if message.author.bot:
        return
    
    tracker.checkMessage(message)

    await bot.process_commands(message)

# command handling
@bot.command(name="glups")
async def stats(ctx):
    rows = database.get_all_counts()

    embed = discord.Embed(
        title=f"{config.GLUP_EMOJI} Glups",
        color=discord.Color.blurple()
    )

    for item, count in rows:
        embed.add_field(
            name=item.replace("_", " ").title(),
            value=f"**{count}** razy",
            inline=False
    )
        
    await ctx.send(embed=embed) 