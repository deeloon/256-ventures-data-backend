# Update daily
import requests
import pandas as pd

# Get timestamp of last entry
filepath = 'data/Coinmetrics/Coinmetrics_btc.csv'
timestamp_df = pd.read_csv(filepath, usecols=['time'])
timestamp_df = timestamp_df.astype('datetime64')
start_time = str(timestamp_df.values[-1][0]+10000000)
start = '&start=' + str(start_time)[:23] + 'Z'

metrics = 'AdrActCnt,BlkCnt,BlkSizeByte,BlkSizeMeanByte,CapMVRVCur,CapMrktCurUSD,CapRealUSD,DiffMean,' \
          'FeeMeanNtv,FeeMeanUSD,FeeMedNtv,FeeMedUSD,FeeTotNtv,FeeTotUSD,IssContNtv,IssContPctAnn,' \
          'IssContUSD,IssTotNtv,IssTotUSD,NVTAdj,NVTAdj90,PriceBTC,PriceUSD,ROI1yr,ROI30d,SplyCur,' \
          'TxCnt,TxTfrCnt,TxTfrValAdjNtv,TxTfrValAdjUSD,TxTfrValMeanNtv,TxTfrValMeanUSD,TxTfrValMedNtv,' \
          'TxTfrValMedUSD,TxTfrValNtv,TxTfrValUSD,VtyDayRet180d,VtyDayRet30d,VtyDayRet60d'
r = requests.get('https://community-api.coinmetrics.io/v2/assets/btc/metricdata.csv?metrics=' + metrics + start)
r.raise_for_status()

csv_list = r.text.split('\n')
with open(filepath, 'a') as csv_file:
    for row in csv_list[1:]:
        csv_file.write(row)
