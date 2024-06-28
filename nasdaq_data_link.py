import nasdaqdatalink
import pandas as pd

nasdaqdatalink.read_key(filename='pyalgo.cfg')
data = nasdaqdatalink.get('CFTC/001602_F_ALL', start_date='2018-01-01', end_date='2020-05-01')

data.info()


