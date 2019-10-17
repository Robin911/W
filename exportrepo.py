import pymysql
import pandas as pd
import smtplib
import time, os, sys
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

os.chdir(os.path.abspath(os.path.dirname(__file__)))
# 连接database
connection = pymysql.connect(host='10.10.10.1',
                             user='xx',
                             password='xx',
                             charset='utf8mb4')
mail_user = 'xxx@xxx.com'
mail_pass = 'xxxx'
export_date = time.strftime("%Y-%m-%d", time.localtime())


### xxx - xxxxxxxxxxxx - 2019-10-17
select * from table1;
"""]


### xxx
task_name_2 = ["""-- 全部用户的微信关注数据
se1ect script 1
""", """-- 全部用户的园区查看
select script 2
""", """-- 项目周报-项目维度
select script 3
""", """-- 项目沟通记录
select script 4
""", """-- 用户操作日志分析
select script 5
"""]


class Export:
    def __init__(self, sqls, mailto, subject):
        self.sqls = sqls
        self.filename = 'xlsx/' + export_date + '-' + subject + '.xlsx'
        self.mailto = mailto
        self.subject = subject

    def xlsx_export(self):
        excel = pd.ExcelWriter(self.filename)
        for sql in self.sqls:
            data = pd.read_sql(sql, connection)
            tab_name = sql.split('\n')[0]
            data.to_excel(excel, sheet_name=tab_name[3:])
        excel.save()

    def send_mail(self):
        try:
            msg = MIMEMultipart()
            msg.attach(MIMEText('Auto export data.', 'plain', 'utf-8'))
            attach_file = MIMEApplication(open(self.filename, 'rb').read())
            attach_file["Content-Type"] = 'application/octet-stream'
            attach_file["Content-Disposition"] = 'attachment; filename=%s-auto_export.xlsx' % export_date
#            attach_file.add_header("Content-Disposition", "attachment", filename=("utf8", "", export_date + 'auto_export.xlsx')
            msg['From'] = mail_user  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = self.mailto  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = self.subject  # 邮件的主题，也可以说是标题
            msg.attach(attach_file)

            server = smtplib.SMTP("smtp.qiye.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(mail_user, mail_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(mail_user, self.mailto.split(';'), msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:
            print(e)

    def run(self):
        self.xlsx_export()
        self.send_mail()

if __name__ == '__main__':
    everyday9 = Export(everyday9, 'evan.xu@paat.com;maggie.xiong@paat.com;tiffany.huang@paat.com;leo.chuang@paat.com;ran.li@paat.com;ailan.zhang@paat.com;Yiou.Wang@paat.com;Bo.Dong@paat.com;robin.wang@paat.com', '招商工作量化统计数据')
	talk = Export(task_name_2, 'user1@xxx.com;user2@xxx.com;user3@xxx.com', '邮件标题')
	talk = Export(task_name_2, 'user1@xxx.com;user2@xxx.com;user3@xxx.com', '邮件标题')

    for task in sys.argv[1:]:
         eval(task).run()
    connection.close()