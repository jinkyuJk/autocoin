import pyupbit
import numpy


print(pyupbit.get_tickers())
len(pyupbit.get_tickers())


#Exchange API

#로그인
access = "rY2mxeDmWiiAxyfwWgQcJFsfCkjSTomMxel1iGZg"          # 본인 값으로 변경
secret = "vxrsTBUI4K2Jx5yxr7kX7YXLuTAA3ziKAIRsvxRu"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

#잔고조회

print(upbit.get_balance("KRW-GRS"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

#과거 데이터 조회

#일별
df = pyupbit.get_ohlcv("KRW-BTC")
print(df)

#interval 옵션으로 월/주/일/분봉 선택가능
df = pyupbit.get_ohlcv("KRW-BTC",interval='minute')
print(df)

#count인자로 최근 n일자 조회가능
df = pyupbit.get_ohlcv("KRW-BTC",count=5)
print(df)

#호가조회

orderbook = pyupbit.get_orderbook("KRW-BTC")
print(orderbook)
bids_asks = orderbook[0]['orderbook_units']

for bid_ask in aids_asks:
    print(bid_ask)


#매수/매도 지정가매수->buy_limit_order()  지정가매도 ->sell_limit_order()
#매수
ret = upbit.buy_limit_order("KRW-XRP",100,20) #ticker,가격,수량
print(ret) #return값인 uuid값으로 미체결주문 취소가능
#매도
ret = upbit.sell_limit_order("KRW-XRP",1000,20)
print(ret)

#주문취소
ret = upbit.cancel_order("취소할 거래 uuid값")