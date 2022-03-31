import configparser
import datetime
import os

import requests
from babel.dates import format_datetime
from bs4 import BeautifulSoup

# Change working directory to current file to make sure config file paths are correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read configuration files
config = configparser.ConfigParser()
config.read("../config/application.ini", encoding="utf8")
config.read("../config/user.ini", encoding="utf8")

if "APPLICATION" not in config:
    raise ValueError("Invalid application configuration")
if "USER" not in config:
    raise ValueError("Invalid user configuration")

OFFERS_URL = config["APPLICATION"]["offers_base_url"] + config["USER"]["location_url"]

DEFAULT_EMOJI = config["APPLICATION"]["default_emoji"].split(",")
EMOJI = config["USER"]["emoji"].split(",")
if len(EMOJI) < len(DEFAULT_EMOJI):
    EMOJI = EMOJI + DEFAULT_EMOJI[len(EMOJI):]


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


def get_offers_string(selected_locations):
    if len(selected_locations) > len(DEFAULT_EMOJI):
        raise ValueError(f"Maximum number of locations is f{len(DEFAULT_EMOJI)}, {len(selected_locations)} requested")

    today = format_datetime(datetime.datetime.today(), "d.MMMM", locale="et")
    offers_string = f"## Päevapakkumised {today} \n"
    location_offers = get_offers()

    for i in range(len(selected_locations)):
        selected_location = selected_locations[i]
        offers_string += f"### {EMOJI[i]} {selected_location}:\n"
        for offer in location_offers[selected_location]:
            offer = offer.split('\n')[0]
            offers_string += f"* {offer}\n"

    return offers_string


if __name__ == '__main__':
    meal_offers = get_offers_string(config["USER"]["locations"].split(","))
    print(meal_offers)
