import datetime
import os
import get_current
import shutil
import csv
current_set ={
    "root": "./csv_files",
    "monthly": "monthly_div",
    "monthly_processed":"monthly_processed",
    "state_" : "state_",
    "manage_file" : "current_bank.csv",
    "account_file" : "account.csv",
    "datebase" : "base_date"
}

csv_folder = current_set["root"]

if os.path.exists(csv_folder) is False:
    os.mkdir(csv_folder)

csv_folder_monthly = os.path.join(csv_folder,current_set["monthly"])


if os.path.exists(csv_folder_monthly) is False:
    os.mkdir(csv_folder_monthly)

csv_folder_monthly_p = os.path.join(csv_folder,current_set["monthly_processed"])

if os.path.exists(csv_folder_monthly_p) is False:
    os.mkdir(csv_folder_monthly_p)
    
csv_file = os.path.join(csv_folder,current_set["manage_file"])
account_file = os.path.join(csv_folder,current_set["account_file"])
date_process_path = os.path.join(csv_folder,current_set["datebase"])
now_date = datetime.datetime.now()
yyyy = now_date.year
mm = now_date.month 

## init state ##
init_state_checker = get_current.get_bank_state_last(csv_file)
print(get_current.cal_account_(csv_file))
# get_current.divide_by_month(csv_file,csv_folder_monthly,get_current.yyyy_mm_format(yyyy,mm))
# account_state = get_current.account_update(account_file,csv_folder_monthly,csv_file) 

# date_30 = get_current.divide_by_basedate(csv_file,30,date_process_path+"30.csv")
# date_60 = get_current.divide_by_basedate(csv_file,60,date_process_path+"60.csv")
# date_90 = get_current.divide_by_basedate(csv_file,90,date_process_path+"90.csv")
# os.remove(csv_file)
# shutil.copy(date_60,csv_file)

# prev_proccessed_list = [f for f in os.listdir(csv_folder_monthly_p) if os.path.isfile(os.path.join(csv_folder_monthly_p, f))]
# update_origin =[f for f in os.listdir(csv_folder_monthly) if os.path.isfile(os.path.join(csv_folder_monthly, f)) and f not in prev_proccessed_list] 
# for update_file in update_origin:
#     update_path = os.path.join(csv_folder_monthly,update_file)
#     exp_path = os.path.join(csv_folder_monthly_p,update_file)
#     get_current.make_static_data(update_path,exp_path)

# get_current.make_static_data(date_30,date_process_path+"30p.csv")
# get_current.make_static_data(date_60,date_process_path+"60p.csv")
# get_current.make_static_data(date_90,date_process_path+"90p.csv")
# get_current.make_chart(date_process_path+"30p.csv","./res30.png")
# # print(cal_ratio_from_dic(expanse))