SELECT * FROM [ODS].[mfg].[ProcessHistoryHipotMaintData]
WHERE Readtime between '{dstart}' and '{dstop}' 
UNION ALL
SELECT * FROM [ODS].[mfg].[ProcessHistoryInterlayerPairingMaintData]
WHERE Readtime between '{dstart}' and '{dstop}' 
Order by Readtime desc