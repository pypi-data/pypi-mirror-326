import abc
import configparser
import getpass
import json
import logging
import re
import shutil
import smtplib
import socket
import subprocess
import sys
import traceback
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ftplib import FTP
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from time import sleep
import datetime

import netifaces
import pymssql
import pymysql
import requests
from func_timeout import func_set_timeout, FunctionTimedOut
from pymysql.cursors import DictCursor
import urllib3
from hashlib import md5

import os





"""RPA  python语言统一框架"""
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64': base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()





def download(localPath, remotePath, filename):
    import json
    import requests
    import netifaces

    ip_address = ''
    try:
        # 获取网络接口列表
        interfaces = netifaces.interfaces()
        # 查找第一个非本地回环接口的IP地址
        for interface in interfaces:
            if interface == 'lo':
                continue
            addresses = netifaces.ifaddresses(interface)
            ip_addresses = addresses.get(netifaces.AF_INET)
            if ip_addresses:
                ip_address = ip_addresses[0]['addr']
                break
    except:
        pass

    """获取machecode"""
    url = "http://platform-rpa.myeverok.com/rest/getMachineCode"
    data = {
        "ip": ip_address
    }
    response = requests.post(url=url, json=data)
    result = json.loads(response.text)
    machineCode = result.get("message")
    url = "https://platform-rpa.myeverok.com/rest/getParam"
    data = {
        "machineCode": machineCode
    }
    response = requests.post(url, json=data)
    Config = json.loads(json.loads(response.text).get("mapper").get("FTP_INFO"))
    HOST = Config.get("host")
    user = Config.get("user")
    passwd = Config.get("password")
    ftp = myFTP(HOST, user, passwd)
    ftp.downloadFile(localPath, remotePath, filename)

class myFTP:
    def __init__(self, HOST, user, passwd):
        self.ftp = FTP(host=HOST, user=user, passwd=passwd)
        self.ftp.login(user=user, passwd=passwd)

    def upload(self, DIR, fileName):
        self.ftp.cwd(DIR)
        with open(fileName, 'rb') as f:
            self.ftp.storbinary('STOR ' + fileName, f, blocksize=2048)
        self.close()

    def close(self):
        self.ftp.quit()

    def downloadFile(self, localPath, remotePath, filename):
        """
        从FTP下载指定文件
        :param localPath:
        :param remotePath:
        :param filename:
        :return:
        """
        os.chdir(localPath)  # 切换工作路径到下载目录
        self.ftp.cwd(remotePath)  # 要登录的ftp目录
        self.ftp.nlst()  # 获取目录下的文件
        file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handle, blocksize=1024)  # 下载ftp文件
        self.close()

    def uploadFile(self, remotePath, filename):
        self.ftp.cwd(remotePath)
        with open(filename, 'rb') as f:
            self.ftp.storbinary('STOR ' + filename, f, blocksize=2048)
        self.close()
