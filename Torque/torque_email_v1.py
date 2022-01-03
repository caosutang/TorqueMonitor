# library debug
import logging 
import Module.send_email as Email
import Module.mine_data as Data  
import Module.draw_chart as Chart
from datetime import datetime, timedelta

sqlScript = r"SqlScripts/TorqueData.sql"
databaseName = 'ModuleAssembly' 
sqlServer1 = 'dmt1messqlods' 
sqlServer2 = 'dmt2messqlods' 

print("Start getting data", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
datenow = datetime.now().replace(microsecond=0, second= 0, minute= 0)
if datenow.hour >= 18:
  dstop = datenow.replace(hour=18)
else:
  dstop = datenow.replace(hour=6)
dstart = dstop - timedelta(days=14)
resultDmt1 = Data.getData(sqlServer1, databaseName, sqlScript, dstart, dstop)
print("Mining and processing data DMT1 completed", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

resultDmt2 = Data.getData(sqlServer2, databaseName, sqlScript, dstart, dstop)
print("Mining and processing data DMT2 completed", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

print("Start drawing data", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
DMT1_img_path = 'DMT1\\'
DMT2_img_path = 'DMT2\\'
Chart.drawTorqueChart(resultDmt1, DMT1_img_path)
print("Completed drawing data DMT1", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
Chart.drawTorqueChart(resultDmt2, DMT2_img_path)
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

# With gmail
# send_email(email_msg, gmail_user, gmail_pwd, to_email, 'smtp.gmail.com', 587)