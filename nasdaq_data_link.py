import nasdaqdatalink
import pandas as pd

nasdaqdatalink.read_key(filename="pyalgo.cfg")
data = nasdaqdatalink.get("WIKI/AAPL", start_date="2018-01-01", end_date="2024-07-04")

print(data)
