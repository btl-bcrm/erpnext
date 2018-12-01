# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
# Module: billing

from __future__ import unicode_literals
import frappe
from frappe import _
import bscs_utils

def fetch_services():
    bscs = bscs_utils.db()
    sql = bscs_utils.query["service"]
    result = bscs.sql(sql)
    
    counter = 0
    for row in result:
        counter += 1
        if not frappe.db.exists("Service",row[0]):
            doc = frappe.new_doc("Service")
            doc.sncode = row[0]
            doc.des = row[1]
            doc.shdes = row[2]
            doc.save()
            print counter, row[0], row[1], row[2],' Created Successfully...'
        else:
            print counter, row[0],row[1],' Already exists...'

    bscs.close()
    
def remove_customer_info():
    counter = 0
    for i in frappe.db.sql("select name, customer_code from `tabCustomers`", as_dict=1):
        counter += 1
        doc = frappe.get_doc("Customers", i.name)
        doc.delete()
        print counter, i.name, i.customer_code, " Removed Successfully..."
    
def sync_customer_info():
    bscs = bscs_utils.db()
    sql = bscs_utils.query["customer"]
    result = bscs.sql(sql)
    
    counter = 0
    for row in result:
        counter += 1
        msg = ""
        
        if not frappe.db.exists("Customers", str(row[0])):
            doc = frappe.new_doc("Customers")
            msg = "Created"
        else:
            doc = frappe.get_doc("Customers", str(row[0]))
            msg = "Updated"
            
        if doc:
            try:
                doc.customer_code   = str(row[0])
                doc.customer_id     = str(row[1])
                doc.customer_status = row[2]
                doc.customer_type   = row[3]
                doc.gender          = row[5]
                doc.company_name    = row[6]
                doc.first_name      = row[7]
                doc.last_name       = row[8]
                doc.email_id        = row[9]
                doc.contact1        = row[10]
                doc.street_no       = row[11]
                doc.street          = row[12]
                doc.address1        = row[13]
                doc.address2        = row[14]
                doc.address3        = row[15]
                doc.city            = row[16]
                doc.country         = row[18]
                doc.bill_cycle      = row[19]
                doc.save()
                
                print counter, "Customer", row[0], msg, "Successfully..."    
            except Exception, e:
                print row[0], "ERROR:", str(e)

    print 'Fresh...'
    result = bscs.sql(sql)
    
    counter = 0
    for row in result:
        counter += 1
        print counter, "TRY2", row[0]
        
    bscs.close()
