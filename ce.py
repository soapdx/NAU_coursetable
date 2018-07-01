#encoding:utf-8
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
usrname = input("Please input your name:\n")
pwd = input("Please input your password:\n")
s=requests.session()
r=s.get('http://jwc.nau.edu.cn/LoginOut.aspx',timeout=60)
#print(r.text)
f = open('VCode.jpg', 'wb')
f.write(s.get('http://jwc.nau.edu.cn/CheckCode.aspx').content)
f.close()
img = Image.open('VCode.jpg')
img.show()
ckcode = input("Please input code:\n")
data={'UserName':usrname,'UserPwd':pwd,'CheckCode':ckcode,'btnLogin':'登录'}
r=s.post('http://jwc.nau.edu.cn/Login.aspx',data,timeout=60)
print(r.status_code)
#r=s.get('http://jwc.nau.edu.cn/Students/CourseElection.aspx?t=672FBCD64580685FDFECBC5AC6A7DE51&cid=DBD08C22A98EC14A')
#print(r.text)

data={'courseID': '12400140','teachingClass': 'JD090','term': '201720182','startDate': '1D0D76C153D4B4732229B1EFC1C5D911FA8AD95A89D898E3','endDate': '587C1289B0A43AC3E8A185EAC73F07F71795460620AC6B6C',
      'limitNum': '0','CourseSelectStyle': '先到先得'}
while 1:
  r=s.post('http://jwc.nau.edu.cn/Servlet/AddCourseSelectModel.ashx',data,timeout=3)
  print(r.text)
log_out=s.get('http://jwc.nau.edu.cn/LoginOut.aspx')