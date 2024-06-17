import os, glob
import json
import pandas as pd
import datetime

## Pick today's date
date_time = str(datetime.datetime.now().strftime("%d-%m-%y"))

## Filter specific '.json' file name
json_files = glob.glob("elasticache-*.json")

## Run loop with the filtered file name
for file in json_files:

## Open specific Files and iterate it
    with open(file, "r") as json_source:
        s_json = json.load(json_source)

    ### Check for data will be get
        data_detail = pd.json_normalize(s_json, record_path=['CacheClusters'])
        security_group = pd.json_normalize(s_json, record_path=['CacheClusters', 'SecurityGroups'])

    ## Data Cleanup, delete unnecessary columns
    column_to_delete = ['SecurityGroups', 'ClientDownloadLandingPage']

    ### Copy existing data from json_normalize and will make changes on the new data
    ### Without alter existing .json file
    df_cp = data_detail.copy()
    data_copy = df_cp.drop(columns=column_to_delete)

    ## Convert existing Normalize data to Data Frame format
    new_sg = pd.DataFrame(security_group)

    ## Combine data to new Data Frame
    new_data = pd.concat([data_copy, new_sg.reset_index(drop=True)], axis=1,  ignore_index=False)

    ### Debug new_data DataFrame
    #print(new_data.head())

    ## Export data to Excel / "-exported.xlsx"
    base_file_name, extention = os.path.splitext(file)
    new_name = base_file_name + "-exported"
    new_data.to_excel(new_name + ".xlsx", index=False)

## Combine all '.xlsx' file into 1 file
xlsx_files  = glob.glob("*-exported.xlsx")
merge_files = pd.DataFrame()

for xl_files in xlsx_files:
    read_xl = pd.read_excel(xl_files)
    merge_files = pd.concat([merge_files, read_xl], ignore_index=True)

merge_files.to_excel("elasticache-export-"+date_time+".xlsx", index=False)