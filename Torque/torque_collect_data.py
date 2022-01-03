import Module.export_data as Exdata
import Module.mine_data as Data  
import pandas as pd 
from datetime import datetime, timedelta

sqlScript = r"SqlScripts/TorqueData.sql"
databaseName = 'ModuleAssembly' 
sqlServer1 = 'dmt1messqlods' 
sqlServer2 = 'dmt2messqlods' 

# Create data csv
totalDay = 14
step = 12
totalSample = (totalDay * 24 / step) 
i = 1 

datenow = datetime.now().replace(microsecond=0, second= 0, minute= 0)
if datenow.hour >= 18:
  dstop = datenow.replace(hour=18)
else:
  dstop = datenow.replace(hour=6)

dmt1_lastestData = pd.DataFrame()
dmt2_lastestData = pd.DataFrame()
while i < totalSample:
  dstop1 = dstop - timedelta(hours=step*i)
  dstart1 = dstop - timedelta(hours=step*(i+1)) 
  resultDmt1 = Data.getData(sqlServer1, databaseName, sqlScript, dstart1, dstop1)
  resultDmt2 = Data.getData(sqlServer2, databaseName, sqlScript, dstart1, dstop1)
  data1, timeData1, temp1 = Exdata.export_day_data('./Data/DMT1/', resultDmt1, dstop1)
  data2, timeData2, temp2 = Exdata.export_day_data('./Data/DMT2/', resultDmt2, dstop1)
  dmt1_lastestData = dmt1_lastestData.append(data1, ignore_index=True)
  dmt2_lastestData = dmt2_lastestData.append(data2, ignore_index=True)
  i = i + 1 
  print(timeData1, temp1, timeData2, temp2)
dmt1_lastestData.to_csv('./Data/DMT1/lastestData.csv')
dmt2_lastestData.to_csv('./Data/DMT2/lastestData.csv')