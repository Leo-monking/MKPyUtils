# -*- coding: UTF-8 -*-

'''
    Created on 2017-12-20
    filename: Utils.py
    @author: MONKING
    
    内容描述：
    Python常用方法

    依赖包：
    sudo pip install requests
    sudo pip install beautifulsoup
    
'''

import requests
import MySQLdb


class Singleton(object):
    _instance = None
    def __new__(cls,*args,**kw):
        if not cls._instance:
            cls._instance = super(Singleton,cls).__new__(cls,*args,**kw)
        return cls._instance

class PyUtils(Singleton):
    def __init__(self):
        pass

    #根据URL获取html文本内容
    def GetHTMLText(self,url):
        try:
            ret = requests.get(url)
            ret.raise_for_status()
            ret.encoding = ret.apparent_encoding
            return ret.text
        except:
            return ""


import sqlite3
class Sqlite3DB(Singleton):
    conn = None
    #创建数据库连接
    def __init__(self,dbName):
        self.conn = sqlite3.connect(dbName)
        
    def ExecBySql(self,sql,*param):
        cursor = self.conn.cursor()
        cursor.excute(sql,param)
        self.conn.commit()
        
    def GetBySql(self,sql,*param):
        cursor = self.conn.cursor()
        ret = cursor.execute(sql,param)
        self.conn.commit()
        return ret
    
    def __del__(self):
        self.conn.close()
        
        

class MySqlDB(Singleton):
    conn = None
    
    #数据库连接的时候，python 不认localhost
    def __init__(self,host = "127.0.0.1",user = "root",pwd = "",db = "" , port = 3306):
        self.conn = MySQLdb.connect(host , user , pwd , db ,port)
    
    def GetBySql(self,sql,*param):
        cursor = self.conn.cursor()
        ret = cursor.fetchmany(cursor.execute(sql,param))
        self.conn.commit()
        return ret
    
    def GetBySqlRetUnique(self,sql,*param):  
        cursor = self.conn.cursor()#初始化游标
        ret = cursor.fetchmany(cursor.execute(sql,param)) 
        self.conn.commit()#提交上面的sql语句到数据库执行  
        return ret[0][0]
    
    def SetBySql(self,sql,*param):  
        cursor=self.conn.cursor()#初始化游标  
        cursor.execute(sql,param) 
        self.conn.commit()#提交上面的sql语句到数据库执行 
    
    def __del__(self):
        self.conn.close()
    