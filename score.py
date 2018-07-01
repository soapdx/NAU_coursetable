import requests,pytesseract
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
def get_score(name):
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

    data1 = {'searchType': 'stuName','key': name}
    r = s.post('http://jwc.nau.edu.cn/JwAdmin/StuLearnInfoView.aspx',data1)
    idx1 = r.text.find('<td>'+name+'</td>')
    idx2 = r.text.find('班</td>')
    stucla = r.text[idx1+31+len(name):idx2+1]

    data2 = {'ClassName': stucla,'Term': '201720182'}
    r = s.post('http://jwc.nau.edu.cn/Servlet/GetClassScoreListForWebRequest.ashx',data2)
    #print(r.text)
    return r.text

if __name__=='__main__':
    stu = input()
    score='0'
    while score[0]!='[':
      score = get_score(stu).replace('\'','\"')
    #print(score)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df = pd.read_json(score)
    #print(df)
    del df['Term']
    df = df.loc[(df['StuName'] == stu)]

    print(df)
