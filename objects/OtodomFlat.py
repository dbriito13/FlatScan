import re


class OtodomFlat:
    def __separate_price(self, price_span):
        # Separate by + (ex: 9450 zł+ czynsz: 1700 zł/miesiąc)
        numbers = re.findall(r"\b\d+\b", price_span)
        numbers = [int(number) for number in numbers]
        if len(numbers) > 1:
            return (numbers[0], numbers[1])
        return (numbers[0], None)

    def __init__(self, article_data, area) -> None:
        # Extract Flat Offer data from article_data
        self.url = "https://www.otodom.pl" + article_data.find("a")["href"]

        # Get Text for price, address and other data
        section = article_data.find("section")

        info_list = (
            section.find_all("div", recursive=False)[1].get_text("<sep>").split("<sep>")
        )
        for i in range(len(info_list)):
            print(f"Number {i}: {info_list[i]}")

        if "czynsz" in info_list[2]:
            self.rent, self.czynsz = self.__separate_price(
                info_list[0] + info_list[1] + info_list[2]
            )
            indexes = [4, 6, 8, 12, -1]
        else:
            self.rent = info_list[0].replace("zł", "")
            self.czynsz = None
            indexes = [2, 4, 6, 10, 13]

        self.area = area
        self.street, self.neighbourhood = info_list[indexes[0]].split(",")[0:2]
        self.rooms = re.sub(r"[^\d.]", "", info_list[indexes[1]])
        self.meters = re.sub(r"[^\d.]", "", info_list[indexes[2]])
        self.floor = re.sub(r"[^\d.]", "", info_list[indexes[3]])
        self.private = True if info_list[indexes[4]] == "Oferta prywatna" else False

        if section:
            self.pic_urls = [pic["src"] for pic in section.find_all("img")]
            # print(f"Found {len(self.pic_urls)} pictures for this flat")
        self.id = "1234"

    def __str__(self) -> str:
        if self.private:
            private_str = "Private Offer"
        else:
            private_str = "Agency Offer"

        return (
            f" Flat - {self.area} \nPrice: {self.rent} \nCzynsz: {self.czynsz if self.czynsz is not None else 'Unavailable'}"
            + f"\nStreet: {self.street}, {self.neighbourhood}.\n"
            + f"{self.rooms} room{'s' if int(self.rooms)>1 else ''} | {self.meters}m\u00b2 | floor {self.floor}.\n"
            + private_str
            + "\n"
            + f"URL: {self.url}"
        )

    def __eq__(self, value: object) -> bool:
        """Overrides the default implementation"""
        if isinstance(value, OtodomFlat):
            return self.url == value.url
        return False

    def to_dict(self):
        return {"url": self.url, "price": self.rent, "street": self.street}
