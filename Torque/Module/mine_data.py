import pyodbc
import pandas as pd
import numpy as np

def getData(serverName, databaseName, sqlFile, dstart, dstop):
  Conn_String = 'Driver={SQL Server Native Client 11.0};Server='+ serverName +';Trusted_Connection=yes;Database='+ databaseName +';'
  Conn = pyodbc.connect(Conn_String)
  sql_script = open(sqlFile,"r").read().format(dstart = dstart, dstop = dstop)
  result = pd.DataFrame() 
  result = pd.read_sql_query(sql_script, Conn)
  Conn.close()
  
  result['Date'] = result['ReadTime'].dt.date
  result['Timestamp'] = result['ReadTime'].dt.floor('h')  
  result['MaxValue'] = abs(result['MaxValue'])
  result['MinValue'] = abs(result['MinValue'])
  result['Plant']= result['EquipmentName'].str.slice(0,4,1)
  result['Line']= result['EquipmentName'].str.slice(4,6,1)
  result['Tool']= result['EquipmentName'].str.slice(7,)  
  
  resultX = result.groupby(['EquipmentName','Plant','Line','Tool','Device','Timestamp']).agg({'MaxValue':np.median}).reset_index()
  resultX['MinValue'] = result.groupby(['EquipmentName','Plant','Line','Tool','Device','Timestamp']).agg({'MinValue':np.median}).reset_index()['MinValue']

  resultY = result.groupby(['EquipmentName','Plant','Line','Tool','Device']).agg({'MaxValue':np.average}).reset_index()
  resultY['MinValue'] = result.groupby(['EquipmentName','Plant','Line','Tool','Device']).agg({'MinValue':np.average}).reset_index()['MinValue']
  for i in range(len(resultX.index)):
    for j in range(len(resultY.index)):
        if resultX['EquipmentName'][i] == resultY['EquipmentName'][j] and resultX['Device'][i] == resultY['Device'][j]:
            if resultX['MaxValue'][i] > resultY['MaxValue'][j] + 70:
                # resultX['MaxValue'][i] = resultY['MaxValue'][j]
                resultX.loc['MaxValue',i] = resultY['MaxValue'][j]
            if resultX['MinValue'][i] > resultY['MinValue'][j] + 70:
                # resultX['MinValue'][i] = resultY['MinValue'][j]
                resultX.loc['MinValue',i] = resultY['MinValue'][j]
  return resultX
