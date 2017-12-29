#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# 处理mysql入库相关操作

import ConfigParser
import logging
import datetime, time
import os, sys
import MySQLdb
import pandas as pd

class mysqlProcess:
    # 初始化数据库
    def __init__(self):
        mysqlConfig = ConfigParser.ConfigParser();
        mysqlConfig.read("../config/mysqlInfo.conf");
        self.IP = mysqlConfig.get("MYSQL", "IP");
        self.UserName = mysqlConfig.get("MYSQL", "UserName");
        self.PassWord = mysqlConfig.get("MYSQL", "PassWord");
        self.DBName = mysqlConfig.get("MYSQL", "DBName");
        try:
            self.conn = MySQLdb.connect(host=self.IP, user=self.UserName, passwd=self.PassWord, db=self.DBName,
                                    charset='utf8');
        except MySQLdb.Error, e:
            try:
                sqlError = "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error:%s" % str(e)
    # cursor = self.conn.cursor();
    # cursor.execute('create table test(name TEXT, ablob BLOB)');

    # 获取数据库数据
    def getSQLData(self, str_sql, sql_conn):
        print "read_sql begin %s ..." % time.localtime(time.time());
        print "str_sql : ", str_sql;
        print "sql_conn : ", sql_conn;
        try:
            pdDataSQL = pd.read_sql(str_sql, sql_conn);  # read_sql_table直接读取表所有数据
        except Exception as e:
            print "数据表获取失败,结束程序---", e;
            sql_conn.close();
            sys.exit();
        print "read_sql end %s ..." % time.localtime(time.time());
        return pdDataSQL;

    def __isset(self, v):
        try:
            type(eval(v))
        except:
            return False
        else:
            return True

    def deleteData(self, tableName):
        print "删除数据:", tableName;
        try:
            deleteSQL = "delete from %s where timeStamp<'%s00'" % (tableName, self.rmDay);
            print "deleteSQL : ", deleteSQL;
            cursor = self.conn.cursor();
            cursor.execute(deleteSQL);
            self.conn.commit();
        except Exception as e:
            print ("delete data fails {}".format(e));
        finally:
            if self.__isset("cursor"):
                cursor.close();
            if self.isset("conn"):
                self.conn.close();

    def InsertData(self, fileLoad, tableName, seq):
        print "插入数据库:", tableName;
        print "file Load = %s------tableName=%s-------fileline=%s" % (fileLoad, tableName, seq);
        try:
            insertSQL = "load data local infile '%s' ignore into table %s character set 'utf8' fields terminated by '%s'" % (
                fileLoad, tableName, seq);
            print "insertSQL : ", insertSQL;
            cursor = self.conn.cursor();
            cursor.execute(insertSQL);
            self.conn.commit();
            print "插入数据库成功:", tableName;
        except Exception as e:
            print('LoadFile sql fails {}'.format(e))
        finally:
            if self.__isset("cursor"):
                cursor.close();
            if self.__isset("conn"):
                self.conn.close();
    
    def updateData(self,updateSQL):
        print "更新数据库"
        try:
            print "updateSQL : ", updateSQL;
            cursor = self.conn.cursor();
            cursor.execute(updateSQL);
            self.conn.commit();
            print "更新数据库成功";
        except Exception as e:
            print('LoadFile sql fails {}'.format(e))
        finally:
            if self.__isset("cursor"):
                cursor.close();
            if self.__isset("conn"):
                self.conn.close();
