# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
from ConfigParser import SafeConfigParser
import pyinotify
import ftputil
import subprocess
import datetime

config = SafeConfigParser()
config.read("/home/frappe/erp/apps/erpnext/erpnext/billing/roaming/config.ini")
ftp_host = config.read('credentials', 'dch_nrt_host')
ftp_usr = config.read('credentials', 'dch_nrt_usr')
ftp_pwd = config.read('credentials', 'dch_nrt_pwd')

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        print datetime.datetime.now(),'|',os.path.basename(event.pathname),'|','process_IN_CLOSE_WRITE'
        for pf in [i.strip(" ") for i in config.get('prefix', 'nrt_out_prefix').split(",")]:
            if os.path.basename(event.pathname).startswith(pf):
                if self.upload(event.pathname):
                    self.backup(event.pathname)
                break
        else:
            print datetime.datetime.now(),'|',os.path.basename(event.pathname),'|','PREFIX not supported'

    def backup(self, pathname):
        backup_path = config.get('directories', 'nrt_out_backup').rstrip("/")

        try:
            if not os.path.isdir(backup_path):
                os.makedirs(backup_path)

            os.rename(str(pathname), str(backup_path+"/"+os.path.basename(pathname)))
            print datetime.datetime.now(),'|',os.path.basename(pathname),'|','Moved to folder {0}'.format(os.path.basename(backup_path))
        except Exception, e:
            print datetime.datetime.now(),'|',os.path.basename(pathname),'|','ERROR MOVING FILE',str(e)

    def upload(self, pathname):
        try:
            with ftputil.FTPHost(ftp_host, ftp_usr, ftp_pwd) as ftp_target:
                if ftp_target.upload_if_newer(str(pathname),str(os.path.basename(pathname))):
                    print datetime.datetime.now(),'|',os.path.basename(pathname),'|','FTP Successful'
                else:
                    print datetime.datetime.now(),'|',os.path.basename(pathname),'|','FTP Failed'
                    return False
        except Exception, e:
            print datetime.datetime.now(),'|',os.path.basename(pathname),'|','FTP Failed',str(e)
            return False
        return True
    
def main():
    path = config.get('directories', 'nrt_out')

    # watch manager
    wm = pyinotify.WatchManager()
    mask = pyinotify.ALL_EVENTS
    wm.add_watch(path, mask, rec=True, auto_add=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__=='__main__':
    main()
