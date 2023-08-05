import sys

import pandas as pd
import psycopg2

from spark_basic_python.com.tf56.util import configloader
from spark_basic_python.com.tf56.sparkbasic.contextfactory import ContextFactory

config = configloader.buildconfig("pg.datasource.ini")


class DataAccess:
    def __init__(self):
        print ("DataAccess self")

    '''
    function: query_pg 该方法用于查询pg数据库
    parameter: 
              sql-> 查询的sql语句，以分号“;”结尾 
              spark_context-> spark的上下文  
    return： 以spark dataFrame的数据结构返回
    '''
    @staticmethod
    def query_pg(sql):
        try:
            conn = psycopg2.connect(
                database=config.get("pg", "database"), user=config.get("pg", "user"),
                password=config.get("pg", "password"), host=config.get("pg", "host"),
                port=config.get("pg", "port"))
            cursor = conn.cursor()
            cursor.execute(sql)
            pdf = pd.DataFrame(cursor.fetchall())
            sdf = ContextFactory.build_spark_context().createDataFrame(pdf)
        except psycopg2.DatabaseError, exception:
            print (exception)
            sys.exit(1)
        return sdf

    '''
    function: query_hive 查询hive数据库的接口
    params: sql->查询的sql语句
    return: 以spark dataFrame的数据结构返回结果集
    '''
    @staticmethod
    def query_hive(sql):
        return ContextFactory.build_sql_context().sql(sql)
