# library debug
import logging 
import pandas as pd 
import os.path
from datetime import datetime
import Module.send_email as Email
import Module.mine_data as Data  
import Module.draw_chart as Chart
import Module.export_data as Exdata
from datetime import datetime, timedelta

sqlScript = r"SqlScripts/TorqueData.sql"
databaseName = 'ModuleAssembly' 
sqlServer1 = 'dmt1messqlods' 
sqlServer2 = 'dmt2messqlods' 

print("Start read the lastest data", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
dmt1_lastestData = pd.read_csv('./Data/DMT1/lastestData.csv', parse_dates=['Timestamp'])
dmt1_data= dmt1_lastestData.drop(dmt1_lastestData.columns[0], axis=1)
dmt2_lastestData = pd.read_csv('./Data/DMT2/lastestData.csv', parse_dates=['Timestamp'])
dmt2_data= dmt2_lastestData.drop(dmt2_lastestData.columns[0], axis=1)

print("Start getting data", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
datenow = datetime.now().replace(microsecond=0, second= 0, minute= 0)
if datenow.hour >= 18:
  dstop = datenow.replace(hour=18)
else:
  dstop = datenow.replace(hour=6)
dstart = dstop - timedelta(hours=12)

resultDmt1 = Data.getData(sqlServer1, databaseName, sqlScript, dstart, dstop)
print("Mining and processing data DMT1 completed", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
dmt1_data = dmt1_data.append(resultDmt1, ignore_index=True)

resultDmt2 = Data.getData(sqlServer2, databaseName, sqlScript, dstart, dstop)
print("Mining and processing data DMT2 completed", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
dmt2_data = dmt2_data.append(resultDmt2, ignore_index=True)

print("Start drawing data", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
DMT1_img_path = 'DMT1\\'
DMT2_img_path = 'DMT2\\'
Chart.drawTorqueChart(dmt1_data, DMT1_img_path)
print("Completed drawing data DMT1", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
Chart.drawTorqueChart(dmt2_data, DMT2_img_path)
print("Completed drawing data DMT2", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

print("Start send email", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
outlook_from = 'MESAutoReport@firstsolar.com'
outlook_to = ['minhhuy.chu@firstsolar.com']
# outlook_to = ['minhhuy.chu@firstsolar.com','hoainam.truong@firstsolar.com','vanthanh.tran@firstsolar.com']
img_path = [DMT1_img_path, DMT2_img_path]
print("Creating email message...", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
dmt_email_msg = Email.generate_email(outlook_from, outlook_to, img_path)

print("Completed create email message and prepare sending email", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
dmt_email_msg = Email.generate_email(outlook_from, outlook_to, img_path)
Email.send_email(dmt_email_msg, outlook_from,'', outlook_to, 'fsbridge.fs.local', '25')
print("Completed task", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

print("Start to export new data and update the lastest data!", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
Exdata.update_data('./Data/DMT1/', resultDmt1, dmt1_data, dstop)
Exdata.update_data('./Data/DMT2/', resultDmt2, dmt2_data, dstop)
print("End export data!",  datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))