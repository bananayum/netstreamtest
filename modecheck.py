import csv
import pymysql
from datetime import datetime
def mode(b):
    filename=b
    db=pymysql.connect("localhost","root","123456","flowdata",charset="UTF8")
    cursor=db.cursor()
    # cursor.execute("DROP TABLE IF EXISTS ANOMALYTYPE")
    # sql="""CREATE TABLE ANOMALYTYPE(异常发生时间 CHAR(64) NOT NULL,异常流量源地址 CHAR(64),异常流量目的地址 CHAR(64),异常流量类型 CHAR(64))"""
    # cursor.execute(sql)

    def srcipcheck(nowhshs):
        hangshuaa=nowhshs
        with open(filename) as f1:
            reader1 = csv.reader(f1)
            ii=0
            while ii<hangshuaa:
                next(reader1)
                ii=ii+1
            srcip=[]
            for row in reader1:
                if row[3] not in srcip:
                    srcip.append(row[3])
            for rows in srcip:
                a=rows
                desip=[]
                srcport=[]
                desport=[]
                with open(filename) as fs1:
                    readers1 = csv.reader(fs1)
                    ii = 0
                    while ii < hangshuaa:
                        next(readers1)
                        ii = ii + 1
                    for row in readers1:
                        if row[3]==a:
                            if row[4] not in srcport:
                                srcport.append(row[4])
                            if row[6] not in desport:
                                desport.append(row[6])
                            if row[5] not in desip:
                                desip.append(row[5])
                    if len(desip)>=10:
                        if len(desport)<3 and len(srcport)<3:
                            with open(filename) as f11:
                                reader11 = csv.reader(f11)
                                iii = 0
                                while iii < hangshuaa:
                                    next(reader11)
                                    iii = iii + 1
                                for row1 in reader11:
                                    if rows==row1[3]:
                                        anomalytime=row1[2]
                                        ano=str(anomalytime)
                                        break
                                sql = "INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" % (ano, rows, '', '针对网络的端口扫描')
                                cursor.execute(sql)
                                db.commit()
                        if len(desport)<3 and len(srcport)>30:
                            with open(filename) as f11:
                                reader11 = csv.reader(f11)
                                iii = 0
                                while iii < hangshuaa:
                                    next(reader11)
                                    iii = iii + 1
                                for row1 in reader11:
                                    if rows==row1[3]:
                                        anomalytime=row1[2]
                                        ano=str(anomalytime)
                                        break
                                sql = "INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" % (ano, rows, '', '多线程下载')
                                cursor.execute(sql)
                                db.commit()
                        if 3<len(desport)<20 and 3<len(srcport)<30:
                            with open(filename) as f11:
                                reader11 = csv.reader(f11)
                                iii = 0
                                while iii < hangshuaa:
                                    next(reader11)
                                    iii = iii + 1
                                for row1 in reader11:
                                    if rows==row1[3]:
                                        anomalytime=row1[2]
                                        ano=str(anomalytime)
                                        break
                                sql = "INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" % (ano, rows, '', '蠕虫病毒传播')
                                cursor.execute(sql)
                                db.commit()


    def desipcheck(nowhshs):
        hangshuaa = nowhshs
        with open(filename) as f2:
            reader2 = csv.reader(f2)
            ii = 0
            while ii < hangshuaa:
                next(reader2)
                ii = ii + 1
            desip=[]
            for row in reader2:
                if row[5] not in desip:
                    desip.append(row[5])

            for rows in desip:
                a=rows
                srcip=[]
                srcport=[]
                desport=[]
                tcplink=0
                with open(filename) as fs2:
                    readers2 = csv.reader(fs2)
                    ii = 0
                    while ii < hangshuaa:
                        next(readers2)
                        ii = ii + 1
                    for row in readers2:
                        if row[5]==a:
                            if row[6] not in desport:
                                desport.append(row[6])
                            if row[3] not in srcip:
                                srcip.append(row[6])
                            if row[8]=='6':
                                tcplink=tcplink+1
                    '''根据相同目的IP地址聚合异常网络流判断'''
                    if len(srcip)<3 and len(desport)>20:
                        '''判断针对主机的端口扫描异常，判断条件为源IP小于3，目的端口大于20'''
                        with open(filename) as f22:
                            reader22 = csv.reader(f22)
                            iii = 0
                            while iii < hangshuaa:
                                next(reader22)
                                iii = iii + 1
                            for row2 in reader22:
                                if rows==row2[5]:
                                    anomalytime=row2[2]
                                    ano=str(anomalytime)
                                    break
                            '''将异常结果写入异常数据库'''
                            sql = "INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" % (ano, '', rows, '针对主机的端口扫描')
                            cursor.execute(sql)
                            db.commit()
                    if len(desport)<3 and tcplink>20:
                        '''判断DDoS攻击异常，判断条件为目的端口小于3，TCP连接数大于20'''
                        with open(filename) as f22:
                            reader22 = csv.reader(f22)
                            iii = 0
                            while iii < hangshuaa:
                                next(reader22)
                                iii = iii + 1
                            for row2 in reader22:
                                if rows==row2[5]:
                                    anomalytime=row2[2]
                                    ano=str(anomalytime)
                                    break
                            sql = "INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" % (ano, '', rows, 'DDos攻击')
                            cursor.execute(sql)
                            db.commit()


    with open(filename) as ft:
        readert=csv.reader(ft)
        next(readert)
        st=1
        for rowt in readert:
            if rowt[0]!=None:
                st=st+1
    with open(filename) as f:
        reader=csv.reader(f)
        next(reader)
        a=next(reader)
        starttime=datetime.strptime(a[2], "%Y/%m/%d %H:%M:%S")
        flows = 1
        allpackage = int(a[9])
        allbyte = int(a[10])
        tempbyte=0
        temppackage=0
        nowhangshu=2
        nowhshs=0
        nowtime=None
        while nowhangshu<st:
            i=0
            for row in reader:
                i = i + 1
                nowtime = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
                tmaa=nowtime-starttime
                if int(tmaa.seconds)>=1800:
                    temppackage=int(row[9])
                    tempbyte=int(row[10])
                    break
                flows = flows + 1
                allpackage = allpackage + int(row[9])
                allbyte = allbyte + int(row[10])

            if flows != 0:
                avrpackage = allpackage / flows
                avrbyte = allbyte / flows
            else:
                avrbyte, avrpackage = 0, 0

            if flows >= 100 and avrbyte <= 64 and avrpackage <= 2:
                srcipcheck(nowhshs)
                desipcheck(nowhshs)
            starttime = nowtime
            flows=1
            allpackage=temppackage
            allbyte=tempbyte
            nowhangshu=i+nowhangshu
            nowhshs = nowhshs + i

    db.close()
