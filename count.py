import hashlib,time,random,string,requests,base64
import cv2
import numpy as np
from urllib.parse import urlencode
import json
app_key = 'y133DFs0epGiuwHF'
app_id =  '1106879169'
def get_params(img):                         #鉴权计算并返回请求参数
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效
    time_stamp=str(int(time.time()))
    #请求随机字符串，用于保证签名不可预测,16代表16位
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    params = {'app_id':app_id,'image':img, 'mode':'0' , 'time_stamp':time_stamp, 'nonce_str':nonce_str}

    sort_dict= sorted(params.items(), key=lambda item:item[0], reverse = False)  #字典排序
    sort_dict.append(('app_key',app_key))   #尾部添加appkey
    rawtext= urlencode(sort_dict).encode()  #urlencod编码
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text= sha.hexdigest().upper()        #MD5加密计算
    params['sign']=md5text                  #将签名赋值到sign
    return  params                          #返回请求包

def test(i):
     dire ='D:\\1701\\'+str(i)+'.jpg'
     f = open(dire,'rb')
     img = base64.b64encode(f.read())  # 得到API可以识别的字符串
     params = get_params(img)  # 获取鉴权签名并获取请求参数
     url = "https://api.ai.qq.com/fcgi-bin/face/face_detectface"
     res = requests.post(url, params).json()
     count = res['data']['face_list'][0]['beauty']
     # if count>90 :
     print(i,count)
if __name__=='__main__':
    for i in range(17010001, 17010500):
        test(i)
