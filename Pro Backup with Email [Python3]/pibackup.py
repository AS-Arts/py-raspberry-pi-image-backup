#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Run this script only with python3

import datetime
import shutil
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# path to usb device 
usbdevice_path = "/media/usbdevice" 

# bigger than 1
number_of_image_files = "1" 

# Email address for sending 
email_from = "demo1@example.net" 

# Password form email address for sending 
email_from_pw = "password123" 

# smtp server form email address for sending 
smtp_host = "smtp.example.net"

# smtp port form email address for sending 
smtp_port = 587 

# E-mail address to receive the messages 
email_to = "demo2@example.net" 

# Name of the system
system_name = "My Raspi" 



before_sdcard = shutil.disk_usage("/")
before_sdcard_total = round(before_sdcard.total/1000000000, 2)
before_sdcard_used = round(before_sdcard.used/1000000000, 2)
before_sdcard_free = round(before_sdcard.free/1000000000, 2)

before_usbdevice = shutil.disk_usage(usbdevice_path)
before_free = round(before_usbdevice.free/1000000000, 2)


tstart = datetime.datetime.now().replace(microsecond=0)

if (before_sdcard.total < before_usbdevice.free) and (number_of_image_files >= "1") :
    log00 = (str(system_name) + " - New Backup")
    log01 = (str(tstart) + " Backup is running!")
    print (log01)

    createimg = "sudo dd if=/dev/mmcblk0 of=" + str(usbdevice_path) + "/pibackup-$(date +%Y%m%d-%H%M%S).img bs=1MB"
    os.system(createimg)

    after_usbdevice = shutil.disk_usage(usbdevice_path)
    after_free = round(after_usbdevice.free/1000000000, 2)

    deleteimg = "sudo pushd " + str(usbdevice_path) + "; ls -tr " + str(usbdevice_path) + "/pibackup* | head -n -" + str(number_of_image_files) + " | xargs rm; popd"
    os.system(deleteimg)

    tend = datetime.datetime.now().replace(microsecond=0)    
    log02 = (str(tend) + " Backup is finished!")
    print (log02)
            
else:
    log00 = (str(system_name) + " - Backup ERROR!")
    log01 = (str(tstart) + " The backup could not be created!")
    log02 = (str(tstart) + " Check the USB device!")
    tstart = 0
    tend = 0
    after_free = before_free
    print (log01)
    print (log02)

now_usbdevice = shutil.disk_usage(usbdevice_path)
now_total = round(now_usbdevice.total/1000000000, 2)
now_used = round(now_usbdevice.used/1000000000, 2)
now_free = round(now_usbdevice.free/1000000000, 2)

storage = ("<style>table {border-collapse: collapse;font-size:14px;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}</style><table><tr><th>Storage</th><th>Total</th><th>Used</th><th>Free</th></tr><tr><td>SD-Card</td><td>" + str(before_sdcard_total) + " GB</td><td>" + str(before_sdcard_used) + " GB</td><td>" + str(before_sdcard_free) + " GB</td></tr><tr><td>External</td><td>" + str(now_total) + " GB</td><td>" + str(now_used) + " GB</td><td>" + str(now_free) + " GB</td></tr></table>")
 
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = log00 
msg.attach(MIMEText(str(log00) + "<br /><br />" + str(log01) + "<br />" + str(log02) + "<br /><br /><br />Time: " + str(tend - tstart) + " | Size : " + str(round(before_free - after_free, 2)) + " GB<br /><br /><br />" + str(storage) + "<br /><br />Backup Pro by Andreas Schmidt", 'html'))
server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(email_from, email_from_pw)
text = msg.as_string()
server.sendmail(email_from, email_to, text)
server.quit()	


