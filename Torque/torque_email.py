# library debug
import logging 
from datetime import datetime
import Module.send_email as Email
import Module.mine_data as Data  
import Module.draw_chart as Chart
from datetime import datetime, timedelta

sqlScript = r"SqlScripts/TorqueData.sql"
databaseName = 'ModuleAssembly' 
sqlServerName = 'dmt1messqlods' 

dstop = datetime.now().replace(microsecond=0, second= 0, minute= 0)
dstart = dstop - timedelta(hours=12)
resultDmt1 = Data.getData(sqlServerName, databaseName, sqlScript, dstart, dstop)
# sqlServerName = 'dmt2messqlods' 
# resultDmt2 = Data.getData(sqlServerName, databaseName, sqlScript, dstart, dstop)
# result = resultDmt1.append(resultDmt2,ignore_index=True)

DMT1_path = '.\Figure\Int\DMT1\ '
# DMT2_path = '.\Figure\Int\DMT1'
Chart.drawTorqueChart(resultDmt1, DMT1_path)
# Chart.drawTorqueChart(resultDmt2, DMT2_path)

# outlook_from = 'MESAutoReport@firstsolar.com'
# # outlook_to = ['minhhuy.chu@firstsolar.com','hoainam.truong@firstsolar.com','vanthanh.tran@firstsolar.com']
# outlook_to = ['minhhuy.chu@firstsolar.com']
# # from_email = 'chuhuyvt@gmail.com'
# path_image = "Figure"
# email_msg = Email.generate_email(outlook_from, outlook_to, path_image)
# # send_email(email_msg, gmail_user, gmail_pwd, to_email, 'smtp.gmail.com', 587)
# Email.send_email(email_msg, outlook_from,'', outlook_to, 'fsbridge.fs.local', '25')