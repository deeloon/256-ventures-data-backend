import quandl
import pandas as pd

for code in ["BCHAIN/MIREV", "BCHAIN/DIFF", "BCHAIN/HRATE", "BCHAIN/TOTBC", "BCHAIN/TOUTV"]:
    old_data_df = pd.read_csv('data/Quandl/'+ code.replace('/', '_') + '.csv', usecols=['Date'])
    final_timestamp = old_data_df.astype('datetime64').values[-1] + pd.Timedelta(1, unit='d')
    start = str(final_timestamp[0])[:10]
    data_df = quandl.get(code, start_date=start)
    # Append
    data_df.to_csv('data/Quandl/'+ code.replace('/', '_') + '.csv', mode='a', header=False)