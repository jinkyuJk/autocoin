

def basic_db_check(self,cursor):
    check_list = ['daili_buy_list','daily_craw','min_craw']
    sql = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA"
    cursor.execute(sql)
    rows = cursor.fetchall()
    db_list = [n['SCHEMA_NAME'].lower() for n in rows]
    create_db_tmp = CREATE DATABASE {}
    has_created = False
    for check_name in check_list
        if check_name not in db_list:
            has_create= True
            logger.debu
            create_db-sql = create_db_tmp.format(check-name)
            cursor.execute9create

    if has_create and self.engine_JB.has_table('setting_data'):
        self.engine_JB.excute("""
        UPDATE setting_data SET code_update=""")
        
        
        
        
def db_name_setting(self,db_name):
    self.db_name = db_name
    logger.debug("DB_name !!! %s", self.db_name)
    conn = pymysql.connect(host=cf.db_ip, port= int(cf.db_port), user = cf.db_id, password = cf.db_passwd, charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    with conn.cusor() as cursor:
        if not self.is_database_exist(cursor):
            slef.create_database(cursor)
            
            
            
def is_database_exist(cursor):
    sql = SELECT 1 FROM Information_schema.SCHEMATA WHERE SCHEMA_NAME = '{}'"
    if cursor.execute(sql.format(self.db_name)):
        
    
def create_database(cursor)
    sql = "CREATE DATABASE {}"
    cursor.execute(sql.format(self.db_name))
    
    self.engine_JB = create_engine("mysql +mysqldb://")


def rotate_date(self):
    for i in range(1, len(self.date_rows)):
        date_rows_today = self.date_rows[i][0]