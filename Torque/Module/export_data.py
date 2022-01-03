from datetime import datetime, timedelta
import os.path
import pandas as pd

def update_data(path, newData, oldData, getDate):
  # Pass process if don't have days
  newData, timeData, temp = export_day_data(path, newData, getDate)
  updatelastestData = oldData.append(newData, ignore_index = True)
  # return updateData.append(newData, ignore_index = True)
  dataExcludeName = timeData - timedelta(days=14) 
  fileExcludeName = path + dataExcludeName.strftime('%Y%m%d') + temp + '.csv'
  if os.path.isfile(fileExcludeName):
    removedData = pd.read_csv(fileExcludeName, parse_dates=['Timestamp'])
    df = pd.merge(updatelastestData, removedData, how='outer', indicator=True)
    endData = df.loc[df._merge == 'left_only'].drop("_merge", axis=1)
    endData.to_csv('./data/DMT1/lastestDataNew.csv')
    print('File exists and update completed')
  else:
    updatelastestData.to_csv('./data/DMT1/lastestData.csv')
    print('File does not exist and update completed')
  
def export_day_data(path, newData, getDate):
  # Save data into csv file and update data file
  # Create name cvs
  timeToday = getDate
  timeString =timeToday.strftime('%Y%m%d')
  if timeToday.hour >= 18:
    newData.to_csv(path + timeString + '_2.csv')
    timeData = timeToday.replace(microsecond=0, second=0, minute=0, hour = 18)
    temp = '_2'
  else:
    newData.to_csv(path + timeString + '_1.csv')
    timeData = timeToday.replace(microsecond=0, second=0, minute=0, hour = 6)
    temp = '_1'
  return newData, timeData , temp
  