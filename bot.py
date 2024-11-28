import discord
import os
from canWin import canWin
from pathlib import Path
from dotenv import load_dotenv

current_dir = Path(__file__).resolve(
).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

discordToken = os.getenv("TOKEN")


def run_discord_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} bot is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user_message = str(message.content)

        if user_message[0] == "!":
            user_message = user_message[1:]

            if user_message == "help":
                await message.channel.send(embed=help_embed)

            if user_message == "canwin":
                user_message = user_message[7:]
                summonerName = user_message
                await message.channel.send(embed=can_win)

            if user_message == "stats":
                await message.channel.send(embed=stats_embed)

    client.run(discordToken)


# !help EMBED COMMAND ----------------------------------------------------------------------------------------
help_embed = discord.Embed(title="Help",
                           colour=discord.Colour.green())
help_embed.add_field(
    name="!help", value="Displays all commands", inline=False)
help_embed.add_field(name="!canwin (summoner)",
                     value="Determines which team is more likely to win", inline=False)
help_embed.add_field(name="!stats (summoner)",
                     value="Shows accumulated team points for each team", inline=False)
help_embed.set_footer(
    text="https://github.com/bnjamkn/LoLGameDiscordBotPredictor")

# !canwin EMBED COMMAND ----------------------------------------------------------------------------------------
can_win = discord.Embed(title="You are likely to {status}".format(status="win"),
                        colour=discord.Colour.orange())
can_win.add_field(name="Red team's competitive ability:",
                  value="{red_points}".format(red_points=10))
can_win.add_field(name="Blue team's competitive ability:",
                  value="{blue_points}".format(blue_points=20))

# !stats EMBED COMMAND ----------------------------------------------------------------------------------------
stats_embed = discord.Embed(title="You are likely to {status}".format(status="win"),
                            colour=discord.Colour.purple())
stats_embed.add_field(name="Red team's stats", value="WR: {redWR} \n KDA Points: {redKDA} \n Rank Points:  {redRank}".format(
    redWR="50%", redKDA="4.0", redRank="421 LP"))
stats_embed.add_field(name="Blue team's stats", value="WR: {blueWR} \n KDA Points: {blueKDA} \n Rank Points:  {blueRank}".format(
    blueWR="53%", blueKDA="2.3", blueRank="436 LP"))
