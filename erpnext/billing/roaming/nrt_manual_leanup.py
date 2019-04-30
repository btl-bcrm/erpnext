# -*- coding: utf-8 -*-

import os, sys, time, shutil
from ConfigParser import SafeConfigParser
import pyinotify
import ftputil
import subprocess
import datetime
import hashlib
import schedule

config = SafeConfigParser()
config.read("/home/frappe/erp/apps/erpnext/erpnext/billing/roaming/config.ini")
ftp_host = config.get('credentials', 'dch_nrt_host')
ftp_usr = config.get('credentials', 'dch_nrt_usr')
ftp_pwd = config.get('credentials', 'dch_nrt_pwd')

def cleanup_backup():
    backup_path = config.get('directories', 'nrt_out_backup').rstrip("/")
    print 'backup_path', backup_path
    folder_path = ""
    for filename in os.listdir(backup_path):
        if os.path.isfile(os.path.join(backup_path, filename)):
            print "**********",filename
            folder_path = os.path.join(backup_path, time.strftime("%Y%m%d", time.localtime(os.stat(os.path.join(backup_path,filename)).st_mtime)))
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)
                print "os.makedirs({0})".format(folder_path)
            os.rename(str(os.path.join(backup_path,filename)),str(os.path.join(folder_path,filename)))    
            print "os.rename({0},{1})".format(str(os.path.join(backup_path,filename)),str(os.path.join(folder_path,filename)))
if __name__ == '__main__':
    cleanup_backup()
