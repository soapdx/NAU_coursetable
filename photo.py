import requests,pytesseract,count
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import info_one as info
def get_photo(stuid):
    s = requests.session()
    r = s.get('http://jwc.nau.edu.cn/LoginOut.aspx', timeout=60)
    usrname = '810019'
    pwd = '405405'
    f = open('VCode.png', 'wb')
    f.write(s.get('http://jwc.nau.edu.cn/CheckCode.aspx').content)
    f.close()
    img = Image.open('VCode.png').convert('L')
    ckcode = pytesseract.image_to_string(img)
    data = {'UserName':usrname,'UserPwd':pwd,'CheckCode':ckcode,'btnLogin':'登录'}
    r = s.post('http://jwc.nau.edu.cn/Login.aspx',data,timeout=60)
    if(stuid[0] == "1"):
        r = s.get('http://jwc.nau.edu.cn/StuPhotoView.ashx?t=1&stuid=' + stuid)
        f = open(stuid + '.jpg', 'wb')
        f.write(r.content)
        f.close()
        #img = Image.open(stuid + '.jpg')
        #img.show()
    return
if __name__=='__main__':
    #name = input()
    for i in range(17010001,17016666):
        print(i)
        get_photo(str(i))

i