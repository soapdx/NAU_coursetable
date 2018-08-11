#coding=utf-8
import requests,datetime,codecs,re,pytesseract,sys
from PIL import Image
from io import BytesIO
from ics import Calendar,Event
global st,et,d1
st=['08:30:00+08:00','09:20:00+08:00','10:20:00+08:00','11:10:00+08:00','12:00:00+08:00','13:30:00+08:00',
    '14:20:00+08:00','15:20:00+08:00','16:10:00+08:00','17:00:00+08:00','18:30:00+08:00','19:20:00+08:00',
	'20:10:00+08:00',]
et=['09:10:00+08:00','10:00:00+08:00','11:00:00+08:00','11:50:00+08:00','12:40:00+08:00','14:10:00+08:00',
    '15:00:00+08:00','16:00:00+08:00','16:50:00+08:00','17:40:00+08:00','19:10:00+08:00','20:00:00+08:00',
	'20:50:00+08:00',]

def AppendKC(kc):
  d1 = datetime.date(2018, 2, 26)
  def AppendEvent():
    e = Event()
    e.name = kc[0]
    e.begin = d1.isoformat() + 'T' + st[int(kc[4]) - 1]
    e.end = d1.isoformat() + 'T' + et[int(kc[5]) - 1]
    e.location = kc[2]
    c.events.append(e)
    print('ok')
    return
  CurrentWeek = 1
  WeekDelta = datetime.timedelta(days=7)
  WeekMark = -1
  WeekDay = datetime.timedelta(days=int(kc[3])-1)
  if kc[1][len(kc[1])-2]=='双':WeekMark=0
  if kc[1][len(kc[1])-2]=='单':WeekMark=1
  d1=d1+WeekDay
  print(WeekDelta)
  rng=re.findall(r"\d+\.?\d*",kc[1])
  print(rng,rng[len(rng)-1])
  if kc[1][0]=='第':
    while CurrentWeek!=int(rng[len(rng)-1]):
      CurrentWeek += 1
      d1 =d1+ WeekDelta
      if str(CurrentWeek) in rng:
        print(CurrentWeek)
        AppendEvent()
  else:
    for i in range(int(rng[0]),int(rng[1])+1):
      while CurrentWeek!=i:
        CurrentWeek += 1
        d1 = d1 + WeekDelta
      if WeekMark<0:
        print(CurrentWeek)
        AppendEvent()
      elif CurrentWeek%2==WeekMark:
        print(CurrentWeek)
        AppendEvent()
      d1=d1+WeekDelta
      CurrentWeek+=1
  return
if __name__ == '__main__':
  c = Calendar()
  usrname = sys.argv[1]
  pwd = sys.argv[2]
  #usrname = input("Please input your name:\n")
  #pwd = input("Please input your passwd:\n")
  s=requests.session()
  r=s.get('http://jwc.nau.edu.cn/LoginOut.aspx',timeout=60)
  #print(r.text)
  f = open('VCode.png', 'wb')
  f.write(s.get('http://jwc.nau.edu.cn/CheckCode.aspx').content)
  f.close()
  img = Image.open('VCode.png').convert('L')
  #img.show()
  ckcode = pytesseract.image_to_string(img)
  #ckcode = input("Please input code:\n")
  data = {'UserName':usrname,'UserPwd':pwd,'CheckCode':ckcode,'btnLogin':'登录'}
  r = s.post('http://jwc.nau.edu.cn/Login.aspx',data,timeout=60)
  print(r.status_code)
  r = s.get('http://jwc.nau.edu.cn/Students/MyCourseScheduleTable.aspx')
  #print(r.text)
  idx = r.text.find('for(i = 0;i <')
  num = int(r.text[idx+14:idx+16])
  for i in range(num-1):
    index0=r.text.find('subcat['+str(i)+']')
    index1=r.text.find('subcat['+str(i+1)+']')
    if i>=10:
      kc0=r.text[index0+23:index1-34]
      AppendKC(kc0.replace("'","").replace(' ','').replace(',', '/', kc0.count(',', kc0.find('第'), kc0.find('周')) + 1).replace('/', ',', 1).split(','))
    else:
      kc0 = r.text[index0 + 22:index1 - 34]
      AppendKC(kc0.replace("'","").replace(' ','').replace(',', '/', kc0.count(',', kc0.find('第'), kc0.find('周')) + 1).replace('/', ',', 1).split(','))
  kc0 = r.text[index1+23:idx-30]
  AppendKC(kc0.replace("'","").replace(' ','').replace(',', '/', kc0.count(',', kc0.find('第'), kc0.find('周')) + 1).replace('/', ',', 1).split(','))

  print(c.events)

  codecs.open(usrname+'.ics', 'wb', 'utf-8').writelines(c)
  log_out=s.get('http://jwc.nau.edu.cn/LoginOut.aspx')
