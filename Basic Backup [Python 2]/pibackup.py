#!/usr/bin/python
# -*- coding: utf-8 -*-

# Run this script only with python2

import os

print "Backup is running!"
createimg = 'sudo dd if=/dev/mmcblk0 of=/media/usbdevice/pibackup-$(date +%Y%m%d-%H%M%S).img bs=1MB'
os.system(createimg)

deleteimg = 'sudo pushd /media/usbdevice; ls -tr /media/usbdevice/pibackup* | head -n -1 | xargs rm; popd'
os.system(deleteimg)
    
print "Backup is finished!"