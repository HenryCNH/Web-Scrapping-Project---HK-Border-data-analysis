import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import pprint
import requests
from bs4 import BeautifulSoup
import lxml

path=r'https://www.immd.gov.hk/eng/stat_20230301.html'
data=requests.get(path).text
bs_data=BeautifulSoup(data, 'lxml')
table=bs_data.find('table', class_='tinymce-table1 table-passengerTrafficStat')
thead=table.find('thead')
body=table.find('tbody')
body_tr=body.find_all('tr')

#Index
control_point_list=[]
for i in body_tr:
    control_point_list.append(i.find('td', headers='Control_Point').text)

#headers
arrival_headers=[]
departure_headers=[]
for i in thead.find_all('th', headers='Arrival'):
    arrival_headers.append(i.text)
for i in thead.find_all('th', headers='Departure'):
    departure_headers.append(i.text)
total_headers=arrival_headers+departure_headers


#Data
number_list=[]
number=body.find_all('td', class_='hRight')
for i in number:
    number_list.append(i.text)

formatted_number_list=[]
for i in number_list:
    delim=','
    formatted_number_list.append(int("".join(i.split(delim))))

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
n = 8
sorted_data = list(divide_chunks(formatted_number_list, n))


#Converting into array
a=np.array(sorted_data)


#Creating DataFrame
desired_width=100
pd.set_option('display.width', desired_width)
pd.set_option('colheader_justify', 'center')
pd.set_option('display.max_columns',20)
df=pd.DataFrame(a,columns=[['Arrival','Arrival','Arrival','Arrival','Departure','Departure','Departure','Departure'],total_headers], index=control_point_list)
print(df)



# # #Create bar chart for arrival
y=df.iloc[-1,0:3]
x=total_headers[0:3]
plt.bar(x,y,width=0.25, color='green')
plt.title('1-Mar-2023 Arrival Number')
plt.show()

# #Create bar chart for control point usage
y=df.iloc[0:15,7]
x=control_point_list[0:15]
plt.figure(figsize=(20,15))
plt.bar(x,y, color='blue')
plt.title('1-Mar-2023 Total border Usage')
plt.xticks(fontsize=4.5)
plt.show()









