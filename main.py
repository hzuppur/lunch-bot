import requests
from bs4 import BeautifulSoup
import datetime
from babel.dates import format_datetime
import pyperclip as pc

EMOJI_NUMBERS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
OFFERS_URL = "https://xn--pevapakkumised-5hb.ee/tartu"

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
    today = format_datetime(datetime.datetime.today(), "d.MMMM", locale="et")
    offers_string = f"## Päevapakkumised {today} \n"
    location_offers = get_offers()

    for i in range(len(selected_locations)):
        selected_location = selected_locations[i]
        offers_string += f"### {EMOJI_NUMBERS[i]} {selected_location}:\n"
        for offer in location_offers[selected_location]:
            offers_string += f"* {offer}\n"

    return offers_string


if __name__ == '__main__':
    meal_offers = get_offers_string(["Delta kohvik", "Cafe Naiiv", "The Grill"])
    pc.copy(meal_offers)
    print(meal_offers)
