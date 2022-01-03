import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

def drawTorqueChart(chartData, path):
  tools = chartData["Tool"].unique()
  devices = chartData['Device'].unique()
  
  for t in tools:
    for d in devices:
      df = chartData[(chartData['Tool'] == t) & (chartData['Device'] == d)]
      if (df.shape[0] > 1) and (d != 'UNKNOWN'):
        fig, ax = plt.subplots(2,1, figsize=(16,8))
        sns.set_theme(style='whitegrid')
        sns.scatterplot(x="Timestamp", y="MaxValue", data= df, hue='Line',  palette="bright", marker="s", ax= ax[0])
        sns.scatterplot(x="Timestamp", y="MinValue", data= df, hue='Line',  palette="bright", marker="v", ax=ax[1])
        ax[0].set(xlabel='', ylabel='Positive Torque')
        ax[0].legend(loc='lower left')
        ax[1].set(xlabel='Read Time', ylabel='Negative Torque')
        ax[1].legend(loc='lower left')
        if t[0:3] == 'INT':
          plt.savefig('.\Figure\Int\\' + path + d + '.jpg',bbox_inches='tight')
        else: 
          plt.savefig('.\Figure\Sim\\' + path + d + '.jpg',bbox_inches='tight')
        plt.close(fig)