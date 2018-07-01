import requests,pytesseract
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import info_one as info
def get_Id(name):
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
    #print(r.status_code)
    data1 = {'searchType': 'stuName','key': name}
    r = s.post('http://jwc.nau.edu.cn/JwAdmin/StuLearnInfoView.aspx',data1)
    #print(r.text)
    idx = r.text.find('currentStuID')
    stuid = r.text[idx+13:idx+21]
    #stuid = '16010666'
    if(stuid[0] == "1"):
        r = s.get('http://jwc.nau.edu.cn/StuPhotoView.ashx?t=1&stuid=' + stuid)
        f = open(stuid + '.jpg', 'wb')
        f.write(r.content)
        f.close()
        img = Image.open(stuid + '.jpg')
        img.show()
    return stuid
if __name__=='__main__':
    name = input()
    id = get_Id(name)
    while id[0] != "1":
        id = get_Id(name)
    print(id)
    print(info.getPwd(id))
