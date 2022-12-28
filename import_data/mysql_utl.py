import pymysql

class Mysql():
    def __init__(self,endpoint,user,pwd):
        try:
            self._conn = pymysql.connect(host=endpoint, user=user, passwd=pwd)
            self._cursor = self._conn.cursor()
        except Exception as e:
            print("Database connection failed due to {}".format(e))
            raise SystemExit

    def __exit__(self):
        self.close()

    def create_database(self, dbname):    
        try:            
            sql_query = 'show databases'
            self._cursor.execute(sql_query)
            databases = self._cursor.fetchall()
            
            for database in databases:
                if dbname == database[0]:
                    print (f'Database {dbname} already exists!')
                    return
                
            sql_statement = 'create database '+ dbname  
            self._cursor.execute(sql_statement)
            print (f'Database {dbname} created!')

        except Exception as e:
            print("Exeception occured:{}".format(e))
    
    def create_table(self, table_name, table_scheme):
        try:
            self._cursor.execute(f'create table {table_name} ({table_scheme});')

            print (f'Table {table_name} created!')
        except Exception as e:
            print("Exeception occured:{}".format(e))
    
    def insert(self, command):
        try:
            self._cursor.execute(command)
        except Exception as e:
            print("Exeception occured:{}".format(e))

    def commit(self):
        self._conn.commit()
        print ('Commit realized!')