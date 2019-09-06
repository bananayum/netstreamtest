
import csv
import pymysql
'''异常单流特征库，判断异常单流类型'''
def singleanomaly(srcip,desip,srcport,desport,protocol,packbytes):
    if packbytes=='48' and desport=='135' and protocol=='6':
        atype='冲击波病毒攻击'
        return atype
    elif srcip=='255.255.255.255' and protocol=='17':
        atype='Fraggle攻击'
        return atype
    elif srcip==desip and srcport==desport and protocol=='6':
        atype='Land攻击'
        return atype
    elif srcip=='127.0.0.1' or srcip=='0.0.0.0':
        atype='非法源地址攻击'
        return atype
    elif packbytes=='144' and desport=='80' and protocol=='80':
        atype='红色代码'
        return atype
    elif srcip=='255.255.255.255' and protocol=='1':
        atype='Smuff攻击'
        return atype
    elif packbytes=='376' and desport=='1433':
        atype='SQL-Slammer攻击'
        return atype
'''读取网络流.csv文件，将异常单流存入数据库'''
def single(b):
    db=pymysql.connect("localhost","root","123456","flowdata",charset="UTF8")
    cursor=db.cursor()
    filename=b

    with open(filename) as f:
        reader=csv.reader(f)
        her=next(reader)

        for row in reader:
            srcip=row[3]
            srcport=row[4]
            desip=row[5]
            desport=row[6]
            protocol=row[8]
            packets=int(row[9])
            byte=int(row[10])
            if packets!=0:
                packbytes=str(int(byte/packets))
            else:
                packbytes='0'
            anomaltype=singleanomaly(srcip,desip,srcport,desport,protocol,packbytes)
            if anomaltype!=None:
                a=str(row[2])
                b=str(row[3])
                c=str(row[5])
                d=str(anomaltype)
                sql="INSERT INTO ANOMALYTYPE(异常发生时间,异常流量源地址,异常流量目的地址,异常流量类型) VALUES('%s','%s','%s','%s')" %(a,b,c,d)
                cursor.execute(sql)
                db.commit()

    db.close()

