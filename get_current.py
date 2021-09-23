import requests
import datetime
import os
import csv

url = 'https://api.notion.com/v1/databases/e2066ae247304da69cf12dd1112f886c/query'

headers = {
    'Authorization': f"Bearer secret_GW6LHmebyJSmV8VScz7cKi14kj7x2ixUDwEO0jhnQsu",
    'Notion-Version': '2021-08-16',
    'Content-Type': 'application/json',
}

account_date = {'name':'account_date',"value":""}
account_content ={'name':'account_content',"value":""}
acc_from =  {'name':'from',"value":""}
acc_to = {'name':'to',"value":""}
acc_value = {'name':'value','value':0}
acc_year = {'name':'year','value':""}
acc_month = {'name':'month','value':""}
acc_id = {'name':'id','value':""}

account_csv_fieldnames = [
    account_date['name'],
    account_content['name'],
    acc_from['name'],
    acc_to['name'],
    acc_value['name'],
    acc_year['name'],
    acc_month['name'],
    acc_id['name'],
    ]

accounts = ['생활비통장','주식투자통장','쿠팡','현금','수입통장']
acc_csv_fieldname = ['last_update']+accounts

def yyyy_mm_format(yyyy,mm):
    if type(yyyy) != str:
        return '{0:04d}'.format(yyyy)+'-'+'{0:02d}'.format(mm)
    else:
        return yyyy+'-'+mm

def update_bank_statement(file_name,data,ids=[],last_date=None,init=False):
    with open(file_name, 'a', newline='') as csvfile:
        print("send_query")
        print(data)
        response = requests.post(url, headers=headers, data=data)
        par = response.json()
        writer = csv.DictWriter(csvfile, fieldnames=account_csv_fieldnames)
        out_of_len = False
        if init:
            writer.writeheader()
        if par.get('results'):
            count = len(par['results'])
            print(count)
            if count>90:
                out_of_len = True

            for i in range(count):
                value_ = len(par['results'][i]['properties']['결제내역']['title'][0]['plain_text'])
                if value_>0:
                    csv_dic = {
                        account_csv_fieldnames[0]: par['results'][i]['properties']['date']['date']['start'],
                        account_csv_fieldnames[1]: par['results'][i]['properties']['결제내역']['title'][0]['plain_text'],
                        account_csv_fieldnames[2]: par['results'][i]['properties']['from_name']['formula']['string'],
                        account_csv_fieldnames[3]: par['results'][i]['properties']['to_name']['formula']['string'],
                        account_csv_fieldnames[4]: par['results'][i]['properties']['금액']['number'],
                        account_csv_fieldnames[5]: par['results'][i]['properties']['year']['formula']['string'],
                        account_csv_fieldnames[6]: par['results'][i]['properties']['month']['formula']['string'],
                        account_csv_fieldnames[7]: par['results'][i]['id'],
                    }
                    if csv_dic[account_csv_fieldnames[-1]] not in ids:
                            writer.writerow(csv_dic)
        return out_of_len

def get_bank_state_last(file_name="./current.csv"):
    def get_last_date(csv_file_name):
        res = ""
        with open(csv_file_name,mode='r') as inp:
            reader = csv.DictReader(inp)
            last = list(reader)[-1]
            if(last['account_date']!=account_date['name']):
                res = last['account_date']
        return res

    def get_ids_in_same_date(csv_file_name,last_date=None):
        ids = []
        with open(csv_file_name,mode='r') as inp:
            reader = csv.DictReader(inp)
            list_reader = list(reader)
            for i in range(len(list_reader)-1,0,-1):
                array = list_reader[i]
                if array['account_date'] == last_date:
                    ids.append(array['id'])
                else:
                    break
        return ids

    def _update_bank_statement(file_name):
        update_state = True
        while(update_state):
            last_date = get_last_date(file_name)
            ids = get_ids_in_same_date(file_name,last_date)
            data='{\
            "filter":{\
                "property":"date","date":{"on_or_after":"'+last_date+'"}\
                },\
            "sorts":[{"property":"date","direction":"ascending"}]\
            }'
            update_state = update_bank_statement(file_name,data,ids,last_date)

    ## update state ##            
    if os.path.exists(file_name):
        _update_bank_statement(file_name)
        return True # Update
    
    ## init state ##
    else:
        with open(file_name, 'w', newline='') as csvfile:
            print("new_file")
        data='{\
        "sorts":[{"property":"date","direction":"ascending"}]\
        }'
        update_bank_statement(file_name,data,init=True)
        _update_bank_statement(file_name)

        return False # init

