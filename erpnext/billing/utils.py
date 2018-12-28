# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
# Module: billing

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate, get_datetime, get_url, nowdate, now_datetime, money_in_words
import bscs_utils
from frappe.desk.tags import DocTags
import time
import logging

def add_service_item():
    for s in frappe.db.sql("select name from `tabService`", as_dict=True):
        doc = frappe.get_doc("Service", s.name)
        
        # 2 Weeks before
        row = doc.append("items",{})
        row.action_type   = 'Notify'
        row.action_method = 'Before Service Expiry'
        row.action_days   = 14
        row.notify_customer = 1
        row.notify_internal = 1
        row.save()
        
        # Month before
        row = doc.append("items",{})
        row.action_type   = 'Notify'
        row.action_method = 'Before Service Expiry'
        row.action_days   = 30
        row.notify_customer = 1
        row.notify_internal = 1
        row.save()
        
def testmail():
    frappe.sendmail(recipients=['siva@bt.bt'],subject="Mail with Delayed TRUE",message="Delayed FALSE",delayed=True)
    print 'Delayed TRUE: Mail sent successfully...'
    frappe.sendmail(recipients=['siva@bt.bt'],subject="Mail with Delayed FALSE",message="Delayed FALSE",delayed=False)
    print 'Delayed FALSE: Mail sent successfully...'
    
def create_tags(dt, dn, dv, updated_on):
    DocTags(dt).remove_all(dn)
    DocTags(dt).add(dn,"Synced "+str(updated_on))
    DocTags(dt).add(dn,"All")
    if dv:
        DocTags(dt).add(dn,dv)
                    
def get_service_list():
    slist = frappe.db.sql_list("select name from `tabService`")
    return tuple(str(i) for i in slist)

def sync_db():
    log = []
    base_time = time.time()
    start_time= ""

    # Logging
    logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    for i in ['sync_customers', 'sync_contract', 'sync_contract_service']:
        logger.info("|".join(str(j) for j in ['Executing',i]))
        start_time = base_time if not start_time else time.time()
        globals()[i]()
        end_time = time.time()
        log.append([i,time.strftime("%H:%M:%S", time.gmtime(end_time-start_time)),time.strftime("%H:%M:%S", time.gmtime(end_time-base_time))])

    for l in log:
        logger.info(" ".join(str(j) for j in [l[0],'Time elapsed:',l[1],'Time elapsed overall:',l[2]]))
    
def remove_all():
    remove_customers()
    remove_contract()
    remove_contract_service()
    
def sync_contract():
    bscs = bscs_utils.db()
    sql = bscs_utils.query["contract"].format(get_service_list())
    result = bscs.sql(sql)
    dt = "Contract"

    # Logging
    logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
        
    counter    = 0
    updated_on = now_datetime().strftime("%Y-%m-%d %H:%M:%S")
    for row in result:
        counter   += 1
        if not frappe.db.exists(dt, str(row[0])):
            doc = frappe.new_doc(dt)
            msg = "Created"
        else:
            doc = frappe.get_doc(dt, str(row[0]))
            msg = "Updated"

        if doc:
            try:
                doc.co_id          = str(row[0])
                doc.co_code        = row[1]
                doc.customer_id    = str(row[2])
                doc.contract_status= row[3]
                doc.co_installed   = str(row[4])
                doc.co_moddate     = str(row[5])
                doc.dn_id          = str(row[6])
                doc.dn_num         = str(row[7])
                doc.dn_status      = row[8]
                doc.save()

                create_tags(dt,doc.co_id,doc.contract_status,updated_on)
                logger.info("|".join(str(i) for i in ["SUCCESS",counter,row[2],row[0],row[1],dt,msg]))
            except Exception, e:
                logger.exception("|".join(str(i) for i in ["FAILED",counter,row[2],row[0],row[1],dt,msg]))
    bscs.close()

def sync_contract_service():
    bscs = bscs_utils.db()
    sql = bscs_utils.query["contract_service"].format(get_service_list())
    result = bscs.sql(sql)
    dt = "Contract Service"

    # Logging
    logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    counter    = 0
    updated_on = now_datetime().strftime("%Y-%m-%d %H:%M:%S")
    for row in result:
        counter += 1
        if not frappe.db.exists(dt, str(row[0])):
            doc = frappe.new_doc(dt)
            msg = "Created"
        else:
            doc = frappe.get_doc(dt, str(row[0]))
            msg = "Updated"

        if doc:
            try:
                doc.transaction_id = str(row[0])
                doc.co_id          = str(row[1])
                doc.customer_id    = str(row[2])
                doc.sncode         = str(row[3])
                doc.des            = str(row[4])
                doc.service_status = str(row[5])
                doc.valid_from_date= str(row[6])
                doc.save()
                create_tags(dt,doc.transaction_id,doc.service_status,updated_on)
                logger.info("|".join(str(i) for i in ["SUCCESS",counter,row[2],row[1],row[0],dt,msg]))
            except Exception, e:
                logger.exception("|".join(str(i) for i in ["FAILED",counter,row[2],row[1],row[0],dt,msg]))

    bscs.close()
        
