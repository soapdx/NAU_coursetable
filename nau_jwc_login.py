#encoding:utf-8
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
usrname = input("Please input your name:\n")
pwd = input("Please input your passwd:\n")
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
r=s.get('http://jwc.nau.edu.cn/Students/MyCourseScheduleTable.aspx')
#print(r.text)
idx=r.text.find('for(i = 0;i <')
num=int(r.text[idx+14:idx+16])
for i in range(num-1):
  index0=r.text.find('subcat['+str(i)+']')
  index1=r.text.find('subcat['+str(i+1)+']')
  if i>=10:
    print(r.text[index0+23:index1-34])
  else:
    print(r.text[index0 + 22:index1 - 34])
print(r.text[index1+23:idx-30])
log_out=s.get('http://jwc.nau.edu.cn/LoginOut.aspx')
