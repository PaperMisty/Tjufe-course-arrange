# encoding:utf-8
import requests
import base64
import pandas as pd

# 利用百度识别api识别图片文本信息
def ocr_course(path):
  # client_id 为官网获取的AK， client_secret 为官网获取的SK
  host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=CyPGn6Z0tCOxG747tru6KRb9&client_secret=2Fr6y4W5Gezp6H2RHt6OVx6uEXUuOOUz'
  tokens = requests.get(host).json()

  request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
  # 二进制方式打开图片文件 
  f = open(path, 'rb')
  img = base64.b64encode(f.read())
  # 定义申请识别的参数
  params = {"image":img}
  access_token = tokens['access_token']
  request_url = request_url + "?access_token=" + access_token
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  # 获取识别结果
  response = requests.post(request_url, data=params, headers=headers)
  return response

# 自定义文本纠正
def week_fix(str):
  if str[0] == '-' or str[0] == '~':
    str = '一'+str[1:]
  if str[-1] == '欢':
    str = str[:-1]+'双'
  return str

# 将识别结果输入到info.txt
def info_format(response):
  if response:
    seq = ''
    information = ''
    for item in response.json()['words_result']:
      information += item['words']+' '+seq
      # 将结果整理分开
      if seq == '\n':
        seq = ''
      if "节" in item['words']:
        seq = '\n'
  else:
    return None
  #df = pd.read_excel('info.xlsx','w',sheet_name='Sheet1')
  with open('info.txt','w',encoding='utf-8') as f:
    f.write("#示例(除了XXX其余都需要仔细校对)：")
    f.write("XXXXXXXXX]课程名字 老师名字 1-17 二[5XXX]双 N3218"+'\n')
    content = ''
    tmp = ''
    for i in information:
      if i != '\n':
        # 把每行内容累积起来
        content += i
      else:
        # 换行，写入文本文件
        info_list = content.split(' ')
        # 自定义纠正
        info_list[-3] = week_fix(info_list[-3])
        # 如果这条是上一课程信息的续写，
        if len(info_list) < 6:
          f.write(tmp+' '+info_list[-4]+' '+info_list[-3]+' '+info_list[-2]+' '+'\n')
        # 如果这是新的课程
        else:
          f.write(info_list[1]+' '+info_list[-5]+' '+info_list[-4]+' '+info_list[-3]+' '+info_list[-2]+' '+'\n')
          # 将这次部分内容暂存，供下次可能的使用
          tmp = info_list[1]+' '+info_list[-5]
        
        content = ''
#info_format(response)     


