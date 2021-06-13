from library.cf import *
from library.simulator_func import *
import numpy as np
import os
import time
from PyQt5.QtWidgets import *
import pandas as pd
import pyupbit

from sqlalchemy import create_engine, event, Text, Float
from sqlachemy.pool import Pool
import pymysql

pymysql.install_as_MySQLdb()

class Coin_data():
    def __init__(self):
        self.db_name = cf.db_name
        self.simul_num = cf.simul_num
        self.db_name_setting(self.db_name)
        self.sf = Simulator_func(self.simul_num,'real',self.db_name)
        logger.debug("self.sf.simul_num(알고리즘 번호) : %s", self.sf.simul_num)
        logger.debug("self.sf.db_to_realtime_daily_buy_list_num : %s", self.sf.db_to_realtime_daily_buy_list_num)
        logger.debug("self.sf.sell_list_num : %s", self.sf.sell_list_num)




    def db_name_setting(self,db_name):
        logger.debug(f"db name !!! {self.db_name}")
        conn = pymysql.connect(
            host = cf.db_ip,
            port = int(cf.db_port),
            user = cf.db_id,
            password = cf.db_passwd,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            if not self.is_database_exist(cursor):
                self.create_database(cursor)
        conn.commit()
        conn.close()

        self.engine_craw = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/min_craw",
            encoding='utf-8')
        self.engine_daily_craw = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_craw",
            encoding='utf-8')
        self.engine_daily_buy_list = create_engine(
            "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_buy_list",
            encoding='utf-8')



    def is_database_exist(self,cursor):
        sql = "SELECT 1 FROM Information_schema.SCHEMATA WHERE SCHEMA_NAME = '{}'"
        if cursor.excute(sql.format(self.db_name)):
            logger.debug(f"{self.db_name}가 존재합니다.")
            return True
        else:
            logger.debug(f"{self.db_name}가 존재 하지않습니다")
            return False

    def create_database(self,cursor):
        sql = "CREATE DATABASE {}"
        cursor.execute(sql.format(self.db_name))



        upbit = pyupbit.Upbit(access_key, secret_key)
        tickers = pyupbit.get_tickers('KRW')
        print(tickers,len(tickers))
        print(upbit.get_balances())
        pyupbit.get_ohlcv(ticker="KRW-BTC", interval="day", count=20)
        pyupbit.get_daily_ohlcv_from_base(ticker="KRW-BTC", base=0)


