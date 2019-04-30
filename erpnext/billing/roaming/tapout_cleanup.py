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
ftp_host = config.get('credentials', 'dch_tapo_host')
ftp_usr = config.get('credentials', 'dch_tapo_usr')
ftp_pwd = config.get('credentials', 'dch_tapo_pwd')

def backup(pathname):
    backup_path = config.get('directories', 'tap_out_backup').rstrip("/")
    backup_path = os.path.join(backup_path, time.strftime("%Y%m%d", time.localtime(os.stat(pathname).st_mtime)))
    try:
        if not os.path.isdir(backup_path):
            os.makedirs(backup_path)

        os.rename(str(pathname), os.path.join(backup_path,os.path.basename(pathname)))
        print datetime.datetime.now(),'|',os.path.basename(pathname),'|','Moved to folder {0}'.format(os.path.basename(backup_path)),'|','tapout_cleanup'
    except Exception, e:
        print datetime.datetime.now(),'|',os.path.basename(pathname),'|','ERROR MOVING FILE','|','tapout_cleanup',str(e)

def cleanup_backup():
    backup_path = config.get('directories', 'tap_out_backup').rstrip("/")
    folder_path = ""
    for filename in os.listdir(backup_path):
        if os.path.isfile(os.path.join(backup_path, filename)):
            folder_path = os.path.join(backup_path, time.strftime("%Y%m%d", time.localtime(os.stat(os.path.join(backup_path,filename)).st_mtime)))
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)
            os.rename(str(os.path.join(backup_path,filename)),str(os.path.join(folder_path,filename)))
                
def cleanup():
    path = config.get('directories', 'tap_out').rstrip('/')
    pathname = ""
    try:
        with ftputil.FTPHost(ftp_host, ftp_usr, ftp_pwd) as ftp_target:
            files = os.listdir(path)
            for filename in files:
                if os.path.isfile(os.path.join(path,filename)):
                    for pf in [i.strip(" ") for i in config.get('prefix', 'tap_out_prefix').split(",")]:
                        if filename.startswith(pf):
                            if filename.find(".") > 0:
                                filename = filename[0:filename.find(".")]

                            fullpath = os.path.join(path,filename)
                            
                            if os.stat(fullpath).st_mtime < (time.time() - (5*60)):
                                ftp_target.upload(fullpath,filename)
                                print datetime.datetime.now(),'|',filename,'|','FTP Successful','|','tapout_cleanup'
                                backup(fullpath)
                            break
                    else:
                        print datetime.datetime.now(),'|',filename,'|','PREFIX not supported','|','tapout_cleanup'
    except Exception, e:
        print datetime.datetime.now(),'|',os.path.basename(pathname),'|','FTP Failed','|','tapout_cleanup',str(e)

    cleanup_backup()        

if __name__ == '__main__':
    schedule.every(5).minutes.do(cleanup)
    while True:
        # Check whether a schedule task is pending to run or not
        schedule.run_pending()
        time.sleep(1)
