import time
import pygsheets
from skpy import Skype
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import requests

import json

url = "https://holidays-jp.github.io/api/v1/date.json"
response = requests.get(url)  #check if page exists or not

soup = BeautifulSoup(response.text, "html.parser")

dates=str(soup).replace("\n","").replace(": ","vvv").replace(",","vvv").replace("\"","").replace(" ","").replace("{","").replace("}","").split("vvv")
weekd={0:"月", 1:"火", 2:"水", 3:"木", 4:"金", 5:"土", 6:"日"}

d_list=[]
n_list=[]
wd = []

count=0
for i in dates:
	if count % 2==1:
		n_list.append(i)
	else:
		d_list.append(i)
	count+=1

for i in d_list:
	j=datetime.strptime(str(i), '%Y-%m-%d')
	wd.append(j.weekday())

is_message=1

today = datetime.today().strftime("%Y-%m-%d")

t_year=(str(today).split("-")[0])
t_month=(str(today).split("-")[1])
t_day=(str(today).split("-")[2])

mess="今後の国民の祝日\n"+"---------------------\n"

count=0
for i in d_list:
	x_year=(str(i).split("-")[0])
	x_month=(str(i).split("-")[1])
	x_day=(str(i).split("-")[2])
	print(i)
	if int(x_year) == int(t_year):
		if int(x_month) == int(t_month):
			if int(x_day) >= int(t_day):	
				mess=mess+(f"{i}({weekd[wd[count]]})    {n_list[count]}")+"\n"
		if int(x_month) == int(t_month)+1:	
			mess=mess+(f"{i}({weekd[wd[count]]})    {n_list[count]}")+"\n"
	if t_month == "12":	
		if int(x_year) > int(t_year):
			if x_month=="01":
				mess=mess+(f"{i}({weekd[wd[count]]})    {n_list[count]}")+"\n"
	count+=1

if is_message==1:

	sk = Skype("username", "password")
	group1=sk.chats.chat('Chat group code') #REAL

	group1.sendMsg(mess)
