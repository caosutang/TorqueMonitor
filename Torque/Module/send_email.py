import os 
import uuid
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

def get_data(path):
  img_dict = []
  all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
  for file in all_files:
        img_dict_single = dict(title=file[:-4:1], path=path +"/"+file, cid=str(uuid.uuid4()))
        img_dict.append(img_dict_single) 
  return img_dict 

def attach_image(img_dict):
  with open(img_dict['path'], 'rb') as file:
    msg_img = MIMEImage(file.read(), name = os.path.basename(img_dict['path']))
    msg_img.add_header('Content-ID', '<{}>'.format(img_dict['cid']))
    return msg_img

def generate_email(mail_user, to_list, img_path):
  subject = 'This is a email monitor torque data!'
  msg= MIMEMultipart('related')
  msg['Subject'] = subject
  msg['From'] = mail_user
  msg['To'] = ','.join(to_list)

  msgAlternative = MIMEMultipart('alternative')
  msg.attach(msgAlternative)
  hipot_img_dict = get_data(img_path + '/sim')
  il_img_dict = get_data(img_path + '/int')
  template = env.get_template('child.html')
  html = template.render(hipot_pictures=hipot_img_dict, il_pictures=il_img_dict)
  msgHtml = MIMEText(html, 'html')
  msgAlternative.attach(msgHtml)
  for img in hipot_img_dict:
    msg.attach(attach_image(img))
  for img in il_img_dict:
    msg.attach(attach_image(img))
  return msg

def send_email(msg, mail_user, mail_pwd, to_list, host,port):
  mailServer = SMTP(host, port)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  if mail_pwd != '':
    mailServer.login(mail_user, mail_pwd)
  mailServer.sendmail(mail_user, to_list, msg.as_string())
  mailServer.quit()
