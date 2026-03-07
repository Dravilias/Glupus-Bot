import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
import database
import tracker
import config

# bot perms
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# prefix
bot = commands.Bot(command_prefix="!", intents=intents)


# --- AUTO RESET ---
# launches every 24h to check if its the first
@tasks.loop(hours=24)
async def monthly_reset():
    if datetime.now().day == 1:
        database.reset_counts()
        print("[BOT] monthly counter reset")


@bot.event
async def on_ready():
    database.setup()
    monthly_reset.start()  # starts the auto reset loop
    print(f"[BOT] online as {bot.user}")


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
    rows = database.get_counts(["glup_emoji", "glup_gif", "glup_sticker"])
    # get_counts returns (item, count, total)
    counts = {item: count for item, count, total in rows}
    totals = {item: total for item, count, total in rows}

    embed = discord.Embed(
        title=f"{config.GLUP_EMOJI} Glup Stats",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Emote", value=f"**{counts.get('glup_emoji', 0)}** times", inline=False)
    embed.add_field(name="GIF", value=f"**{counts.get('glup_gif', 0)}** times", inline=False)
    embed.add_field(name="Sticker", value=f"**{counts.get('glup_sticker', 0)}** times", inline=False)

    # monthly sum
    monthly = counts.get('glup_emoji', 0) + counts.get('glup_gif', 0) + counts.get('glup_sticker', 0)
    embed.add_field(name="Monthly Glups", value=f"**{monthly}** times", inline=False)

    # total sum (never resets)
    all_time = totals.get('glup_emoji', 0) + totals.get('glup_gif', 0) + totals.get('glup_sticker', 0)
    embed.add_field(name="All Glups", value=f"**{all_time}** times", inline=False)

    await ctx.send(embed=embed)


# !steamhappy command
@bot.command(name="steamhappy")
async def steamhappy(ctx):
    rows = database.get_counts(["steamhappy_emoji", "steamhappy_gif"])
    counts = {item: count for item, count, total in rows}
    totals = {item: total for item, count, total in rows}

    embed = discord.Embed(
        title=f"{config.STEAMHAPPY_EMOJI} Steam Happy Stats",
        color=discord.Color.yellow()
    )
    embed.add_field(name="Emote", value=f"**{counts.get('steamhappy_emoji', 0)}** times", inline=False)
    embed.add_field(name="GIF", value=f"**{counts.get('steamhappy_gif', 0)}** times", inline=False)

    # monthly sum
    monthly = counts.get('steamhappy_emoji', 0) + counts.get('steamhappy_gif', 0)
    embed.add_field(name="Monthly Steam Happy", value=f"**{monthly}** times", inline=False)

    # total sum
    all_time = totals.get('steamhappy_emoji', 0) + totals.get('steamhappy_gif', 0)
    embed.add_field(name="All Steam Happy", value=f"**{all_time}** times", inline=False)

    await ctx.send(embed=embed)


# !reset (admin only)
@commands.has_permissions(administrator=True)
@bot.command(name="reset")
async def reset(ctx):
    database.reset_counts()
    await ctx.send("✅ Liczniki miesięczne zresetowane!")


print("launching bot...")
try:
    bot.run(config.BOT_TOKEN)
except Exception as e:
    print(f"BŁĄD: {e}")
    input()