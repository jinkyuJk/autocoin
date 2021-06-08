from library.mk_database import *
from library.cf import *
import pyupbit
import numpy





#Exchange API

#로그인

upbit = pyupbit.Upbit(access_key, secret_key)

#잔고조회

print(upbit.get_balance("KRW-DOGE"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
list = pyupbit.get_tickers('KRW')
print(list)
len(list)
df = pyupbit.get_ohlcv("KRW-BTC",count =600,period=1,to='2021231')

# for coin in list:
#
#     print(coin)
#과거 데이터 조회

# #일별
# df = pyupbit.get_ohlcv("KRW-BTC")
# print(df)
#
# #interval 옵션으로 월/주/일/분봉 선택가능
# df = pyupbit.get_ohlcv("KRW-BTC",interval='minute')
# print(df)
#
# #count인자로 최근 n일자 조회가능
# df = pyupbit.get_ohlcv("KRW-BTC",count=5)
# print(df)
#
# #호가조회
#
# orderbook = pyupbit.get_orderbook("KRW-BTC")
# print(orderbook)
# bids_asks = orderbook[0]['orderbook_units']
#
# for bid_ask in aids_asks:
#     print(bid_ask)
#
#
# #매수/매도 지정가매수->buy_limit_order()  지정가매도 ->sell_limit_order()
# #매수
# ret = upbit.buy_limit_order("KRW-XRP",100,20) #ticker,가격,수량
# print(ret) #return값인 uuid값으로 미체결주문 취소가능
# #매도
# ret = upbit.sell_limit_order("KRW-XRP",1000,20)
# print(ret)
#
# #주문취소
# ret = upbit.cancel_order("취소할 거래 uuid값")