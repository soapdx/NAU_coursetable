#encoding:utf-8
import requests,pytesseract
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
def getPwd(usrname):
  s=requests.session()
  r=s.get('http://172.17.61.200:8010/reader/login.php',timeout=60)
  f = open('VCode.jpg', 'wb')
  f.write(s.get('http://172.17.61.200:8010/reader/captcha.php').content)
  f.close()
  box= [4, 13, 52, 28]
  img = Image.open('VCode.jpg').convert('1').crop(box)
  ckcode = pytesseract.image_to_string(img)
  #print(ckcode)
  data={'number':usrname,'passwd':usrname,'captcha':ckcode,'select':'cert_no','returnUrl':'' }
  r=s.post('http://172.17.61.200:8010/reader/redr_verify.php',data,timeout=60)
  #print(r.status_code)
  idx = r.text.find("èº«ä»½è")
  #print(r.text[idx+35:idx+41])
  pwd=r.text[idx+35:idx+41]
  log_out=s.get('http://172.17.61.200:8010/reader/logout.php')
  return r.text[idx+35:idx+41]
if __name__=='__main__':
  usr = input()
  print(getPwd(usr))
