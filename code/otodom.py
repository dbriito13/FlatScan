import requests
import telegram
from bs4 import BeautifulSoup
from telegram import InputMediaPhoto

from objects.OtodomFlat import OtodomFlat


def otodom_processing():
    print("Empty method")


TELEGRAM_TOKEN = "7190088816:AAF3_gFThTcMQOR5x64gxYIJ2CFNilev8ts"
TELEGRAM_CHAT_ID = "-1002012368199"

URLS = [
    "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/wiele-lokalizacji?distanceRadius=0&limit=10&locations=%5Bmazowieckie%2Fwarszawa%2Fwarszawa%2Fwarszawa%2Fmokotow%2Fwygledow%2Cmazowieckie%2Fwarszawa%2Fwarszawa%2Fwarszawa%2Fmokotow%2Fsluzewiec%5D&daysSinceCreated=1&by=DEFAULT&direction=DESC&viewType=listing&mapBounds=52.19724060316587%3B21.020591622073546%3B52.17713033916398%3B20.959394660101534"
]


async def send_msg(flat: OtodomFlat):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    media_group = []
    for num in range(len(flat.pic_urls)):
        media_group.append(
            InputMediaPhoto(flat.pic_urls[num], caption=str(flat) if num == 0 else "")
        )
    await bot.send_media_group(chat_id=TELEGRAM_CHAT_ID, media=media_group)


def fetch_latest():
    for url in URLS:
        # Send a GET request to the URL
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }

        response = requests.get(url, headers=headers)
        flats = []

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, "html.parser")
            title_element = soup.find("span", text="Wszystkie ogłoszenia")
            ul_element = title_element.find_next_sibling("ul")
            if ul_element:
                # Find all <li> elements under the current <ul> element
                li_elements = ul_element.find_all("li")
                for li in [li_elements[0]]:
                    otodomFlat = OtodomFlat(li.find("article"))
                    print(otodomFlat)
                    flats.append(otodomFlat)

        else:
            # If the request was not successful, print an error message
            print(
                "Error: Unable to fetch HTML content, error code:", response.status_code
            )

            return None
    return flats[0]
