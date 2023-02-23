import uuid
from datetime import datetime, timedelta

calendar_name = 'events.ics'
def create_ics_file(events,calendar_name):
  # 生成ics文件头部信息
  ics_file = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\n'

  # 循环生成每个事件的ics信息
  for event in events:
    # 生成事件唯一标识符
    event_uid = uuid.uuid4().hex

    # 生成事件开始和结束时间
    start_time = event['start_time']
    end_time = event['end_time']

    # 生成事件的ics信息
    ics_event = f'BEGIN:VEVENT\nUID:{event_uid}\nDTSTAMP:{datetime.now().strftime("%Y%m%dT%H%M%SZ")}\nDTSTART:{start_time.strftime("%Y%m%dT%H%M%S")}\nDTEND:{end_time.strftime("%Y%m%dT%H%M%S")}\nSUMMARY:{event["summary"]}\nDESCRIPTION:{event["description"]}\nLOCATION:{event["location"]}\nEND:VEVENT\n'

    # 将事件信息添加到ics文件中
    ics_file += ics_event

  # 添加ics文件尾部信息
  ics_file += 'END:VCALENDAR\n'

  # 将ics文件保存到本地
  with open(calendar_name, 'w', encoding='utf-8') as f:
    f.write(ics_file)


path = 'info.txt'
with open(path,'r',encoding='utf-8') as f:
  contents = f.readlines()
  # 从非注释行开始
  structs = []
  for content in contents[1:]:
    sub_dict = {}
    con_list = content.split(' ')
    # 课程
    sub_dict['summary'] = con_list[0].split(']')[1]
    # 老师
    sub_dict['description'] = con_list[1]
    # 周数
    weeks = con_list[2]
    if '-' in weeks:
      sub_dict['week_start'] = int(weeks.split('-')[0])
      sub_dict['week_end'] = int(weeks.split('-')[1])
    else:
      sub_dict['week_start'] = int(weeks)
      sub_dict['week_end'] = int(weeks)
    # 日程
    schedule = con_list[3]
    sub_dict['week_time'] = schedule[0]
    # 默认只上两节（一单）课
    sub_dict['start_course'] = schedule[2]
    if schedule[-1] == "单":
      sub_dict['step'] = 2
      sub_dict['week_parity'] = 0
    elif schedule[-1] == "双":
      sub_dict['step'] = 2
      sub_dict['week_parity'] = 1
    else:
      sub_dict['step'] = 1
      sub_dict['week_parity'] = 0
    # 位置
    sub_dict['location'] = con_list[4]

    structs.append(sub_dict)
  print(structs)

events = []
# 课程遍历
for struct in structs:
  # 周数遍历
  days = -1
  for week in range(struct['week_start']+struct['week_parity'],struct['week_end']+1,struct['step']):
    sub_dict2 = {}
    # 周的累计
    days += 7*(week-1)
    # 周具体时间修改
    if struct['week_time'] == '一':
      days += 1
    elif struct['week_time'] == '二':
      days += 2
    elif struct['week_time'] == '三':
      days += 3
    elif struct['week_time'] == '四':
      days += 4
    elif struct['week_time'] == '五':
      days += 5
    elif struct['week_time'] == '六':
      days += 6
    elif struct['week_time'] == '日':
      days += 7
    # 教学楼时间修改
    if struct['location'][0] in 'CDEFJM':
      # 时段修改
      if struct['start_course'] == '1':
        hours = 0
        minutes = 0
      elif struct['start_course'] == '3':
        hours = 2
        minutes = 10
      elif struct['start_course'] == '5':
        hours = 5
        minutes = 20
      elif struct['start_course'] == '7':
        hours = 7
        minutes = 30
      elif struct['start_course'] == '9':
        hours = 9
        minutes = 50
      elif struct['start_course'] == '11':
        hours = 11
        minutes = 40
      sub_dict2['start_time'] = datetime(2023, 2, 28, 8, 10, 0)+timedelta(days=days,minutes=minutes,hours=hours)
      sub_dict2['end_time'] = sub_dict2['start_time']+timedelta(minutes=30,hours=1)
      sub_dict2['summary'] = struct['summary']
      sub_dict2['description'] = struct['description']
      sub_dict2['location'] = struct['location']
    else:
      if struct['start_course'] == '1':
        hours = 0
        minutes = 0
      elif struct['start_course'] == '3':
        hours = 2
        minutes = 0
      elif struct['start_course'] == '5':
        hours = 5
        minutes = 20
      elif struct['start_course'] == '7':
        hours = 7
        minutes = 20
      elif struct['start_course'] == '9':
        hours = 10
        minutes = 0
      elif struct['start_course'] == '11':
        hours = 11
        minutes = 50
      sub_dict2['start_time'] = datetime(2023, 2, 28, 8, 0, 0)+timedelta(days=days,minutes=minutes,hours=hours)
      sub_dict2['end_time'] = sub_dict2['start_time']+timedelta(minutes=30,hours=1)
      sub_dict2['summary'] = struct['summary']
      sub_dict2['description'] = struct['description']
      sub_dict2['location'] = struct['location']
    events.append(sub_dict2)
    # 结束一周，days归位
    days = -1
create_ics_file(events,calendar_name)