def get_ids_account(csv_file_name):
    ids = []
    with open(csv_file_name,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        for i in range(len(list_reader),0,-1):
            array = list_reader[i-1]
            if array['to'] not in ids:
                ids.append(array['to'])
            if array['from'] not in ids:
                ids.append(array['from'])
    return ids

def account_sum(csv_file_name,account):
    res=0
    with open(csv_file_name,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        for i in range(0,len(list_reader)):
            array = list_reader[i]
            if array['to'] == account:
                res-=int(array['value'])       
            if array['from'] == account:
                res+=int(array['value'])
    return res

def divide_by_month(csv_file_name,monthly_div_folder,now_yyyy_mm):
    ## save for last month 
    with open(csv_file_name,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        id = ""
        m_reader = None
        montly = None
        prev_porccessed_list = [f for f in os.listdir(monthly_div_folder) if os.path.isfile(os.path.join(monthly_div_folder, f))]
        for i in range(len(list_reader)):
            array = list_reader[i]
            year = array['year']
            yyyy_mm = yyyy_mm_format(year,array['month'])
            file_path = os.path.join(monthly_div_folder,yyyy_mm)+'.csv'
            if((yyyy_mm!= now_yyyy_mm) and (yyyy_mm+'.csv' not in prev_porccessed_list)):
                if id != array['month']:
                    if montly is not None:
                        montly.close()
                    montly = open(file_path,mode='w')
                    m_reader = csv.DictWriter(montly,fieldnames=account_csv_fieldnames)
                    m_reader.writeheader()
                    id = array['month']
                m_reader.writerow(array)

def divide_by_basedate(csv_file_name,basedate,output_data_path=None):
    today = datetime.datetime.now()
    preive = (today-datetime.timedelta(days=basedate))
    if output_data_path is None:
        output_file_name = 'date'+str(basedate)+'.csv'
    else:
        output_file_name = output_data_path

    with open(csv_file_name,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        id = ""
        find_line = -1
        for i in range(0,len(list_reader)):
            date_pointer = list_reader[i]['account_date']
            datetimer = datetime.datetime.strptime(date_pointer,'%Y-%m-%d')
            if preive<datetimer:
                find_line = i
                break
        with open(output_file_name,mode='w') as tp:
            m_reader = csv.DictWriter(tp,fieldnames=account_csv_fieldnames)
            m_reader.writeheader()
            for i in range(find_line,len(list_reader)):
                array = list_reader[i]    
                m_reader.writerow(array)
    return output_file_name

def cal_account(csv_file_name,state,accounts=accounts):
    with open(csv_file_name,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        cal_state = []
        cal_state_dict = {}
        if state == 'income':
            cal = 'from'
        else:
            cal = 'to'
        for i in range(len(list_reader)):
            array = list_reader[i]
            if array[cal] not in accounts:
                if array[cal] not in cal_state:
                    cal_state.append(array[cal])
                    cal_state_dict[array[cal]]=0
                    cal_state_dict[array[cal]]+=int(array['value'])
                else:
                    cal_state_dict[array[cal]]+=int(array['value'])
    return cal_state_dict

def cal_ratio_from_dic(in_dic):
    out_dic = in_dic.copy()
    length = len(in_dic)
    total = 0.0
    keys = list(in_dic.keys())
    for i in range(length):
        total+=in_dic[keys[i]]
    for i in range(length):
        out_dic[keys[i]] = float(in_dic[keys[i]])/total
    return out_dic

def cal_account_(acc_file,acc_dic=None):
    if acc_dic is None:
        init_data = ["0001-01-01"]+ [0] * len(accounts)
        acc_dic = dict(zip(acc_csv_fieldname, init_data))
    acc_dic_ = acc_dic.copy()
    with open(acc_file,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        print(len(list_reader))
        for i in range(0,len(list_reader)):
            array = list_reader[i]
            # print(array)
            if array['to'] in accounts: 
                acc_dic_[array['to']]+=int(array['value'])
            if array['from'] in accounts:
                acc_dic_[array['from']]-=int(array['value']) 
            acc_dic_['last_update'] = array[account_csv_fieldnames[0]]
    return acc_dic_
    
def account_update(account_file,monthly_div_folder,csv_file):
    init_data = ["0001-01-01"]+ [0] * len(accounts)
    init_dic = dict(zip(acc_csv_fieldname, init_data))
    init_prev_dic = dict(zip(acc_csv_fieldname, init_data))
    now_date = datetime.datetime.now()
    last_date = (now_date.replace(day=1)-datetime.timedelta(days=1))
    update_date = last_date
    
    def formatting(dic):
        dic[acc_csv_fieldname[0]] = str(dic[acc_csv_fieldname[0]])
        for account in accounts:
            dic[account] = int(dic[account])
        return dic 

    if os.path.exists(account_file) is False:
        with open(account_file, 'w', newline='') as ac_file:
            writer = csv.DictWriter(ac_file, fieldnames=acc_csv_fieldname)
            writer.writeheader() 
            writer.writerow(init_dic)
            writer.writerow(init_prev_dic)
    
    with open(account_file, 'r', newline='') as ac_file: 
        reader = csv.DictReader(ac_file)
        readers = list(reader)
        init_dic = formatting(readers[0])
        init_prev_dic = formatting(readers[1])
        update_date = datetime.datetime.strptime(init_prev_dic[acc_csv_fieldname[0]],'%Y-%m-%d')
        print("update_date: ",update_date)
        if update_date<last_date:
            init_prev_dic = dict(zip(acc_csv_fieldname, init_data))
            update_origin =[f for f in os.listdir(monthly_div_folder) if os.path.isfile(os.path.join(monthly_div_folder, f))]
            for monthly in update_origin:
                init_prev_dic = cal_account_(acc_dic = init_prev_dic,acc_file = os.path.join(monthly_div_folder,monthly))
            update_date = last_date
        print(init_prev_dic)  

    with open(csv_file,mode='r') as inp:
        reader = csv.DictReader(inp)
        list_reader = list(reader)
        find_line = len(list_reader)
        today = datetime.datetime.strptime(list_reader[-1]['account_date'],'%Y-%m-%d')
        preive = (today-datetime.timedelta(days=1))

        for i in range(0,len(list_reader)):
            read_p = list_reader[i]
            datetimer = datetime.datetime.strptime(read_p['account_date'],'%Y-%m-%d')
            if update_date<datetimer or preive<datetimer:
                find_line = i
                break
        print(datetimer)
        for i in range(find_line,len(list_reader)):
            read_p = list_reader[i]
            datetimer = datetime.datetime.strptime(read_p['account_date'],'%Y-%m-%d')
            if read_p['to'] in accounts: 
                init_prev_dic[read_p['to']]+=int(read_p['value'])
            if read_p['from'] in accounts:
                init_prev_dic[read_p['from']]-=int(read_p['value'])
            init_prev_dic[acc_csv_fieldname[0]] = datetimer.strftime("%Y-%m-%d")
            if preive<datetimer:
                find_line = i
                init_prev_dic[acc_csv_fieldname[0]] = preive.strftime("%Y-%m-%d")
                break
        print(find_line)
        init_dic = init_prev_dic.copy()
        for i in range(find_line,len(list_reader)):
            read_p = list_reader[i]
            if read_p['to'] in accounts: 
                init_dic[read_p['to']]+=int(read_p['value'])
            if read_p['from'] in accounts:
                init_dic[read_p['from']]-=int(read_p['value'])
        init_dic[acc_csv_fieldname[0]]=today.strftime("%Y-%m-%d")

    with open(account_file, 'w', newline='') as ac_file: 
        writer = csv.DictWriter(ac_file,acc_csv_fieldname)
        writer.writeheader() 
        writer.writerow(init_dic)
        writer.writerow(init_prev_dic)

def static_process(input_data):
    expanse = cal_account(input_data,state='expanse')
    income = cal_account(input_data,state='income')
    
    exp_total = 0
    for exp_key in expanse.keys():
        exp_total += expanse[exp_key]
        expanse[exp_key] *=-1
    expanse.update({"total_exp":exp_total*(-1)})

    income_total = 0
    for exp_key in income.keys():
        income_total += income[exp_key]
 
    income.update({"total_income":income_total})
    return income, expanse

def make_static_data(input_data_path,output_data_path):
    s_income,s_exp = static_process(input_data_path)
    r_income = s_income.copy()
    r_exp = s_exp.copy()
    for income_key in s_income.keys():
        r_income[income_key] = round(float(s_income[income_key])/(float(s_income['total_income'])+0.0000001)*100)
    for exp_key in s_exp.keys():
        r_exp[exp_key] = round(float(s_exp[exp_key])/(float(s_exp['total_exp'])+0.000001)*100)  


    res = s_income.copy()
    res.update(s_exp)
    res2 = r_income.copy()
    res2.update(r_exp)
    with open(output_data_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=res.keys())
        writer.writeheader()
        writer.writerow(res)
        writer.writerow(res2)

def make_chart(csv_input,png_output):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    from matplotlib import rc
    # import seaborn as sns
    # %matplotlib inline

    rc('font', family='AppleGothic')

    plt.rcParams['axes.unicode_minus'] = False

    income = {}
    exp = {}
    with open(csv_input, 'r', newline='') as ac_file: 
        reader = csv.DictReader(ac_file)
        readers = list(reader)
        dec = readers[0]
        for key in dec.keys():
            if key not in ["total_income","total_exp"]:
                if int(dec[key])>0:
                    income.update({key:int(dec[key])})
                else:
                    exp.update({key:abs(int(dec[key]))})
   
    ratio_income = income.values()
    labels_income = income.keys()
    ratio_exp = exp.values()
    labels_exp = exp.keys()
    p1 = plt.subplot(211)
    p2 = plt.subplot(212)
    p1.pie(ratio_income, labels=labels_income, autopct='%.1f%%')
    p2.pie(ratio_exp, labels=labels_exp, autopct='%.1f%%')
    plt.savefig(png_output)