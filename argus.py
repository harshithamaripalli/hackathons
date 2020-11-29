import requests
import json
from requests.auth import HTTPBasicAuth
import time

api_token = ''
def login():
    login_response = requests.post(
        'https://argus-url/argusapp/v2/auth/login',
        auth=HTTPBasicAuth('username', 'password'))
    print(login_response)
    headers = {'Content-Type': 'application/json'}
    data = {'username': 'username', 'password': 'password'}
    token_url = 'https://argus-url/argusws/v2/auth/login'
    api_token = requests.post(token_url, data=data, headers=headers)
    print(api_token)



def get_data():

    global api_token

    api_url = 'https://argus-url/argusapp/metrics?expression=-10h:-0s:testservice1:metric1:avg'



    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_token)}

    response = requests.get(url=api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

response = get_data()
print ("GET RESPONSE = ", response)


def availability(values):
    pass_count = 0
    total = len(values)
    for value in values:
        if value != -1:
            pass_count = pass_count + 1

    pass_percentage = (pass_count/total) * 100
    print ("PASS_PERCENTAGE = " , pass_percentage, "%")



def send(ts):
    global api_token
    url='http://argus-url/v1/metrics/v2'


    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(api_token)}
    payload = [
        {
                "service": "testservice1",
                "metricName" : [ "metric1" ],
                "metricValue" : 2,
                "timestamp" : ts,
                "version" : 0
        }
    ]
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print('Send Response ', response)

'''
print (response[0]['scope'])
print (response[0]['metric'])
print (response[0]['tags'])
print (response[0]['datapoints'])


for item in response[0]['datapoints'].keys():
    print (item)
    print (response[0]['datapoints'][item])
'''
my_dict = response[0]['datapoints']

my_keys = my_dict.keys()
my_values = my_dict.values()

#print(my_keys)
#print(my_values)

dict_len = len(my_values)

#print(dict_len)

new_key_list = []
new_value_list = []

for key in my_keys:
    new_key_list.append(key)

for value in my_values:
    new_value_list.append(value)

availability(new_value_list)
index = 0

print ("Checking 1 time test failues ... ")
while index < dict_len:
    if new_value_list[index] == -1:
        if new_value_list[index+1] == 1:
            send(int(new_key_list[index]))
        else:
            index = index + 2
    index = index + 1

print ("Wating few seconds for Argus to pickup the changes...")
time.sleep(20)

response = get_data()
print ("GET RESPONSE = ", response)
my_dict = response[0]['datapoints']

my_keys = my_dict.keys()
my_values = my_dict.values()

#print(my_keys)
#print(my_values)

dict_len = len(my_values)

#print(dict_len)

new_key_list = []
new_value_list = []

for key in my_keys:
    new_key_list.append(key)

for value in my_values:
    new_value_list.append(value)

availability(new_value_list)


