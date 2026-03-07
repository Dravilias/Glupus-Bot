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
    # makes tracker check the contents
    tracker.checkMessage(message)
    # some bullshit that breaks it
    await bot.process_commands(message)

# !glups command
@bot.command(name="glups")
async def glups(ctx):
    # gets the rows for glup related stuff
    rows = database.get_counts(["glup_emoji", "glup_gif", "glup_sticker"])
    # does some bullshit i guess
    counts = dict(rows)
    # bullshit for embeds
    embed = discord.Embed(
        title=f"{config.GLUP_EMOJI} Glup Stats",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Emote", value=f"**{counts.get('glup_emoji', 0)}** times", inline=False)
    embed.add_field(name="GIF", value=f"**{counts.get('glup_gif', 0)}** times", inline=False)
    embed.add_field(name="Sticker", value=f"**{counts.get('glup_sticker', 0)}** times", inline=False)

    await ctx.send(embed=embed)

# !steamhappy

@bot.command(name="steamhappy")
async def steamhappy(ctx):
    # gets counts for steamhappy
    rows = database.get_counts(["steamhappy_emoji", "steamhappy_gif"])
    # does some bs
    counts = dict(rows)
    # bullshit for embed
    embed = discord.Embed(
        title=f"{config.STEAMHAPPY_EMOJI} Steam Happy Stats",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Emote", value=f"**{counts.get('steamhappy_emoji', 0)}** times", inline=False)
    embed.add_field(name="GIF", value=f"**{counts.get('steamhappy_gif', 0)}** times", inline=False)

    await ctx.send(embed=embed)

# !reset (admin only)

@commands.has_permissions(administrator=True)
@bot.command(name="reset")
async def reset(ctx):
    database.reset_counts()
    await ctx.send("✅ Liczniki zresetowane!")

print("lauching bot")


try:
    bot.run(config.BOT_TOKEN)
except Exception as e:
    print(f"BŁĄD: {e}")
    input()