import pyupbit
import numpy as np
import pandas as pd

#로그인
access = "rY2mxeDmWiiAxyfwWgQcJFsfCkjSTomMxel1iGZg"          # 본인 값으로 변경
secret = "vxrsTBUI4K2Jx5yxr7kX7YXLuTAA3ziKAIRsvxRu"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)


#일별
df = pyupbit.get_ohlcv("KRW-BTC")
print(df)

#DataFrame 객체를 엑셀로 저장하기
# df = pyupbit.get_ohlcv("KRW-BTC")
# df.to_excel("btc.xlsx")

df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
df['range'] = (df['high'] - df['low']) *0.5
df['target'] = df['open'] +df['range'].shift(1)
df['bull'] = df['open'] > df['ma5']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'],df['close'] / df['target'] -fee,1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() *100
print("MDD:", df['dd'].max())
print("HPR:",df['hpr'][-2])
df.to_excel("larry_ma.xlsx")

#기간 수익률이 높은 코인찾기

def get_hpr(ticker):
    try:
        df = pyupbit.get_ohlcv(ticker)
        df = df['2020']

        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high'] - df['low']) *0.5
        df['target'] = df['open'] +df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']

        fee = 0.0032
        df['ror'] =np.where((df['high'] > df['target']) &df['bull'], df['close'] / df['target'] -fee, 1 )
        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax - df['hpr'])/df['hpr'].cummax()*100
        return df['hpr'][-2] #-2를 가져오는이유는?

    except:
        return 1

tickers = pyupbit.get_tickers(fiat='KRW')
hprs = []
for ticker in tickers:
    hpr = get_hpr(ticker)
    hprs.append((ticker,hpr))

sorted_hprs = sorted(hprs, key=lambda x:x[1],reverse=True)
print(sorted_hprs[:5])


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv('KRW-BTC')
    df['range'] = (df['high'] - df['low']) *k
    df['target']  = df['open'] +df['range'].shift(1)

    fee = 0
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] -fee ,1)
    ror = df['ror'].cumprod()[-2] #오늘은 장이아직안끝났으니깐....?
    return ror

for k in np.arange(0.1,1.0,0.1):
    ror = get_ror(k)
    print(f"{k:.1f}-> {ror} ")