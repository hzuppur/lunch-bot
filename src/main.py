import configparser
import datetime
import os
from typing import Union, Literal

import discord
import pytz
import requests
from babel.dates import format_datetime
from bs4 import BeautifulSoup
from discord.ext import tasks

# Change working directory to current file to make sure config file paths are correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read configuration files
config = configparser.ConfigParser()
config.read("../config/application.ini", encoding="utf8")
config.read("../config/user.ini", encoding="utf8")

if "APPLICATION" not in config:
    raise ValueError("Invalid/missing application configuration")
if "USER" not in config:
    raise ValueError("Invalid/missing user configuration")

OFFERS_URL = config["APPLICATION"]["offers_base_url"] + config["USER"]["location_url"]

DEFAULT_EMOJI = config["APPLICATION"]["default_emoji"].split(",")
EMOJI = config["USER"]["emoji"].split(",") if "emoji" in config["USER"] else []
if len(EMOJI) < len(DEFAULT_EMOJI):
    EMOJI = EMOJI + DEFAULT_EMOJI[len(EMOJI):]

TIMEZONE = pytz.timezone(config["USER"]["discord_bot_timezone"]) if "discord_bot_timezone" in config["USER"] else datetime.timezone.utc
DISCORD = False
if "discord_bot_token" in config["USER"] and "discord_channel_id" in config["USER"]:
    DISCORD = True
    DISCORD_BOT_TOKEN = config["USER"]["discord_bot_token"]
    DISCORD_BOT_CHANNEL = int(config["USER"]["discord_channel_id"])


def get_time_utc() -> datetime.time:
    return (datetime.datetime.combine(datetime.date.today(), datetime.time(11, 40)) - TIMEZONE.utcoffset(datetime.datetime.now())).time()


def get_offers():
    html_doc = requests.get(OFFERS_URL).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    meal_locations = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["offerLayout"])
    location_offers = {}

    for location in meal_locations:
        name = location.find('h3').text.strip()
        offers = [i.text.strip() for i in
                  location.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["offer"])]
        location_offers[name] = offers

    return location_offers


def get_offers_string(formatting: Union[Literal["md"], Literal["discord"]] = "md"):
    selected_locations = config["USER"]["locations"].split(",")

    if len(selected_locations) > len(DEFAULT_EMOJI):
        raise ValueError(f"Maximum number of locations is f{len(DEFAULT_EMOJI)}, {len(selected_locations)} requested")

    today = format_datetime(datetime.datetime.today(), "d. MMMM", locale="et")
    offers_string = f"## Päevapakkumised {today}\n" if formatting == "md" else f"**Päevapakkumised {today}**\n"
    location_offers = get_offers()
    valid_emoji = []

    for i in range(len(selected_locations)):
        selected_location = selected_locations[i].strip()
        if len(location_offers[selected_location]):
            offers_string += f"### {EMOJI[i]} {selected_location}:\n" if formatting == "md" else f"\n{EMOJI[i]} ***{selected_location}***\n"
            for offer in location_offers[selected_location]:
                offer = offer.split('\n')[0]
                offers_string += f"* {offer}\n" if formatting == "md" else f"> {offer}\n"
            valid_emoji.append(EMOJI[i])
        else:
            offers_string += f"### {selected_location} - pakkumised puuduvad\n" if formatting == "md" else f"\n~~{selected_location}~~\n"

    if formatting == "md":
        return offers_string
    if formatting == "discord":
        return offers_string, valid_emoji


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lunchtime.start()

    async def on_ready(self):
        print(f"Logged in to discord as {self.user} (ID: {self.user.id})")

    @tasks.loop(time=get_time_utc())
    async def lunchtime(self):
        if datetime.datetime.now().weekday() > 4:
            print("Weekend, skipping")
            return

        print("Sending offers to channel")
        channel = self.get_channel(DISCORD_BOT_CHANNEL)
        offers, emoji = get_offers_string("discord")
        message = await channel.send(offers)
        for reaction in emoji:
            await message.add_reaction(reaction)

    @lunchtime.before_loop
    async def before_lunchtime(self):
        # Wait until the bot is logged in
        await self.wait_until_ready()


if __name__ == '__main__':

    if DISCORD:
        client = DiscordClient()
        client.run(DISCORD_BOT_TOKEN)
    else:
        meal_offers = get_offers_string()
        print(meal_offers)
