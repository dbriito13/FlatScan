import asyncio
from code import otodom


def lambda_handler(event, context):
    asyncio.run(otodom.send_latest_flat())


if __name__ == "__main__":
    asyncio.run(otodom.send_latest_flat())
