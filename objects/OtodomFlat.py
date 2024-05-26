import re


class OtodomFlat:
    def __separate_price(self, price_span):
        # Separate by + (ex: 9450 zł+ czynsz: 1700 zł/miesiąc)
        numbers = re.findall(r"\b\d+\b", price_span)
        numbers = [int(number) for number in numbers]
        if len(numbers) > 1:
            return (numbers[0], numbers[1])
        return (numbers[0], None)

    def __init__(self, article_data) -> None:
        # Extract Flat Offer data from article_data
        self.url = "https://www.otodom.pl" + article_data.find("a")["href"]

        # Get Price for listing
        price_div = article_data.find(
            "div", attrs={"data-testid": "listing-item-header"}
        )
        if price_div:
            # print(price_div.prettify())
            price_font = price_div.find("span").text
            self.rent, self.czynsz = self.__separate_price(price_font)

        # Get Address
        address_p = article_data.find(
            "p", attrs={"data-testid": "advert-card-address"}
        ).text
        if address_p:
            self.street, self.neighbourhood = [
                part.strip() for part in address_p.split(",")
            ][0:2]

        # Get Flat Info (number of rooms, floor, sq meters)
        flat_info_div = article_data.find(
            "div", attrs={"data-testid": "advert-card-specs-list"}
        )
        self.rooms, self.meters, self.floor = [
            re.sub(r"\D", "", info.text) for info in flat_info_div.find_all("dd")
        ]

        # Is it a private offer?
        private = article_data.find(
            "div", attrs={"data-testid": "listing-item-owner-name"}
        )
        self.private = False if private else True

        # Get a maximum of 5 images from the offer to include in message
        pic_carousel = article_data.find(
            "div", attrs={"data-testid": "carousel-container"}
        )
        if pic_carousel:
            self.pic_urls = [pic["src"] for pic in pic_carousel.find_all("img")]
            print(f"Found {len(self.pic_urls)} pictures for this flat")
        self.id = "1234"

    def __str__(self) -> str:
        return (
            f"Otodom Flat - {self.id}. Price: {self.rent} + Czynsz: {self.czynsz} at: {self.street}, {self.neighbourhood}.\n"
            + f"Has {self.rooms} rooms, {self.meters}m2 and is on floor {self.floor} with URL: {self.url}."
            + f"Private: {self.private}"
        )
