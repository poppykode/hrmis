import random
import string
import datetime
from accounts.models import User
from app_settings.models import BlockedSite
from django.core.mail import EmailMessage

host_path ='C:\Windows\System32\drivers\etc\hosts'
ip_address = '127.0.0.1'

def generate_employee_id(size=4, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    year  = str(datetime.date.today().year)
    employee_id = 'HRMIS' + year + the_id
    try:
        User.objects.get(employee_id=employee_id)
        generate_employee_id()
    except:
        return employee_id  


def generate_password():
    gen_pass = User.objects.make_random_password()
    return gen_pass

def send_password_and_username(username, email, password):
    try:
        subject = 'Account Creation for HRMIS'
        recipient_list = [email, ]
        email_body = """\
        <html>
        <head> </head>
        <body>
            <h2>New Account Details</h2>
            <p>URL: <a href='http://127.0.0.1:8000/accounts/login/?next=/redirect'>Login in</a></p>
            <p>Employee ID: %s</p>
            <p>Password: %s</p>
        </body>
        </html>
        """ % (username, password,)
        mail = EmailMessage(
            subject,
            email_body,
            'HRMIS',
            recipient_list,
        )
        mail.content_subtype = "html"
        mail.send()
    except Exception as e:
        print(e)

def Blocker():
  website_lists = BlockedSite.objects.all()
  with open (host_path , 'r+') as host_file:
   file_content = host_file.read()
   for web in website_lists:
    if web.link in file_content:
       pass
    else:
       host_file.write(ip_address + " " + web.link + '\n')

def Unblocker():
    website_lists = BlockedSite.objects.all()
    with open (host_path , 'r+') as host_file:
     file_content = host_file.readlines()
    for web in website_lists:
      if web.link in website_lists:
       with open (host_path , 'r+') as f:
        for line in file_content:
            if line.strip(',') != website_lists:
                f.write(line)
                pass
            else:
                pass

def UnBlock():
    website_list = BlockedSite.objects.all()
    with open(host_path, 'r+') as file:   
        content=file.readlines()
        file.seek(0)
        for line in content:
            if not any(website.link in line for website in website_list):
                file.write(line)
        # removing hostnmes from host file
        file.truncate()

def send_board_messages(title):
    email = []
    qs = User.objects.filter(designation='employee')
    for email_addr in qs:
       email.append(email_addr.email)     
    try:
        subject = 'New Board Message'
        recipient_list = email
        email_body = """\
        <html>
        <head> </head>
        <body>
            <p>Board Title: %s</p>
            <p>Date Created: %s</p>
        </body>
        </html>
        """ % (title,  str(datetime.date.today()))
        mail = EmailMessage(
            subject,
            email_body,
            'HRMIS',
            recipient_list,
        )
        mail.content_subtype = "html"
        mail.send()
    except Exception as e:
        print(e)

def send_task_messages(project,title, dates,email,subject):
    email = [email,]  
    try:
        subject = subject
        recipient_list = email
        email_body = """\
        <html>
        <head> </head>
        <body>
            <p>Project: %s</p>
            <p>Task Title: %s</p>
            <p>Task Dates: %s</p>
        </body>
        </html>
        """ % (project,title, dates)
        mail = EmailMessage(
            subject,
            email_body,
            'HRMIS',
            recipient_list,
        )
        mail.content_subtype = "html"
        mail.send()
    except Exception as e:
        print(e)