# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_site_name, get_site_base_path
from frappe.utils import now_datetime, getdate, flt, cint, get_fullname

class SIMUpload(Document):
    def validate(self):
        self.get_file_info()

    def on_submit(self):
        if not self.sim_file:
            frappe.throw(_("Please upload SIM file."), title="Data Missing")
        else:
            self.create_sim_entry()

    def on_cancel(self):
        if cint(self.migration_data):
            frappe.throw(_("This is data migration entry and cannot be deleted."), title="Invalid Operation")
            
        self.remove_sim_entry()

    def remove_sim_entry(self):
        frappe.db.sql("delete from `tabSIM Entry` where sim_upload='{0}'".format(self.name))
        
    def create_sim_entry(self):
	counter = 0
	values = []
	flag = 0
	url = str(self.sim_file).split("/")
        file_path = str(self.sim_file)
        
        if u'private' not in url:
            file_path = '/public'+str(self.sim_file)
        file_path = str(get_site_base_path())+str(file_path)
        
	qry = """
        	insert into `tabSIM Entry`(name,imsi,iccid,pin1,puk1,pin2,puk2,eki,sim_upload,
                	owner,creation,modified,modified_by,idx,docstatus,sim_vendor
                ) values {0}
        """
	line_count = 0
	with open(file_path) as sim_file:
	    for line in sim_file:
		if str(line[:5]) == "40211":
		    line_count += 1
		    data = line.split(" ")
		    counter += 1
		    if counter <= 700:
			flag = 0
		    else:
			try: 
			    sql = qry.format(",".join(values))
			    frappe.db.sql(sql)
			except Exception, e:
			    frappe.throw(_("{0} {1} {2}").format(line_count, counter, str(e)))

			values = []
			counter = 1
			flag = 1
		
		    values.append(str(tuple([str(data[1])[:19].strip(),str(data[0]).strip(),str(data[1])[:19].strip(),
                            str(data[2]).strip(),str(data[3]).strip(),str(data[4]).strip(),str(data[5]).strip(),
                            str(data[6]).strip(),str(self.name).strip(),str(frappe.session.user).strip(),
                            str(now_datetime()).strip(),str(now_datetime()).strip(),str(frappe.session.user).strip(),
                            0,0,str(self.sim_vendor)])))

	if len(values) > 0 and not flag:
	    try:
		sql = qry.format(",".join(values))
		frappe.db.sql(sql)
            except Exception, e:
                frappe.throw(_("{0}").format(str(e)))

    def get_file_info(self):
        if not self.sim_file:
                self.sim_file_header = None
                self.noof_sim_entries = 0
                return
        
        counter = 0
        header = ""
        flag = 0
        noof_sim_entries = 0

        url = str(self.sim_file).split("/")
        file_path = str(self.sim_file)
        
        if u'private' not in url:
            file_path = '/public'+str(self.sim_file)
        file_path = str(get_site_base_path())+str(file_path)
        
        with open(file_path) as sim_file:
            for line in sim_file:
                counter += 1
                if str(line[:5]) == "40211":
                        flag = 1
                        noof_sim_entries += 1
                else:
                        if not flag:
                            header += "<div>"+str(line)+"</div>"
                        else:
                            frappe.throw(_("Row#{0} : Invalid SIM entry found <br/>{1}").format(counter,str(line)), title="Invalid SIM Entry")

        self.noof_sim_entries = noof_sim_entries
        self.sim_file_header = header