class WinxinApi(object):
    def __init__(self, corpid, secret, agentid, touser='', totag = '',chatid=''):
        self.secret = secret  # 企业微信应用凭证
        self.corpid = corpid  # 企业微信id
        self.agentid = agentid  # 应用Agentid
        self.touser = touser  # 接收消息的userid
        self.chatid = chatid  # 接收消息的群id
        self.totag = totag    # 接收消息的标签
        self.http = urllib3.PoolManager()

    def __get_token(self):
        # '''token获取'''
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.corpid, self.secret)
        r = self.http.request('GET', url)
        req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            return data['access_token']
        else:
            raise ValueError(data)

    def __upload_file(self, file_path, type='file'):
        # '''上传临时文件'''
        if not os.path.exists(file_path):
            raise ValueError("{},文件不存在".format(file_path))
        file_name = file_path.split("\\")[-1]

        token = self.__get_token()
        with open(file_path, 'rb') as f:
            file_content = f.read()

        files = {'filefield': (file_name, file_content, 'text/plain')}
        # return files
        url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}".format(token, type)
        r = self.http.request('POST', url, fields=files)
        req = r.data.decode("utf-8")
        # req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            return data['media_id']
        else:
            raise ValueError(data)

    def send_file_message(self, file_path):
        token = self.__get_token()

        media_id = self.__upload_file(file_path)
        # return media_id
        body = {
            "agentid": self.agentid,  # agentid
            "touser": self.touser,
            "totag":self.totag,
            "chatid": self.chatid,
            "msgtype": "file",  # 消息类型，此时固定为：file
            "file": {"media_id": media_id},  # 文件id，可以调用上传临时素材接口获取
            "safe": 0  # 表示是否是保密消息，0表示否，1表示是
        }
        list_urls = []
        if self.totag or self.touser:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
            list_urls.append(url)
        if self.chatid:
            url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={}".format(token)
            list_urls.append(url)
        bodyjson = json.dumps(body)
        for url in list_urls:
            r = self.http.request('POST', url, body=bodyjson)
            req = r.data.decode("utf-8")
            data = json.loads(req)
            if data["errcode"] == 0:
                print("发送文件到企业微信成功")
                # return data
                continue
            else:
                raise ValueError(data)
    def send_img_message(self, file_path):
        token = self.__get_token()

        media_id = self.__upload_file(file_path,"image")
        # return media_id
        body = {
            "agentid": self.agentid,  # agentid
            "touser": self.touser,
            "totag":self.totag,
            "chatid": self.chatid,
            "msgtype": "image",  # 消息类型，此时固定为：file
            "image": {"media_id": media_id},  # 文件id，可以调用上传临时素材接口获取
            "safe": 0  # 表示是否是保密消息，0表示否，1表示是
        }
        list_urls = []
        if self.totag or self.touser:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
            list_urls.append(url)
        if self.chatid:
            url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={}".format(token)
            list_urls.append(url)
        bodyjson = json.dumps(body)
        for url in list_urls:
            r = self.http.request('POST', url, body=bodyjson)
            req = r.data.decode("utf-8")
            data = json.loads(req)
            if data["errcode"] == 0:
                print("发送文件到企业微信成功")
                # return data
                continue
            else:
                raise ValueError(data)

    def send_message(self, toUser, toTag, error_level, error_code, error_desc, task_id, process_id, busi_record_id,
                     exe_machine):
        """
        :param toUser: 错误通知人 多个则用|分割    A|B|C
        :param toTag: 错误通知标签
        :param error_level: 错误危机程度 1: 紧急    2: 重要    3: 普通
        :param error_code: 错误码
        :param error_desc: 错误描述
        :param task_id: 流程ID
        :param process_id: 任务ID
        :param busi_record_id: 业务任务ID
        :param exe_machine: 执行机器 可传机器码 可传IP
        :param toTag: 错误通知标签
        :param toGroup: 错误通知群ID
        :return:
        """
        token = self.__get_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
        color = 'black'
        if error_level == '紧急':
            color = 'warning'
        elif error_level == '重要':
            color = 'comment'
        markdown = {
            "content": f"报错通知 \n>   <font color='{color}'>**{error_level}**</font> \n>  <font color='{color}'>流程ID:  {task_id}</font> \n>  <font color='{color}'>任务ID:  {process_id}</font> \n> <font color='{color}'>业务任务ID:  {busi_record_id}</font> \n> <font color='{color}'>错误编码:  {error_code}</font> \n> <font color='{color}'>错误描述:  {error_desc}</font>\n>  <font color='{color}'>机器:  {exe_machine}</font>"
        }

        body = {
            "agentid": self.agentid,  # agentid
            "touser": toUser,
            "totag": toTag,
            "toparty": "",
            "msgtype": "markdown",
            "markdown": markdown,  # 消息类型，此时固定为：file
            "safe": 0,  # 表示是否是保密消息，0表示否，1表示是
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        bodyjson = json.dumps(body)
        r = self.http.request('POST', url, body=bodyjson)
        req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            print("发送消息到企业微信成功")
            return 'success'
        else:
            print(req)
            return 'error'

    def send_message_common(self, message):
        """
        :param toUser: 错误通知人 多个则用|分割    A|B|C
        :param toTag: 错误通知标签
        :param message: 发送的消息内容
        :return:
        """
        token = self.__get_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
        body = {
            "agentid": self.agentid,  # agentid
            "touser": self.touser,
            "totag": self.totag,
            "toparty": "",
            "msgtype": "text",
            "text":{
                "content":message
            },
            "safe": 0,  # 表示是否是保密消息，0表示否，1表示是
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        bodyjson = json.dumps(body)
        r = self.http.request('POST', url, body=bodyjson)
        req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            print("发送消息到企业微信成功")
            return 'success'
        else:
            print(req)
            return 'error'

    def send_message_group(self, group_id, error_level, error_code, error_desc, task_id, process_id, busi_record_id,
                           exe_machine):
        """
        :param group_id: 错误通知群ID
        :param error_level: 错误危机程度 1: 紧急    2: 重要    3: 普通
        :param error_code: 错误码
        :param error_desc: 错误描述
        :param task_id: 流程ID
        :param process_id: 任务ID
        :param busi_record_id: 业务任务ID
        :param exe_machine: 执行机器 可传机器码 可传IP

        :return:
        """
        token = self.__get_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={}'.format(token)
        color = 'black'
        if error_level == '紧急':
            color = 'warning'
        elif error_level == '重要':
            color = 'comment'

        markdown = {
            "content": f"报错通知 \n>   <font color='{color}'>**{error_level}**</font> \n>  <font color='{color}'>流程ID:  {task_id}</font> \n>  <font color='{color}'>任务ID:  {process_id}</font> \n> <font color='{color}'>业务任务ID:  {busi_record_id}</font> \n> <font color='{color}'>错误编码:  {error_code}</font> \n> <font color='{color}'>错误描述:  {error_desc}</font>\n>  <font color='{color}'>机器:  {exe_machine}</font>"
        }
        body = {
            "chatid": group_id,
            "msgtype": "markdown",
            "markdown": markdown,  # 消息类型，此时固定为：file
            "safe": 0,  # 表示是否是保密消息，0表示否，1表示是
        }
        bodyjson = json.dumps(body)
        r = self.http.request('POST', url, body=bodyjson)
        req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            print("发送消息到企业微信成功")
            return 'success'
        else:
            print(req)
            return 'error'

    def send_message_group_common(self,message):
        token = self.__get_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={}'.format(token)
        body = {
            "chatid": self.chatid,
            "msgtype": "text",
            "text" : {
                   "content" : message
               },
            "safe": 0,  # 表示是否是保密消息，0表示否，1表示是
        }
        bodyjson = json.dumps(body)
        r = self.http.request('POST', url, body=bodyjson)
        req = r.data.decode("utf-8")
        data = json.loads(req)
        if data["errcode"] == 0:
            print("发送消息到企业微信成功")
            return 'success'
        else:
            print(req)
            return 'error'
class MySQLDataBase:

    def __init__(self,host=None,port=None,username=None,password=None,database=None):

        #cursorclass=cursors.DictCursor
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.database=database

    def __enter__(self):
        self.db = pymysql.connect(host=self.host,port=self.port,user=self.username,password=self.password,database=self.database,cursorclass =DictCursor)
        return self.db
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()



class SQLSERVERDataBase:
    def __init__(self,host=None,port=None,username=None,password=None,database=None):
        #cursorclass=cursors.DictCursor
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.database=database

    def __enter__(self):
        self.db = pymssql.connect(host=self.host,port=self.port,user=self.username,password=self.password,database=self.database)
        return self.db
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()



def timer_decorator(time):
    def actual_decorator(func):
        @wraps(func)
        @func_set_timeout(time)
        def wrapper(*args, **kwargs):
            print(f"{func}开始执行")
            result = func(*args, **kwargs)
            print(f"{func}结束执行")
            return result
        return wrapper
    return actual_decorator
class Robot(metaclass=abc.ABCMeta):
    @classmethod
    def getParams(cls,taskID):
        """
        :param submit: submit:0 预发  1 生产  2 测试
        :return:
        """
        """获取流程参数"""

        """获取CMD数据库配置信息"""
        # 从FTP获取生产测试数据库地址
        localPath = r"C:\tools\databaseConfig"
        remotePath = "databaseConfig/"
        fileName = "config.ini"
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        download(localPath, remotePath, fileName)
        dbConfig = f"{localPath}\\{fileName}"
        if not os.path.exists(dbConfig):
            raise Exception("配置表下载失败")
        config = configparser.ConfigParser()
        # 读取INI文件
        config.read(dbConfig, encoding="utf-8")
        ub_host = config.get('ub_database', "host")
        ub_port = int(config.get('ub_database', "port"))
        ub_username = config.get('ub_database', "username")
        ub_password = config.get('ub_database', "password")
        ub_database = config.get('ub_database', "database")
        with MySQLDataBase(ub_host, ub_port, ub_username, ub_password, ub_database) as myRPADB:
            cursor = myRPADB.cursor()
            sql = f"SELECT * FROM tbl_cmd_task_paramter where task_id='{taskID}'"
            cursor.execute(sql)
            res = cursor.fetchall()
        params = {}
        for item in res:
            params[item.get('name')] = item.get("value")
        return params
    @classmethod
    def report(cls,envType, task_id, process_id, busi_record_id, error_level, error_code, error_desc, exe_machine, toUser):
        """
        :param envType: 区分生产测试      1：生产  0：测试
        :param task_id: 流程ID
        :param process_id: 任务ID
        :param busi_record_id: 业务任务ID
        :param error_level: 错误危机程度      1:紧急     2:重要     3:普通
        :param error_code:错误码
        :param error_desc:错误描述
        :param exe_machine:执行机器   可传机器码  可传IP
        :param toUser: 错误通知人   多个则用|分割   A|B|C
        :return:
        """
        errorLevelMap = {
            1: "紧急",
            2: "重要",
            3: "普通",
        }

        # 从FTP获取生产测试数据库地址
        localPath = r"C:\tools\databaseConfig"
        remotePath = "databaseConfig/"
        fileName = "config.ini"
        if not os.path.exists(localPath):
            os.makedirs(localPath)
        download(localPath, remotePath, fileName)
        dbConfig = f"{localPath}\\{fileName}"
        if not os.path.exists(dbConfig):
            raise Exception("配置表下载失败")
        config = configparser.ConfigParser()
        # 读取INI文件
        config.read(dbConfig, encoding="utf-8")
        # 获取指定section中的值

        pro_host = config.get('database_produce', "host")
        pro_port = config.get('database_produce', "port")
        pro_username = config.get('database_produce', "username")
        pro_password = config.get('database_produce', "password")
        pro_database = config.get('database_produce', "database")

        test_host = config.get('database_test', "host")
        test_port = config.get('database_test', "port")
        test_username = config.get('database_test', "username")
        test_password = config.get('database_test', "password")
        test_database = config.get('database_test', "database")

        if envType == 1:
            host = pro_host
            port = int(pro_port)
            username = pro_username
            password = pro_password
            database = pro_database
        else:
            host = test_host
            port = int(test_port)
            username = test_username
            password = test_password
            database = test_database

        # 有业务任务ID用业务任务ID 没有就用任务ID
        if busi_record_id is None or busi_record_id == "":
            busi_record_id = process_id

        """错误入库"""
        exe_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with MySQLDataBase(host, port, username, password, database) as myRPADB:
            cursor = myRPADB.cursor()
            # 获取默认消息接收人
            sql = 'select * from T01_BUSI_PARAM'
            cursor.execute(sql)
            list_param = cursor.fetchall()
            config = {item['PARAM_KEY']: item['PARAM_VALUE'] for item in list_param}

            # exe_machine匹配成MACHINE_NAME
            res = re.findall('\d+\.\d+\.\d+\.\d+', exe_machine)
            sql = "select * from T00_SYS_00_MACHINE_NAME"
            cursor.execute(sql)
            list_machine = cursor.fetchall()
            if len(res) > 0:
                # exe_machine是IP
                dict_machine_ip = {item['MACHINE_IP']: item['MACHINE_NAME'] for item in list_machine}
                machine_name = dict_machine_ip.get(exe_machine, '未知IP')
            else:
                # exe_machine是machine_code
                dict_machine_code = {item['MACHINE_CODE']: item['MACHINE_NAME'] for item in list_machine}
                machine_name = dict_machine_code.get(exe_machine, '未知机器码')

            if error_code == '200000':
                sql = "UPDATE T00_SYS_00_ERROR_TASK_INFO SET FINAL_STATUS='SUCCESS' WHERE BUSI_RECORD_ID=%s"
                params = [busi_record_id]
                cursor.execute(sql, params)
                myRPADB.commit()
            else:
                id = uuid.uuid1().hex
                # FINAL_STATUS = None
                sql = "insert into T00_SYS_00_ERROR_TASK_INFO(ID,TASK_ID,PROCESS_ID,BUSI_RECORD_ID,ERROR_CODE,ERROR_DESC,EXE_TIME,EXE_MACHINE,ERROR_LEVEL) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = [id, task_id, process_id, busi_record_id, error_code, error_desc, exe_time,
                          machine_name, errorLevelMap.get(error_level)]
                cursor.execute(sql, params)
                myRPADB.commit()
                """发送消息通知"""
                wechat = WinxinApi(config.get('corpid_me'), config.get('corpsecret_me'), config.get('agentId_me'),
                                   toUser)
                if error_level == 1:
                    if toUser:
                        wechat.send_message(toUser, "", errorLevelMap.get(error_level), error_code, error_desc, task_id,
                                            process_id,
                                            busi_record_id, machine_name)
                    wechat.send_message_group("RPAEmergencyProblemGroup", errorLevelMap.get(error_level), error_code,
                                              error_desc,
                                              task_id, process_id, busi_record_id, machine_name)
    @classmethod
    def getDbConfig(cls,submit):
        """
        :param submit: submit:0 预发  1 生产  2 测试
        :return:
        """
        submit = submit
        # 从FTP获取生产测试数据库地址
        localPath = r"C:\tools\databaseConfig"
        remotePath = "databaseConfig/"
        fileName = "config.ini"
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        download(localPath, remotePath, fileName)
        dbConfig = f"{localPath}\\{fileName}"
        if not os.path.exists(dbConfig):
            raise Exception("配置表下载失败")
        config = configparser.ConfigParser()
        # 读取INI文件
        config.read(dbConfig, encoding="utf-8")
        # 获取指定section中的值

        pro_host = config.get('database_produce', "host")
        pro_port = int(config.get('database_produce', "port"))
        pro_username = config.get('database_produce', "username")
        pro_password = config.get('database_produce', "password")
        pro_database = config.get('database_produce', "database")

        test_host = config.get('database_test', "host")
        test_port = int(config.get('database_test', "port"))
        test_username = config.get('database_test', "username")
        test_password = config.get('database_test', "password")
        test_database = config.get('database_test', "database")

        ub_host = config.get('ub_database', "host")
        ub_port = int(config.get('ub_database', "port"))
        ub_username = config.get('ub_database', "username")
        ub_password = config.get('ub_database', "password")
        ub_database = config.get('ub_database', "database")

        """读取所有配置文件返回 """
        dbConfigMap = {}
        sections = config.sections()
        for sectionName in sections:
            host = config.get(sectionName, "host")
            port = int(config.get(sectionName, "port"))
            username = config.get(sectionName, "username")
            password = config.get(sectionName, "password")
            database = config.get(sectionName, "database")
            dbConfigMap[sectionName] = {"host": host, "port": port, "username": username, "password": password,
                                        "database": database}

        if submit == 1:
            return [pro_host, pro_port, pro_username, pro_password, pro_database]
        elif submit == 0:
            return [test_host, test_port, test_username, test_password, test_database]
        elif submit == 2:
            return [test_host, test_port, test_username, test_password, test_database]
        else:
            raise Exception("submit error")

    @classmethod
    def get_private_ips(cls):
        ip_address = ''
        try:
            # 获取网络接口列表
            interfaces = netifaces.interfaces()
            # 查找第一个非本地回环接口的IP地址
            for interface in interfaces:
                if interface == 'lo':
                    continue
                addresses = netifaces.ifaddresses(interface)
                ip_addresses = addresses.get(netifaces.AF_INET)
                if ip_addresses:
                    ip_address = ip_addresses[0]['addr']
                    break
        except:
            pass
        return ip_address


    def __init__(self,taskId,retryTimes,submit,flowName,maxTimeOut,human_flag):
        self.taskId=taskId
        self.errorTime=0
        self.retryTimes=retryTimes
        self.submit=submit
        self.flowName=flowName  #流程名称
        self.maxTimeOut=maxTimeOut  #主方法最大执行时间
        host, port, dbUser, dbPsd, database,ub_host,ub_port,ub_username,ub_password,ub_database,dbConfigMap = self.getDBConfig_RPA()  # 获取数据库连接信息
        self.host = host
        self.port = port
        self.dbUser = dbUser
        self.dbPsd = dbPsd
        self.database = database
        self.ub_host = ub_host
        self.ub_port = ub_port
        self.ub_username = ub_username
        self.ub_password = ub_password
        self.ub_database = ub_database
        self.driver=None
        self.ubDbConnect=None
        self.dbConfigMap=dbConfigMap   #数据库配置文件映射
        self.get_mye_db_config()
        self.errorInfo=[]
        self.taskStatus=None
        self.ip=socket.gethostbyname(socket.gethostname())   #获取本机IP
        self.paramMap,self.errorCodeMap,self.machineName=self.getParamValue()   #获取RPA配置表,错误码映射表,机器名称
        self.toUser=self.paramMap.get("framework-python-toUser")
        #self.createCa()      #下载CA
        self.createLoger()  # 创建日志
        self.createUbDbConnect()  # 创建UB数据库长连接并获取当前任务信息
        self.human_behavior_flag=human_flag   #是否模拟人类行为
        #self.createDriver()  #创建selenium驱动
        self.ubLogInfo(2, "框架初始化完成")

    def get_mye_db_config(self):
        suffix_map={
            0:"prepare",
            1:"produce",
            2:"test",
        }
        suffix_name=f"mye_database_{suffix_map.get(self.submit)}"
        info=self.dbConfigMap.get(suffix_name)
        self.mye_host = info.get("host")
        self.mye_port = info.get("port")
        self.mye_dbUser = info.get("username")
        self.mye_dbPsd = info.get("password")
        self.mye_database = info.get("database")

    def imitate_human_behavior(self):
        """设置本次任务为模拟人类行为"""
        self.human_behavior_flag=True

    def timer_decorator(self,time):
        def actual_decorator(func):
            @wraps(func)
            @func_set_timeout(time)
            def wrapper(*args, **kwargs):
                print(f"{func}开始执行")
                result = func(*args, **kwargs)
                print(f"{func}结束执行")
                return result
            return wrapper
        return actual_decorator

    def get_error_message_map(self, carrier, b_type):
        with MySQLDataBase(self.host, self.port, self.dbUser, self.dbPsd, self.database) as myRPADB:
            cursor = myRPADB.cursor()
            sql = f"select * from T00_SYS_00_B_ERROR_MESSAGE_MAP where carrier='{carrier}' and b_type='{b_type}'"
            cursor.execute(sql)
            res = cursor.fetchall()
        self.error_message_map = {item.get("error_code"): {"cn": item.get("message"), "en": item.get("message_en"),"variable_map": json.loads(item.get("variable_map"))} for item in res}

    def get_error_message(self, error_code, variable_map):
        """
        根据error_code 获取提前配置的错误描述信息
        :param error_code:  错误码
        :param variable_map: 变量名对应的字典   与数据库里配置的错误信息里的变量名一一对应 例如{"BOOKINGREQ_ID":"123","BOOKING_COMPANY":"234","ROUTE_CODE":"999"}
        :return:
        """
        error_info = self.error_message_map.get(error_code)
        if not error_info:
            return f'警告！未找到该错误码{error_code}'
        message = error_info.get("cn")
        message_en = error_info.get("en")
        db_variable_map = error_info.get("variable_map")
        if (not message) or (not message_en):
            return f'警告！未找到该错误码{error_code}的描述信息'
        error_message = f'f"""{message}\n\n\n{message_en}"""'
        """变量初始化赋值"""
        for key, value in db_variable_map.items():
            exec(f"global {key}\n{key}=None")
        """变量赋值"""
        for key, value in variable_map.items():
            exec(f"global {key}\n{key}='{value}'")
        error_message = eval(error_message)
        return error_message

    def sendEmailWithFile(self,ReceiveEmails,smtp_server,smtp_port,sender_email,sender_password,file,subject,body):
        """发送邮件 ReceiveEmails接收人列表 """

        try:

            with open(file, 'rb') as f:
                excel_data = f.read()

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            attachment = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            attachment.set_payload(excel_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(attachment)

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # 启动TLS加密（如果端口是587）
                # server.starttls()
                # 登录到你的邮箱账户
                server.login(sender_email, sender_password)
                # 发送邮件
                for item in ReceiveEmails:
                    msg['To'] = item
                    server.sendmail(sender_email, item, msg.as_string())
                    sleep(2)

            self.ubLogInfo(2, f"发送邮件成功")
        except Exception as e:
            self.ubLogInfo(1, f"参数  {str(e)}")
    def createUbDbConnect(self):
        print(f"self.taskId:  {self.taskId}")
        if self.taskId==0:
            return
        sleep(2)
        """创建UB数据库长连接"""
        self.ubDbConnect = pymysql.connect(host=self.ub_host , port=self.ub_port, user=self.ub_username, password=self.ub_password, database=self.ub_database,cursorclass=DictCursor)
        """根据任务ID 获取当前tbl_cmd_task_execute_log 日志信息"""
        cursor = self.ubDbConnect.cursor()
        sql=f"select flow_id,worker_id from tbl_cmd_task where task_id='{self.taskId}'"
        cursor.execute(sql)
        res=cursor.fetchone()

        sql = f"SELECT * FROM tbl_cmd_task_execute_log WHERE task_id='{self.taskId}' ORDER BY id limit 1"
        cursor.execute(sql)
        res_log = cursor.fetchone()
        if not res_log:
            task_id=self.taskId
            create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            level=2
            worker_id=res.get("worker_id")
            flow_id=res.get("flow_id")
            content="新建任务"
            company_id="2"
            client_time=1691993781881
            flow_char_id='uibot3b751f8fea9abc'
            video_time=15537
            sql="insert into tbl_cmd_task_execute_log(task_id,create_time,`level`,worker_id,flow_id,content,company_id,client_time,flow_char_id,video_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params=[task_id,create_time,level,worker_id,flow_id,content,company_id,client_time,flow_char_id,video_time]
            cursor.execute(sql,params)
            self.ubDbConnect.commit()

        sql = f"SELECT * FROM tbl_cmd_task_execute_log WHERE task_id='{self.taskId}' ORDER BY id limit 1"
        cursor.execute(sql)
        res = cursor.fetchone()



        microsecond=int(res.get("create_time").microsecond/1000)
        self.taskCreateTime= (res.get("create_time") + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        self.taskCreateTime=f"{self.taskCreateTime}.{str(microsecond)}"
        self.taskLevel=res.get("level")
        self.taskWorkerId=res.get("worker_id")
        self.taskFlowId=res.get("flow_id")
        self.taskCompanyId=res.get("company_id")
    def ubLogInfo(self,level,content):
        """日志记录进UB表   日志级别(1 Trace  2 Info 3 Warn 4 Error)"""
        map = {
            1: "debug",
            2: "info",
            3: "warn",
            4: "error",
        }
        methodName = map.get(level)
        method = getattr(self.logger, methodName)
        method(content)

        if self.taskId == 0:
            """日志记录在本地"""
            return
        task_id=self.taskId
        now = datetime.datetime.now() - datetime.timedelta(hours=8)
        now2 = datetime.datetime.now()
        timestamp = now2.timestamp()*1000000
        timestamp=int(str(timestamp)[0:13])
        create_time = now
        level=level
        if not self.taskWorkerId:
            return
        worker_id=self.taskWorkerId
        flow_id=self.taskFlowId
        content=content
        company_id=self.taskCompanyId
        client_time=timestamp
        flow_char_id='1111'
        video_time='110'
        params=[task_id,create_time,level,worker_id,flow_id,content,company_id,client_time,flow_char_id,video_time]
        cursor = self.ubDbConnect.cursor()
        sql = f"INSERT INTO tbl_cmd_task_execute_log(task_id,create_time,level,worker_id,flow_id,content,company_id,client_time,flow_char_id,video_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,params)
        self.ubDbConnect.commit()

    def installDriver(self):
        from webdriver_manager.chrome import ChromeDriverManager
        """判断是否需要下载driver"""

        """找到本机谷歌浏览器版本"""
        """C:\Program Files\Google\Chrome\Application\122.0.6261.112   找到名字为版本号的文件夹"""
        dirPath = r'C:\Program Files\Google\Chrome\Application'
        version = '122.0.6261.112'

        try:
            for item in os.listdir(dirPath):
                if re.search(r'\d{3}.\d.\d{4}.\d{1,3}', item):
                    version = re.search(r'\d{3}.\d.\d{4}.\d{1,3}', item).group(0)
                    break
        except Exception as e:
            self.ubLogInfo(2, str(e))
            dirPath = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application"
            for item in os.listdir(dirPath):
                if re.search(r'\d{3}.\d.\d{4}.\d{1,3}', item):
                    version = re.search(r'\d{3}.\d.\d{4}.\d{1,3}', item).group(0)
                    break

        username = getpass.getuser()
        # 遍历文件夹下所有driver版本   前三位参与比较  第四位不参与比较
        driverDirPath = f"""C:\\Users\\{username}\\.wdm\\drivers\\chromedriver\\win64"""
        version_s = re.search(r'(\d{3}.\d.\d{1,4}).\d{1,3}', version).group(1)
        driver_path = None
        for item in os.listdir(driverDirPath):
            if version_s in item:
                driver_path = f"""C:\\Users\\{username}\\.wdm\\drivers\\chromedriver\\win64\\{item}\\chromedriver-win32\\chromedriver.exe"""
                break

        if not driver_path:
            driver_path = ChromeDriverManager().install()
            driver_path = driver_path.replace("THIRD_PARTY_NOTICES.", "")
            driver_path = f"{driver_path}.exe"
        return driver_path

    def getIdentifyCodeByPicBase64(self, username,password,pic):
        """解析图片验证码 图片base64编码   chaojiyingUser  chaojiyingPassWord """
        chaojiying = Chaojiying_Client(username, password, "945982")
        result = chaojiying.PostPic_base64(pic, "1902")
        self.picResult = result
        return result.get("pic_str", "0000")

    def getIdentifyBySlider(self, username,password,pic):
        """解析滑块   图片base64编码"""
        # pic = pic.split("base64,")[1]
        chaojiying = Chaojiying_Client(username, password, "945982")
        result = chaojiying.PostPic_base64(pic, "9101")
        self.picResult = result
        res = result.get("pic_str", "100,100")
        if '|' in res and ',' in res:
            res1 = (res.split("|")[1])
            x = int(res1.split(",")[0])
            y = int(res1.split(",")[1])
        elif "," in res:
            x = int(res.split(",")[0])
            y = int(res.split(",")[1])
        elif "|" in res:
            x = int(res.split("|")[0])
            y = int(res.split("|")[1])
        else:
            x = 122
            y = 221
        return x, y

    def reportErrorByChaoJiYin(self,username,password):
        """超级鹰识别报错"""
        chaojiying = Chaojiying_Client(username, password, "945982")
        chaojiying.ReportError(self.picResult.get("pic_id"))



    def createDriver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        options = {
            "ca_cert": "C:\\tools\\00401_MSK\\ca.crt",
            "ca_key": "C:\\tools\\00401_MSK\\ca.key",
        }
        driver_path=self.installDriver()
        op = webdriver.ChromeOptions()
        # op.add_argument('headless')
        op.add_argument('disable-infobars')
        op.add_argument('--ignore-certificate-errors')
        op.add_argument('--allow-insecure-localhost')
        op.add_argument('-ignore -ssl-errors')
        op.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以键值对的形式加入参数
        prefs = {"profile.default_content_settings.popups": 1}
        op.add_experimental_option('prefs', prefs)
        script = '''
                                        Object.defineProperty(navigator, 'webdriver', {
                                            get: () => undefined
                                        })
                                        '''
        self.driver = webdriver.Chrome(service=Service(driver_path), options=op)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.driver.execute_script(script)
        script = '''
                                                Object.defineProperty(navigator, 'plugins', {
                                                    get: () => 2
                                                })
                                                '''
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.driver.set_page_load_timeout(60)
    def createLoger(self):

        if not os.path.exists("C:\\tools"):
            os.mkdir("C:\\tools")
        file = f"C:\\tools\\{self.taskId}"
        if not os.path.exists(file):
            os.mkdir(file)
        now=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        log_path = os.path.join(file, f'{now}log.txt')
        handler = TimedRotatingFileHandler(log_path,
                                           when="midnight",
                                           interval=1,
                                           backupCount=5, encoding='utf-8')
        logging.basicConfig(format='[%(asctime)s-%(levelname)s-%(filename)s:%(lineno)s   %(message)s]',
                            level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S', handlers=[handler, logging.StreamHandler()])
        self.logger = logging
    def createCa(self):
        if not os.path.exists("C:\\tools"):
            os.mkdir("C:\\tools")
        localPath = "C:\\tools\\00401_MSK"
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        remotePath = "task00401/msk/"
        filenameKEY = "ca.key"
        filenameCRT = "ca.crt"
        res = json.loads(self.paramMap.get("FTP_INFO"))
        HOST = res.get("host")
        user = res.get("user")
        passwd = res.get("password")
        ftp = myFTP(HOST, user, passwd)
        ftp.downloadFile(localPath, remotePath, filenameKEY)
        sleep(3)
        ftp = myFTP(HOST, user, passwd)
        ftp.downloadFile(localPath, remotePath, filenameCRT)
    def getParamValue(self):
        """获取RPA参数表"""
        with MySQLDataBase(self.host, self.port, self.dbUser, self.dbPsd, self.database) as myRPADB:
            cursor = myRPADB.cursor()
            sql = f"SELECT * FROM T01_BUSI_PARAM"
            cursor.execute(sql)
            res = cursor.fetchall()

            sql="SELECT * FROM T00_SYS_00_ERROR_CODE_MAP"
            cursor.execute(sql)
            res1 = cursor.fetchall()

            sql = f"SELECT * FROM T00_SYS_00_MACHINE_NAME WHERE MACHINE_IP='{self.ip}'"
            cursor.execute(sql)
            res2 = cursor.fetchone()
        if res2:
            machineName=res2.get("MACHINE_NAME",self.ip)
        else:
            machineName=self.ip

        """解析配置表"""
        paramMap={}
        for item in res:
            key=item.get("PARAM_KEY")
            value=item.get("PARAM_VALUE")
            paramMap[key]=value
        codeMap={}
        for item in res1:
            key = item.get("ERROR_CODE")
            value = item.get("ERROR_TYPE")
            codeMap[key] = value
        return paramMap,codeMap,machineName
    def download(self,localPath, remotePath, filename):
        download(localPath, remotePath, filename)
    def getDBConfig_RPA(self):
        """

        :param submit: submit:0 预发  1 生产  2 测试
        :return:
        """
        submit=self.submit
        # 从FTP获取生产测试数据库地址
        localPath = r"C:\tools\databaseConfig"
        remotePath = "databaseConfig/"
        fileName = "config.ini"
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        self.download(localPath, remotePath, fileName)
        dbConfig = f"{localPath}\\{fileName}"
        if not os.path.exists(dbConfig):
            raise Exception("配置表下载失败")
        config = configparser.ConfigParser()
        # 读取INI文件
        config.read(dbConfig, encoding="utf-8")
        # 获取指定section中的值

        pro_host = config.get('database_produce', "host")
        pro_port = int(config.get('database_produce', "port"))
        pro_username = config.get('database_produce', "username")
        pro_password = config.get('database_produce', "password")
        pro_database = config.get('database_produce', "database")

        test_host = config.get('database_test', "host")
        test_port = int(config.get('database_test', "port"))
        test_username = config.get('database_test', "username")
        test_password = config.get('database_test', "password")
        test_database = config.get('database_test', "database")


        ub_host=config.get('ub_database', "host")
        ub_port = int(config.get('ub_database', "port"))
        ub_username = config.get('ub_database', "username")
        ub_password = config.get('ub_database', "password")
        ub_database = config.get('ub_database', "database")

        """读取所有配置文件返回 """
        dbConfigMap={}
        sections=config.sections()
        for sectionName in sections:
            host=config.get(sectionName, "host")
            port=int(config.get(sectionName, "port"))
            username=config.get(sectionName, "username")
            password=config.get(sectionName, "password")
            database=config.get(sectionName, "database")
            dbConfigMap[sectionName]={"host":host,"port":port,"username":username,"password":password,"database":database}

        if submit == 1:
            return pro_host, pro_port, pro_username, pro_password, pro_database,ub_host,ub_port,ub_username,ub_password,ub_database,dbConfigMap
        elif submit == 0:
            return test_host, test_port, test_username, test_password, test_database,ub_host,ub_port,ub_username,ub_password,ub_database,dbConfigMap
        elif submit == 2:
            return test_host, test_port, test_username, test_password, test_database,ub_host,ub_port,ub_username,ub_password,ub_database,dbConfigMap
        else:
            raise Exception("submit error")
    def report(self,process_id, task_id, busi_record_id, error_level, error_code, error_desc, exe_machine, toUser):
        """
        :param envType: 区分生产测试      1：生产  0：测试
        :param task_id: 流程ID
        :param process_id: 任务ID
        :param busi_record_id: 业务任务ID
        :param error_level: 错误危机程度      1:紧急     2:重要     3:普通
        :param error_code:错误码
        :param error_desc:错误描述
        :param exe_machine:执行机器   可传机器码  可传IP
        :param toUser: 错误通知人   多个则用|分割   A|B|C
        :return:
        """
        errorLevelMap = {
            1: "紧急",
            2: "重要",
            3: "普通",
        }


        # 有业务任务ID用业务任务ID 没有就用任务ID
        if busi_record_id is None or busi_record_id == "":
            busi_record_id = process_id

        """错误入库"""
        exe_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with MySQLDataBase(self.host, self.port, self.dbUser, self.dbPsd, self.database) as myRPADB:
            cursor = myRPADB.cursor()
            # 获取默认消息接收人
            sql = 'select * from T01_BUSI_PARAM'
            cursor.execute(sql)
            list_param = cursor.fetchall()
            config = {item['PARAM_KEY']: item['PARAM_VALUE'] for item in list_param}

            # exe_machine匹配成MACHINE_NAME
            res = re.findall('\d+\.\d+\.\d+\.\d+', exe_machine)
            sql = "select * from T00_SYS_00_MACHINE_NAME"
            cursor.execute(sql)
            list_machine = cursor.fetchall()
            if len(res) > 0:
                # exe_machine是IP
                dict_machine_ip = {item['MACHINE_IP']: item['MACHINE_NAME'] for item in list_machine}
                machine_name = dict_machine_ip.get(exe_machine, '未知IP')
            else:
                # exe_machine是machine_code
                dict_machine_code = {item['MACHINE_CODE']: item['MACHINE_NAME'] for item in list_machine}
                machine_name = dict_machine_code.get(exe_machine, '未知机器码')

            if error_code == '200000':
                sql = "UPDATE T00_SYS_00_ERROR_TASK_INFO SET FINAL_STATUS='SUCCESS' WHERE BUSI_RECORD_ID=%s"
                params = [busi_record_id]
                cursor.execute(sql, params)
                myRPADB.commit()
            else:
                id = uuid.uuid1().hex
                # FINAL_STATUS = None
                sql = "insert into T00_SYS_00_ERROR_TASK_INFO(ID,TASK_ID,PROCESS_ID,BUSI_RECORD_ID,ERROR_CODE,ERROR_DESC,EXE_TIME,EXE_MACHINE,ERROR_LEVEL) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = [id, task_id, process_id, busi_record_id, error_code, error_desc, exe_time,
                          machine_name, errorLevelMap.get(error_level)]
                cursor.execute(sql, params)
                myRPADB.commit()
                """发送消息通知"""
                wechat = WinxinApi(config.get('corpid_me'), config.get('corpsecret_me'), config.get('agentId_me'),
                                   toUser)
                if error_level == 1:
                    if toUser:
                        wechat.send_message(toUser, "", errorLevelMap.get(error_level), error_code, error_desc, task_id,
                                            process_id,
                                            busi_record_id, machine_name)
                    wechat.send_message_group("RPAEmergencyProblemGroup", errorLevelMap.get(error_level), error_code,
                                              error_desc,
                                              task_id, process_id, busi_record_id, machine_name)
    def send_message(self,toUser, toTag, toGroup, message, filePath):
        # 有业务任务ID用业务任务ID 没有就用任务ID
        with MySQLDataBase(self.host, self.port, self.dbUser, self.dbPsd, self.database) as myRPADB:
            cursor = myRPADB.cursor()
            # 获取默认消息接收人
            sql = 'select * from T01_BUSI_PARAM'
            cursor.execute(sql)
            list_param = cursor.fetchall()
            config = {item['PARAM_KEY']: item['PARAM_VALUE'] for item in list_param}
            wechat = WinxinApi(config.get('corpid_me'), config.get('corpsecret_me'), config.get('agentId_me'), toUser,
                               toTag, toGroup)
            if message:
                if toUser or toTag:
                    wechat.send_message_common(message)
                if toGroup:
                    wechat.send_message_group_common(message)
            if filePath and (toTag or toGroup or toUser):
                wechat.send_file_message(filePath)
            cursor.close()
    def send_message_with_img(self,toUser, toTag, toGroup, message, filePath):
        # 有业务任务ID用业务任务ID 没有就用任务ID
        with MySQLDataBase(self.host, self.port, self.dbUser, self.dbPsd, self.database) as myRPADB:
            cursor = myRPADB.cursor()
            # 获取默认消息接收人
            sql = 'select * from T01_BUSI_PARAM'
            cursor.execute(sql)
            list_param = cursor.fetchall()
            config = {item['PARAM_KEY']: item['PARAM_VALUE'] for item in list_param}
            wechat = WinxinApi(config.get('corpid_me'), config.get('corpsecret_me'), config.get('agentId_me'), toUser,
                               toTag, toGroup)
            if message:
                if toUser or toTag:
                    wechat.send_message_common(message)
                if toGroup:
                    wechat.send_message_group_common(message)
            if filePath and (toTag or toGroup or toUser):
                wechat.send_img_message(filePath)
            cursor.close()
    def setTaskResult(self,result:str):
        """任务结果数据外带进来   """
        """设置任务结果"""
        if self.taskId==0:
            return

        # result={"RUN_COUNT":RUN_COUNT,"SUCCESS_COUNT":SUCCESS_COUNT,"ERROR_RATE":ERROR_RATE}
        # result=json.dumps(result)


        cursor = self.ubDbConnect.cursor()
        sql="UPDATE tbl_cmd_task_ext SET task_external_result=%s WHERE task_id=%s"
        params=[result,self.taskId]
        cursor.execute(sql,params)
        self.ubDbConnect.commit()
        self.ubLogInfo(2, f"设置任务结果 {result}")

    def judge_human_behavior(self):
        """如果本次任务设定 模拟人类行为   则 判断当前时间是否满足人类正常作息时间  从而判断是否继续执行"""
        flag=True
        if self.human_behavior_flag:
            now = datetime.datetime.now()
            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start = today + datetime.timedelta(hours=8)
            end = today + datetime.timedelta(hours=19)
            start_1 = today + datetime.timedelta(hours=12)
            end_1 = today + datetime.timedelta(hours=13)
            hour = now.hour
            if now >= start and now <= end:
                if now >= start_1 and now <= end_1:
                    flag=False
            else:
                flag=False
        return flag

    @abc.abstractmethod
    def doTask(self):
        pass
    def reportRrror(self):
        if self.errorInfo:
            bussineInfo=None
            if self.args:
                bussineInfo=self.args
            message=f"  机器:{self.machineName}\n  流程:{self.flowName}\n"
            message+='\n'
            message+='\n'
            for item in self.errorInfo:
                message+=f"第{item.get('errorTimes')+1}次\n"
                message+=f"  任务id： {self.taskId}\n"
                message+=f"  业务信息: {bussineInfo}\n"
                message+=f"  时间: {item.get('time')}\n"
                message+=f"  错误: {item.get('message')}\n"
            self.report(self.flowName,self.taskId,None,2,'300000',message,self.machineName,None)
            self.send_message(self.toUser,None,None,message,None)

    def run(self):
        while self.errorTime<self.retryTimes and self.taskStatus is None:
            try:
                if self.judge_human_behavior():   #判断是否在可执行的时间范围之内
                    self.doTask = self.timer_decorator(self.maxTimeOut)(self.doTask)
                    self.doTask()
                else:
                    self.ubLogInfo(2, '因设置模拟人类行为，当前时间不满足人类正常作息，故任务停止')
            except FunctionTimedOut as e:
                errorMessage = f"doTask方法执行超时 最大执行时间 {self.maxTimeOut}秒"
                self.ubLogInfo(2, errorMessage)
                error = {
                    "errorTimes": self.errorTime,
                    "machine": self.machineName,
                    "flow": self.flowName,
                    "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "message": errorMessage,
                }
                self.errorInfo.append(error)
                self.errorTime += 1
            except Exception as e:
                errorMessage = str(e) + '\n' + traceback.format_exc()
                self.ubLogInfo(2,errorMessage)
                error={
                    "errorTimes":self.errorTime,
                    "machine":self.machineName,
                    "flow":self.flowName,
                    "time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "message":errorMessage,
                }
                self.errorInfo.append(error)
                self.errorTime+=1
            else:
                self.taskStatus='SUCCESS'
                self.ubLogInfo(2,"任务SUCCESS")
        self.reportRrror()
        self.release()
    def release(self):
        if self.driver:
            self.driver.quit()
            self.driver=None
        if self.ubDbConnect and self.ubDbConnect.open:
            self.ubDbConnect.close()
            self.ubDbConnect=None





class RpaRobbt(Robot):
    def __init__(self,taskId,retryTimes,submit,flowName,maxTimeOut,human_flag,args):
        super(RpaRobbt,self).__init__(taskId,retryTimes,submit,flowName,maxTimeOut,human_flag)

        """"""
        self.createDriver()  # 创建selenium驱动
        self.args=args                #业务参数   此处接收你从ub带过来的本次任务的业务参数
        self.loginUrl=self.args.get("param_1")
        self.param1=self.args.get("param_2")


    def doTask(self):
        """重写此方法   主要业务逻辑处   """
        self.logger.info(f"任务ID:{self.taskId}")
        self.logger.info(f"重试次数:{self.retryTimes}")
        self.logger.info(f"环境:{self.submit}")
        self.logger.info(f"业务参数:{self.args}")
        self.ubLogInfo(2,"开始执行")
        self.ubLogInfo(2,f"登录地址 {self.loginUrl}")
        self.ubLogInfo(2,f"参数  {self.param1}")

        self.driver.get("https://blog.csdn.net/qq_48441158?type=blog")
        sleep(1)
        self.driver.close()







def getParams(taskID):
    """
    :param submit: submit:0 预发  1 生产  2 测试
    :return:
    """
    """获取流程参数"""

    """获取CMD数据库配置信息"""
    # 从FTP获取生产测试数据库地址
    localPath = r"C:\tools\databaseConfig"
    remotePath = "databaseConfig/"
    fileName = "config.ini"
    if not os.path.exists(localPath):
        os.mkdir(localPath)
    download(localPath, remotePath, fileName)
    dbConfig = f"{localPath}\\{fileName}"
    if not os.path.exists(dbConfig):
        raise Exception("配置表下载失败")
    config = configparser.ConfigParser()
    # 读取INI文件
    config.read(dbConfig, encoding="utf-8")
    ub_host = config.get('ub_database', "host")
    ub_port = int(config.get('ub_database', "port"))
    ub_username = config.get('ub_database', "username")
    ub_password = config.get('ub_database', "password")
    ub_database = config.get('ub_database', "database")
    with MySQLDataBase(ub_host, ub_port, ub_username, ub_password, ub_database) as myRPADB:
        cursor = myRPADB.cursor()
        sql = f"SELECT * FROM tbl_cmd_task_paramter where task_id='{taskID}'"
        cursor.execute(sql)
        res = cursor.fetchall()
    params={}
    for item in res:
        params[item.get('name')]=item.get("value")
    return params




def getUUid():
    return uuid.uuid1().hex


def doTask(taskId,retryTimes,submit,flowName,args):
    """
    :param taskId:  任务ID  必传
    :param retryTimes: 重试次数  必传  如果此流程错误无需重试  则为 1
    :param submit:  环境参数 必传     1：生产  0： 预生产   2： 测试
    :param flowName: 流程名称
    :param args: 位置参数    业务参数
    :return:
    """
    ip = socket.gethostbyname(socket.gethostname())
    robbot = None
    if not (taskId is not None and retryTimes and submit is not None and flowName):
        raise Exception('缺少必要参数')
    try:
        robbot=RpaRobbt(taskId,retryTimes,submit,flowName,args)
        robbot.run()
    except Exception as e:
        message=str(e) + '\n' + traceback.format_exc()
        report(1, flowName, taskId, None, 1, '300000', message, ip, "")
        if robbot:
            robbot.ubLogInfo(4,message)
        raise Exception(message)
    else:
        if robbot.taskStatus!='SUCCESS':
            raise Exception("任务执行失败")
    finally:
        if robbot and hasattr(robbot,'driver') and robbot.driver:
            robbot.driver.quit()
        if robbot and hasattr(robbot,'ubDbConnect') and robbot.ubDbConnect and robbot.ubDbConnect.open:
            robbot.ubDbConnect.close()

def get_private_ips():
    ip_address = ''
    try:
        # 获取网络接口列表
        interfaces = netifaces.interfaces()
        # 查找第一个非本地回环接口的IP地址
        for interface in interfaces:
            if interface == 'lo':
                continue
            addresses = netifaces.ifaddresses(interface)
            ip_addresses = addresses.get(netifaces.AF_INET)
            if ip_addresses:
                ip_address = ip_addresses[0]['addr']
                break
    except:
        pass
    return ip_address

def doTaskByexe(taskID):
    """
    :param taskId:  任务ID  必传
    :param retryTimes: 重试次数  必传  如果此流程错误无需重试  则为 1
    :param submit:  环境参数 必传     1：生产  0： 预生产   2： 测试
    :param flowName: 流程名称
    :param args: 位置参数    业务参数
    :return:
    """
    ip = get_private_ips()
    robbot = None
    res = None
    taskId = None
    retryTimes = None
    flowName = None
    args = [None,None]
    try:
        #根据taskID获取库里的参数
        params=getParams(taskID)
        taskId=taskID
        retryTimes=int(params.get("retryTimes",1))
        flowName=params.get("flowName","未知流程")
        submit=int(params.get("submit",1))
        human_flag=(params.get("human_flag",False))   #是否模拟人类行为
        try:
            maxTimeOut=int(params.get("maxTimeOut",120))*60
        except:
            maxTimeOut=120*60
        #maxTimeOut=20
        robbot=RpaRobbt(taskId,retryTimes,submit,flowName,maxTimeOut,human_flag,params)
        robbot.run()
    except Exception as e:
        message=str(e) + '\n' + traceback.format_exc()
        #report(1, flowName, taskId, None, 1, '300000', message, ip, "")
        if robbot:
            robbot.ubLogInfo(4,message)
        print(message)
    else:
        if robbot.taskStatus!='SUCCESS':
            print("任务执行失败")
        else:
            print("SUCCESS")
    finally:
        if robbot and hasattr(robbot,'driver') and robbot.driver:
            robbot.driver.quit()
        if robbot and hasattr(robbot,'ubDbConnect') and robbot.ubDbConnect and robbot.ubDbConnect.open:
            robbot.ubDbConnect.close()




if __name__=="__main__":

    """新版框架----"""
    #  打包命令  ：pyinstaller -F -w pythonRpaFrameworkNew.py
    #参数表变字典
    #taskId=0（本地执行任务）    则日志功能写到本地   否则写入UB库   1
    #优化UB数据库没有及时生成task_id的信息导致报错    1
    #快速pip环境包
    #判断selnium是否已存在     1
    #优化设置任务结果方法参数由用户指定    1
    #doTask(0,3,1,"Task03601华东外运邮件获取-框架测试",["kk",'https://blog.csdn.net/qq_48441158?spm=1010.2135.3001.5343'])


    """新版框架   传递任务id taskID   去"""
    #taskID=sys.argv[1]
    taskID='3948915355287553'


    doTaskByexe(taskID)
    #xxxrobbot=RpaRobbt(1)


    #新增发送邮件入口
    #优化获取本地IP
    #6.27 新增任务最大超时时间 maxTimeOut   单位为分钟    默认120分钟

