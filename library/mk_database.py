import pymysql
import pandas



class mk_database():
    def __init__(self):
        self.db_conn = pymysql.connect(host=cf.db_ip, port=int(cf.db_port), user=cf.db_id, password= cf.db_passwd, charset='utf8')
        self.engine =

