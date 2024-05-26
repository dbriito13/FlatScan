from code import otodom


def lambda_handler():
    otodom.store_flat(otodom.fetch_latest())


if __name__ == "__main__":
    otodom.store_flat(otodom.fetch_latest())
