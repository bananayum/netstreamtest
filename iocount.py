import csv
from matplotlib import pyplot as plt
from datetime import datetime

filename = 'flowtable.csv'
with open(filename) as f:
    reader = csv.reader(f)
    her = next(reader)

    src, des ,allsrcdes ,dates = [], [], [], []
    tempdatef=datetime.strptime(next(reader)[2], "%Y/%m/%d %H:%M:%S")
    tempbytes = 0

    for row in reader:
        nowdatef=datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
        if nowdatef.minute == tempdatef.minute:
            if row[4] not in src:
                src.append(row[4])
            if row[6] not in des:
                des.append(row[6])
        else:
            lensrc=len(src)
            lendes=len(des)
            if lendes==0:
                srcdes=0
            else:
                srcdes=lensrc/lendes
            allsrcdes.append(srcdes)
            dates.append(tempdatef)
            tempdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
            src,des=[],[]


fig = plt.figure(dpi=96, figsize=(12, 6))
plt.plot(dates, allsrcdes, c='blue')
plt.title("Network traffic display platform", fontsize=24)
fig.autofmt_xdate()
plt.xlabel('Time', fontsize=16)
plt.ylabel('Network traffic', fontsize=16)
plt.show()