def sync_service():
    bscs = bscs_utils.db()
    sql = bscs_utils.query["service"].format(get_service_list())
    result = bscs.sql(sql)
    
    counter = 0
    for row in result:
        counter += 1
        if not frappe.db.exists("Service", str(row[0])):
            doc = frappe.new_doc("Service")
            msg = "Created"
        else:
            doc = frappe.get_doc("Service", str(row[0]))
            msg = "Updated"

        if doc:
            try:
                doc.sncode = str(row[0])
                doc.des    = str(row[1])
                doc.shdes  = str(row[2])
                doc.save()
                print counter,"Service ",row[0],row[1],msg," Successfully."
            except Exception, e:
                print row[0], "ERROR:", str(e)

    bscs.close()
    
def remove_customers():
    counter = 0
    for i in frappe.db.sql("select name, customer_code from `tabCustomers`", as_dict=1):
        counter += 1
        doc = frappe.get_doc("Customers", i.name)
        doc.delete()
        print counter, i.name, i.customer_code, " Customer Removed Successfully..."

def remove_contract():
    counter = 0
    for i in frappe.db.sql("select name, customer_id from `tabContract`", as_dict=1):
        counter += 1
        doc = frappe.get_doc("Contract", i.name)
        doc.delete()
        print counter, i.customer_id, i.name, " Contract Removed Successfully"

def remove_contract_service():
    counter = 0
    for i in frappe.db.sql("select name, customer_id from `tabContract Service`", as_dict=1):
        counter += 1
        doc = frappe.get_doc("Contract Service", i.name)
        doc.delete()
        print counter, i.customer_id, i.name, " Contract Service Removed Successfully"
    
def sync_customers():
    counter    = 0
    updated_on = now_datetime().strftime("%Y-%m-%d %H:%M:%S")
    bscs = bscs_utils.db()
    dt = "Customers"

    # Logging
    logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    for ct in ["customers","large_customers"]:
        if ct == "large_customers":
            sql = bscs_utils.query[ct].format(get_service_list())
            msg2= "Large"
        else:
            sql = bscs_utils.query[ct].format(get_service_list())
            msg2= ""
            
        result = bscs.sql(sql)
        for row in result:
            counter += 1
            msg = ""
            
            if not frappe.db.exists(dt, str(row[0])):
                doc = frappe.new_doc(dt)
                msg = "Created"
            else:
                doc = frappe.get_doc(dt, str(row[0]))
                msg = "Updated"
                    
            if doc:
                try:
                    doc.customer_id     = str(row[0])
                    doc.customer_code   = str(row[1])
                    doc.customer_status = row[2] if row[2] else None
                    doc.customer_type   = row[3] if row[3] else None
                    doc.gender          = row[5] if row[5] else None
                    doc.company_name    = row[6] if row[6] else None
                    doc.first_name      = row[7] if row[7] else None
                    doc.last_name       = row[8] if row[8] else None
                    doc.email_id        = row[9] if row[9] else None
                    doc.contact1        = row[10] if row[10] else None
                    doc.street_no       = row[11] if row[11] else None
                    doc.street          = row[12] if row[12] else None
                    doc.address1        = row[13] if row[13] else None
                    doc.address2        = row[14] if row[14] else None
                    doc.address3        = row[15] if row[15] else None
                    doc.city            = row[16] if row[16] else None
                    doc.country         = row[18] if row[18] else None
                    doc.bill_cycle      = row[19] if row[19] else None
                    doc.customer_id_high= str(row[20]) if row[20] else None
                    doc.cscurbalance    = row[21]
                    doc.last_updated_on = now_datetime()
                    doc.root_customer   = 1 if ct == "large_customers" else 0
                    doc.save()

                    create_tags(dt,doc.customer_id,doc.customer_status,updated_on)
                    logger.info("|".join(str(i) for i in ["SUCCESS",counter,row[0],row[1],msg2,dt,msg]))
                except Exception, e:
                    logger.exception("|".join(str(i) for i in ["FAILED",counter,row[0],row[1],msg2,dt,msg]))

    bscs.close()
