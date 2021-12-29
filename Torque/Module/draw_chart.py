import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

def drawTorqueChart(chartData, path):
  plants = chartData["Plant"].unique()
  tools = chartData["Tool"].unique()
  devices = chartData['Device'].unique()
  
  for p in plants:
    for t in tools:
      for d in devices:
        df = chartData[(chartData['Plant'] == p) &(chartData['Tool'] == t) & (chartData['Device'] == d)]
        if df.shape[0] > 0:
          fig, ax = plt.subplots()
          sns.set_theme(style='whitegrid')
          plt.figure(figsize=(16,3))

          # sns.lmplot(x="date", y="MaxValue", data= df, fit_reg=False, hue='Line', legend=False, palette="bright", height=3, aspect=20/3, lowess=True, markers='v', scatter_kws={'s':20})
          sns.scatterplot(x="Timestamp", y="MaxValue", data= df, hue='Line',  palette="bright", marker="s")
          plt.legend(loc="lower left")
          plt.xlabel('Read Time')
          plt.ylabel('Positive Torque in %')
          if t[0:3] == 'INT':
            # plt.savefig(path + p + "_" + d + "_P" + '.jpg',bbox_inches='tight')
            plt.savefig(path + d + "_P" + '.jpg',bbox_inches='tight')
          else: 
            plt.savefig(path + p + "_" + d + "_P" + '.jpg',bbox_inches='tight')
            # plt.savefig(path + d + "_P" + '.jpg',bbox_inches='tight')
          plt.clf()
          plt.close(fig)

          # sns.lmplot(x='Hours', y='MinValue', data= df, fit_reg=False, hue='Line', legend=False, palette="bright", height=3, aspect=20/3, lowess=True, markers='v', scatter_kws={'s':20})
          sns.scatterplot(x="Timestamp", y="MinValue", data= df, hue='Line',  palette="bright", marker="v")
          plt.legend(loc="lower left")
          plt.xlabel('Read Time')
          plt.ylabel('Negative Torque in %')
          if t[0:3] == 'INT':
            plt.savefig(r".\Figure\Int\ " + p + "_" + d  + "_N" + '.jpg',bbox_inches='tight')
          else: 
            plt.savefig(r".\Figure\Sim\ " + p + "_" + d +  "_N" + '.jpg',bbox_inches='tight')
          plt.clf()
          plt.close(fig)
