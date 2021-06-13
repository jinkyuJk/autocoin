
import sys
is_64bits = sys.maxsize > 2**32
if is_64bits:
    print('64bit 환경입니다.')
else:
    print('32bit 환경입니다.')

from sqlalchemy import event
from sqlalchemy.exc import ProgrammingError

from library.daily_crawler import *
import pymysql.cursors
# import numpy as np
from datetime import timedelta
from library.logging_pack import *
from library import cf
from pandas import DataFrame
import datetime

class Simulator_func:
    def __init(self,simul_num,op,db_name):
        self.simul_num = int(simul_num)

        if self.simul_num ==-1:
            self.date_settting()

        # option이 reset일 경우 실행

        elif op =='reset':
            self.op = 'reset'
            self.simul_reset = True
            self.variable_setting()
            self.rotate_date()

        # option이 continue 일 경우 실행
        elif op =='continue':
            self.op = 'continue'
            self.simul_reset = False
            self.variable_setting()
            self.rotae_date()
        else:
            print(f"simul_num or op 어느 것도 만족 하지 못함 simul num: {simul_num}, op: {}")

    def date_setting(self):
        self.today = datetime.datetime.today().strftime("%Y%m%d")
        self.today_detail = datetime.datetime.today().strftime("%Y%m%d%H%M")
        self.today_date_form = datetime.datetime.strptime(self.today,"%Y%m%d").date()


    def variable_setting(self):
        self.date_setting()
        self.simul_end_date = self.today
        self.start_min = '0900'

        self.use_min = False
        self.only_nine_buy = True
        self.buy_stop = False

        self.trade_check_num = False

        if self.sumul_num ==1:
            self.simul_start_date = '20190101'

            # 매수 리스트 설정 알고리즘
            self.db_to_realtime_daily_buy_list_num = 1
            # 매도 리스트 설정 알고리즘 번호
            self.sell_list_num = 1

            self.start_invest_price = 100000000

            self.invest_unit = 1000000
            self.limit_money = 3000000
            self.sell_point = 10
            self.losscut_point = -2
            # 실전/모의 봇 돌릴 때 매수하는 순간 종목의 최신 종가 보다 1% 이상 오른 경우 사지 않도록 하는 설정(변경 가능)
            self.invest_limit_rate = 1.01
            # 실전/모의 봇 돌릴 때 매수하는 순간 종목의 최신 종가 보다 -2% 이하로 떨어진 경우 사지 않도록 하는 설정(변경 가능)
            self.invest_min_limit_rate = 0.98
        self.db_name_setting()

        if self.op != 'real':
            # database, table 초기화 함수
            self.table_setting()

            # 시뮬레이팅 할 날짜를 가져 오는 함수
            self.get_date_for_simul()

            # 매도를 한 종목들 대상 수익
            self.total_valuation_profit = 0

            # 실제 수익 : 매도를 한 종목들 대상 수익 + 현재 보유 중인 종목들의 수익
            self.sum_valuation_profit = 0

            # 전재산 : 투자금액 + 실제 수익(self.sum_valuation_profit)
            self.total_invest_price = self.start_invest_price

            # 현재 총 투자한 금액
            self.total_purchase_price = 0

            # 현재 투자 가능한 금액(예수금) = (초기자본 + 매도한 종목의 수익) - 현재 총 투자 금액
            self.d2_deposit = self.start_invest_price

            # 일별 정산 함수
            self.check_balance()

            # 매수할때 수수료 한번, 매도할때 전체금액에 세금, 수수료
            self.tax_rate = 0.0025
            self.fees_rate = 0.00015

            # 시뮬레이터를 멈춘 지점 부터 다시 돌리기 위해 사용하는 변수(중요X)
            self.simul_reset_lock = False

    def table_setting(self):
        print("self.simul_reset" + str(self.simul_reset))
        # 시뮬레이터를 초기화 하고 처음부터 구축하기 위한 로직
        if self.simul_reset:
            print("table reset setting !!! ")
            self.init_database()
        # 시뮬레이터를 초기화 하지 않고 마지막으로 끝난 시점 부터 구동하기 위한 로직
        else:
            # self.simul_reset 이 False이고, 시뮬레이터 데이터베이스와, all_item_db 테이블, jango_table이 존재하는 경우 이어서 시뮬레이터 시작
            if self.is_simul_database_exist() and self.is_simul_table_exist(self.db_name,
                                                                            "all_item_db") and self.is_simul_table_exist(
                self.db_name, "jango_data"):
                self.init_df_jango()
                self.init_df_all_item()
                # 마지막으로 구동했던 시뮬레이터의 날짜를 가져온다.
                self.last_simul_date = self.get_jango_data_last_date()
                print("self.last_simul_date: " + str(self.last_simul_date))
            #    초반에 reset 으로 돌다가 멈춰버린 경우 다시 init 해줘야함
            else:
                print("초반에 reset 으로 돌다가 멈춰버린 경우 다시 init 해줘야함 ! ")
                self.init_database()
                self.simul_reset = True

    def init_database(self):
        self.drop_database()
        self.create_database()
        self.init_df_jango()
        self.init_df_all_item()

        # 데이터베이스를 삭제하는 함수

    def drop_database(self):
        if self.is_simul_database_exist():
            print("drop!!!!")
            sql = "drop DATABASE %s"
            self.db_conn.cursor().execute(sql % (self.db_name))
            self.db_conn.commit()

    def is_simul_database_exist(self):
        sql = "SELECT 1 FROM Information_schema.SCHEMATA WHERE SCHEMA_NAME = '%s'"
        rows = self.engine_daily_buy_list.execute(sql % (self.db_name)).fetchall()
        print("rows : ", rows)
        if len(rows):
            return True
        else:
            return False



    def create_database(self):
        if not self.is_simul_database_exist() :
            sql = 'CREATE DATABASE %s'
            self.db_conn.cursor().execute(sql % (self.db_name))
            self.db_conn.commit()

    def init_df_jango(self):
        jango_temp = {'id': []}

        self.jango = DataFrame(jango_temp,
                               columns=['date', 'today_earning_rate', 'sum_valuation_profit', 'total_profit',
                                        'today_profit',
                                        'today_profitcut_count', 'today_losscut_count', 'today_profitcut',
                                        'today_losscut',
                                        'd2_deposit', 'total_possess_count', 'today_buy_count', 'today_buy_list_count',
                                        'today_reinvest_count',
                                        'today_cant_reinvest_count',
                                        'total_asset',
                                        'total_invest',
                                        'sum_item_total_purchase', 'total_evaluation', 'today_rate',
                                        'today_invest_price', 'today_reinvest_price',
                                        'today_sell_price', 'volume_limit', 'reinvest_point', 'sell_point',
                                        'max_reinvest_count', 'invest_limit_rate', 'invest_unit',
                                        'rate_std_sell_point', 'limit_money', 'total_profitcut', 'total_losscut',
                                        'total_profitcut_count',
                                        'total_losscut_count', 'loan_money', 'start_kospi_point',
                                        'start_kosdaq_point', 'end_kospi_point', 'end_kosdaq_point',
                                        'today_buy_total_sell_count',
                                        'today_buy_total_possess_count', 'today_buy_today_profitcut_count',
                                        'today_buy_today_profitcut_rate', 'today_buy_today_losscut_count',
                                        'today_buy_today_losscut_rate',
                                        'today_buy_total_profitcut_count', 'today_buy_total_profitcut_rate',
                                        'today_buy_total_losscut_count', 'today_buy_total_losscut_rate',
                                        'today_buy_reinvest_count0_sell_count',
                                        'today_buy_reinvest_count1_sell_count', 'today_buy_reinvest_count2_sell_count',
                                        'today_buy_reinvest_count3_sell_count', 'today_buy_reinvest_count4_sell_count',
                                        'today_buy_reinvest_count4_sell_profitcut_count',
                                        'today_buy_reinvest_count4_sell_losscut_count',
                                        'today_buy_reinvest_count5_sell_count',
                                        'today_buy_reinvest_count5_sell_profitcut_count',
                                        'today_buy_reinvest_count5_sell_losscut_count',
                                        'today_buy_reinvest_count0_remain_count',
                                        'today_buy_reinvest_count1_remain_count',
                                        'today_buy_reinvest_count2_remain_count',
                                        'today_buy_reinvest_count3_remain_count',
                                        'today_buy_reinvest_count4_remain_count',
                                        'today_buy_reinvest_count5_remain_count'],
                               index=jango_temp['id'])

        # all_item_db 라는 테이블을 만들기 위한 self.df_all_item 데이터프레임

    def init_df_all_item(self):
        df_all_item_temp = {'id': []}

        self.df_all_item = DataFrame(df_all_item_temp,
                                     columns=['id', 'order_num', 'code', 'code_name', 'rate', 'purchase_rate',
                                              'purchase_price',
                                              'present_price', 'valuation_price',
                                              'valuation_profit', 'holding_amount', 'buy_date', 'item_total_purchase',
                                              'chegyul_check', 'reinvest_count', 'reinvest_date', 'invest_unit',
                                              'reinvest_unit',
                                              'sell_date', 'sell_price', 'sell_rate', 'rate_std', 'rate_std_mod_val',
                                              'rate_std_htr', 'rate_htr',
                                              'rate_std_mod_val_htr', 'yes_close', 'close', 'd1_diff_rate', 'd1_diff',
                                              'open', 'high',
                                              'low',
                                              'volume', 'clo5', 'clo10', 'clo20', 'clo40', 'clo60', 'clo80',
                                              'clo100', 'clo120', "clo5_diff_rate", "clo10_diff_rate",
                                              "clo20_diff_rate", "clo40_diff_rate", "clo60_diff_rate",
                                              "clo80_diff_rate", "clo100_diff_rate", "clo120_diff_rate"])

    def is_simul_table_exist(self, db_name, table_name):
        sql = "select 1 from information_schema.tables where table_schema = '%s' and table_name = '%s'"
        rows = self.engine_simulator.execute(sql % (db_name, table_name)).fetchall()
        if len(rows) == 1:
            return True
        else:
            return False

    def get_jango_data_last_date(self):
        sql = "SELECT date from jango_data order by date desc limit 1"
        return self.engine_simulator.execute(sql).fetchall()[0][0]

        # 시뮬레이팅 할 날짜를 가져 오는 함수
        # 장이 열렸던 날 들을 self.date_rows 에 담기 위해서 gs글로벌의 date값을 대표적으로 가져온 것
        def get_date_for_simul(self):
            sql = "select date from `gs글로벌` where date >= '%s' and date <= '%s' group by date"
            self.date_rows = self.engine_daily_craw.execute(
                sql % (self.simul_start_date, self.simul_end_date)).fetchall()

    def check_balance(self):
        # all_item_db가 없으면 check_balance 함수를 나가라
        if self.is_simul_table_exist(self.db_name, "all_item_db") == False:
            return

        # 총 수익 금액 (종목별 평가 금액 합산)
        sql = "SELECT sum(valuation_profit) from all_item_db"
        self.sum_valuation_profit = self.engine_simulator.execute(sql).fetchall()[0][0]
        print("sum_valuation_profit: " + str(self.sum_valuation_profit))

        # 전재산이라고 보면 된다. 현재 총손익 까지 고려했을 때
        self.total_invest_price = self.start_invest_price + self.sum_valuation_profit

        # 현재 총 투자한 금액 계산
        sql = "select sum(item_total_purchase) from all_item_db where sell_date = '%s'"
        self.total_purchase_price = self.engine_simulator.execute(sql % (0)).fetchall()[0][0]
        if self.total_purchase_price is None:
            self.total_purchase_price = 0

        # 매도를 한 종목들 대상 수익 계산
        sql = "select sum(valuation_profit) from all_item_db where sell_date != '%s'"
        self.total_valuation_profit = self.engine_simulator.execute(sql % (0)).fetchall()[0][0]

        if self.total_valuation_profit is None:
            self.total_valuation_profit = 0

        # 현재 투자 가능한 금액(예수금) = (초기자본 + 매도한 종목의 수익) - 현재 총 투자 금액
        self.d2_deposit = self.start_invest_price + self.total_valuation_profit - self.total_purchase_price

    def db_name_setting(self):
        if self.op == "real":
            self.engine_simulator = create_engine(
                "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/" + str(
                    self.db_name),
                encoding='utf-8')

        else:
            # db_name을 setting 한다.
            self.db_name = "simulator" + str(self.simul_num)
            self.engine_simulator = create_engine(
                "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/" + str(
                    self.db_name), encoding='utf-8')

        self.engine_daily_craw = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_craw",
            encoding='utf-8')

        self.engine_craw = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/min_craw",
            encoding='utf-8')
        self.engine_daily_buy_list = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_buy_list",
            encoding='utf-8')

        from library.open_api import escape_percentage
        event.listen(self.engine_simulator, 'before_execute', escape_percentage, retval=True)
        event.listen(self.engine_daily_craw, 'before_execute', escape_percentage, retval=True)
        event.listen(self.engine_craw, 'before_execute', escape_percentage, retval=True)
        event.listen(self.engine_daily_buy_list, 'before_execute', escape_percentage, retval=True)

        # 특정 데이터 베이스가 아닌, mysql 에 접속하는 객체
        self.db_conn = pymysql.connect(host=cf.db_ip, port=int(cf.db_port), user=cf.db_id, password=cf.db_passwd,
                                       charset='utf8')

    # 날짜 별 로테이팅 함수
    def rotate_date(self):
        for i in range(1, len(self.date_rows)):
            # print("self.date_rows!!" ,self.date_rows)
            # 시뮬레이팅 할 일자
            date_rows_today = self.date_rows[i][0]
            # 시뮬레이팅 하기 전의 일자
            date_rows_yesterday = self.date_rows[i - 1][0]

            # self.simul_reset 이 False, 즉 시뮬레이터를 멈춘 지점 부터 실행하기 위한 조건
            if not self.simul_reset and not self.simul_reset_lock:
                if int(date_rows_today) <= int(self.last_simul_date):
                    print("**************************   date: " + date_rows_today + "simul jango date exist pass ! ")
                    continue
                else:
                    self.simul_reset_lock = True

            # 분별 시뮬레이팅
            if self.use_min:
                self.simul_by_min(date_rows_today, date_rows_yesterday, i)
            # 일별 시뮬레이팅
            else:
                self.simul_by_date(date_rows_today, date_rows_yesterday, i)
