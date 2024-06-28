import asyncio
from iol_api.client import IOLClient
from iol_api.constants import Mercado


async def main():

    iol_client = IOLClient("desconfiadotota", "acGh*q9:gW>7u_")

    data = await iol_client.get_titulo("SUPV", Mercado.BCBA)

    print(data)


asyncio.run(main())
