import csv
from matplotlib import pyplot as plt
from datetime import datetime

filename='flowtable.csv'
with open(filename) as f:
    reader=csv.reader(f)
    next(reader)

    dates,allbyte=[],[]
    tempdatef=datetime.strptime(next(reader)[2], "%Y/%m/%d %H:%M:%S")
    tempbytes=0

    for row in reader:
        nowdatef = datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
        if nowdatef.minute != tempdatef.minute:
            allbyte.append(tempbytes)
            dates.append(tempdatef)
            tempdatef=datetime.strptime(row[2], "%Y/%m/%d %H:%M:%S")
            tempbytes=int(row[10])
        else:
            tempbytes=tempbytes+int(row[10])

fig=plt.figure(dpi=96,figsize=(12,6))
plt.plot(dates,allbyte, c='blue')
plt.title("Network traffic display platform", fontsize=24)
fig.autofmt_xdate()
plt.xlabel('Time',fontsize=16)
plt.ylabel('Network traffic', fontsize=16)
plt.show()