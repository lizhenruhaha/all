#分析日志   发送邮件 (定时任务)
import os
import logging
import smtplib
from email.mime.text import MIMEText
from myfirst import settings
log_file='statistics.log'
logger=logging.getLogger('django')
def analyze_log():
    log_file_path=os.path.join(settings.BASE_DIR,log_file)
    if not log_file_path:
        logger.info('日志不存在')
        return
    result={}
    with open(log_file_path,'r',encoding='utf8') as f:
        for line in f:
            # print(line)
            line_dict=eval(line)
#             记录数据
            # 接口耗时多少 最高耗时多杀 最少耗时多少 出现多少次
            key=line_dict['path']
            if key in result:
                result[key][0]+=1 #第0位表示次数
                if line_dict['used_time'] < result[key][1]:
                    result[key][1] = line_dict['used_time']
                if line_dict['used_time'] > result[key][1]:
                    result[key][2] = line_dict['used_time']
                result[key][3]+=result[key][3]
            else:
                result[key]=['次数','最短耗时','最长耗时','总耗时']
                # 次数
                result[key][0]=1
                # 最短耗时
                result[key][1]=line_dict['used_time']
                # 最长耗时
                result[key][2] = line_dict['used_time']
                # 总耗时
                result[key][3] = line_dict['used_time']
        return result

def analyse():
    res = analyze_log()
    for key in res:
        res[key].append(res[key][3]/res[key][0])
    return res

def send_email():
    msg = MIMEText(repr(analyze_log()), "plain", "utf-8")
    msg['FROM'] = "2134933571@qq.com"
    msg['Subject'] = "【端口总计】"
    receivers = ['2134933571@qq.com']
    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_FROM, receivers, msg.as_string())
    server.close()
    pass
if __name__ == '__main__':
   send_email()
