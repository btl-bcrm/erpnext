# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.desk.tags import DocTags
from frappe.core.doctype.communication import email
from frappe.utils import flt, cint, getdate, get_datetime, get_url, nowdate, now_datetime, \
     money_in_words, add_days, add_months, add_years

class WorkOrder(Document):
        def validate(self):
                self.update_title()
                self.update_status()
                pass

        def on_update(self):
                self.update_tags()
                
        def on_submit(self):
                pass
        
        def on_cancel(self):
                if self.order_status not in ('Billing Cancelled','Systems Cancelled'):
                        self.db_set('order_status','Cancelled')

        def update_title(self):
                if not self.order_title:
                        if self.order_type == "Notification":
                                self.order_title = (str(self.action_days)+"days" if self.action_days else "")+" "+str(self.action_method)
                        else:
                                self.order_title = "Service Disconnection" if self.action_method == "After Service Expiry" else self.action_method
                                
                self.document_title = (str(self.customer_code)+" " if self.customer_code else "") + self.order_title
        
        def update_status(self):
                if self.order_status == 'Closed':
                        self.docstatus = 1
                elif self.order_status in ('Billing Cancelled','Systems Cancelled'):
                        self.docstatus = 2
                else:
                        self.docstatus = 0

                # Send Email alerts
                self.send_email_alerts()

        def get_customer_service_table(self):
                cust_info = []
                service_info = []
                table_th = ""
                table_td = ""
                msg = ""
                
                # Customer Information
                if self.customers:
                        doc = frappe.get_doc("Customers", self.customers)
                        if self.customer_code:
                                cust_info.append("Customer Code: "+str(self.customer_code)+"<br/>")
                        if self.company_name:
                                cust_info.append(self.company_name)
                        if self.first_name and self.first_name != self.company_name and self.first_name != self.last_name:
                                cust_info.append(self.first_name)
                        if self.last_name and self.last_name != self.company_name and self.last_name != self.first_name:
                                cust_info.append(self.last_name)
                        if doc.street_no:
                                cust_info.append(doc.street_no)
                        if doc.street:
                                cust_info.append(doc.street)
                        if doc.city:
                                cust_info.append(doc.city)
                        if doc.country:
                                cust_info.append(doc.country)
                        if doc.address1:
                                cust_info.append(doc.address1)
                        if doc.address2:
                                cust_info.append(doc.address2)
                        if doc.address3:
                                cust_info.append(doc.address3)
                        if doc.email_id:
                                cust_info.append(doc.email_id)
                        if doc.contact1:
                                cust_info.append(doc.contact1)
                        if doc.contact2:
                                cust_info.append(doc.contact2)

                        cust_info = "<br/>".join(cust_info)

                # Service Information
                if self.service:
                        if self.first_name:
                                service_info.append(self.first_name)
                        if self.des:
                                service_info.append("<b>Package:</b> "+str(self.des))
                        if self.price:
                                service_info.append("<b>Price:</b> "+str(self.currency)+". "+str(frappe.format_value(self.price, {"fieldtype":"Currency"}))+"/-")
                        if self.valid_from_date:
                                service_info.append("<br/><b>Activation Date:</b> "+str(self.valid_from_date))
                        if self.expiry_date:
                                service_info.append('<b style="color: FF4500;">Expiry Date: '+str(str(self.expiry_date))+'</b>')
                        service_info = "<br/>".join(service_info)
                                
                # Email body
                table_th += '<th style="border: 1px solid black;">Customer Details</th>' if self.customers else ""
                table_th += '<th style="border: 1px solid black;">Subscription Details</th>' if self.service else ""
                table_td += '<td style="border: 1px solid black; padding: 5px;">{cust_info}</td>'.format(cust_info=cust_info) if self.customers else ""
                table_td += '<td style="border: 1px solid black; padding: 5px;">{service_info}</td>'.format(service_info=service_info) if self.service else ""

                if self.customers or self.service:
                        msg = """
                        <table style="border: 1px solid black; font-size: x-small; border-collapse: collapse;">
                                <tr>
                                        {table_th}
                                </tr>
                                <tr>
                                        {table_td}
                                </tr>
                        </table>
                        """.format(table_th=table_th, table_td=table_td)
                return msg

        def get_email_content(self):
                msg_subject = msg_header = msg_body = msg_footer = ""

                if frappe.db.exists("Email Settings", {"action_type": self.order_type, "action_method": self.action_method, "action_days": cint(self.action_days)}):
                        doc = frappe.get_doc("Email Settings", {"action_type": self.order_type, "action_method": self.action_method, "action_days": cint(self.action_days)})
                        msg_subject = str(doc.email_subject).format(action_days=cint(self.action_days),work_order_no=self.name,expiry_date=getdate(self.expiry_date).strftime("%B %d, %Y"))
                        msg_header  = str(doc.email_header).format(action_days=cint(self.action_days),work_order_no=self.name,expiry_date=getdate(self.expiry_date).strftime("%B %d, %Y"))
                        msg_body    = str(doc.email_body).format(action_days=cint(self.action_days),work_order_no=self.name,expiry_date=getdate(self.expiry_date).strftime("%B %d, %Y"))
                        msg_footer  = str(doc.email_footer).format(action_days=cint(self.action_days),work_order_no=self.name,expiry_date=getdate(self.expiry_date).strftime("%B %d, %Y"))
                else:
                        if self.order_type == "Ticket":
                                msg_subject = "Work Order "+self.name+": "+self.document_title
                                msg_header  = ""
                                msg_body   += "Work Order {0} assigned to you for necessary action.".format(self.name)
                                msg_footer  = "Your Sincerely"

                if self.order_type == "Ticket":
                        if self.order_status == "Systems Pending":
                                msg_header = "Dear Systems,"
                        elif self.order_status == "Billing Pending":
                                msg_header = "Dear Billing,"
                        else:
                                pass

                        msg_body   += "<br/><b>Order Title: {0}</b>".format(self.order_title) if self.order_title else ""
                        msg_body   += "<br/><b>Remarks: </b>{0}".format(self.remarks) if self.remarks else ""
                else:
                        pass

                msg_body += "<br/>{0}".format(self.get_customer_service_table())
                
                return msg_subject, msg_header, msg_body, msg_footer
        
        def send_email_alerts(self):
                cust_email_id = []
                internal      = frappe._dict()
                recipients    = []
                cc            = []
                bcc           = ['siva@bt.bt']
                msg_subject = msg_header = msg_body = msg_footer = ""

                if cint(self.notify_customer):
                        cust_email_id.append(self.email_id)
                
                if cint(self.notify_internal):
                        int_list = frappe.db.sql("""
                                select
                                        (case
                                                when hr.role in ('Billing User','Billing Admin') then 'Billing'
                                                when hr.role in ('Systems User','Systems Admin') then 'Systems'
                                                else hr.role
                                        end) as role,
                                        hr.parent
                                from `tabHas Role` hr
                                where hr.parenttype = 'User'
                                and hr.parentfield = 'roles'
                                and hr.role in ('Billing User','Billing Admin','Systems User','Systems Admin')
                                and exists(select 1
                                                from `tabUser` u
                                                where u.name = hr.parent
                                                and u.enabled= 1)
                        """, as_dict=True)
                        for i in int_list:
                                internal.setdefault(str(i.role),[]).append(str(i.parent))

                if cint(self.notify_customer) or cint(self.notify_internal):
                        msg_subject, msg_header, msg_body, msg_footer = self.get_email_content()
                        
                        if self.order_type == "Notification":
                                if cint(self.notify_customer):
                                        if self.email_id:
                                                #recipients = cust_email_id     # Temporarily commented
                                                recipients = ['siva@bt.bt']
                                        else:
                                                recipients = ['siva@bt.bt']
                                                msg_subject = "WorkOrder {0}: {1} Email ID missing".format(self.name, self.customers)
                        else:
                                if self.order_status == "Systems Pending":
                                        recipients = list(set(internal.get('Systems')))
                                        cc = list(set(internal.get('Billing')))
                                elif self.order_status == "Billing Pending":
                                        recipients = list(set(internal.get('Billing')))
                                        cc = list(set(internal.get('Systems')))
                                else:
                                        pass

                                # CC to customer for Tickets
                                if cint(self.notify_customer):
                                        cc += [self.email_id]

                        if len(recipients):        
                                # Sending mail
                                email.make(
                                        doctype = 'Customers',
                                        name = self.customers,
                                        content = "{msg_header}<br/>{msg_body}<br/><br/>{msg_footer}".format(
                                                        msg_header=msg_header,
                                                        msg_body=msg_body,
                                                        msg_footer=msg_footer
                                                  ),
                                        subject = msg_subject,
                                        recipients=",".join(recipients),
                                        cc = ",".join(cc),
                                        bcc = ",".join(bcc),
                                        communication_medium='Email',
                                        send_email=True,
                                        send_me_a_copy=True,            #Sends a copy to bia@bt.bt
                                        #print_html=email_body          #Sends the print_html content as html attachment
                                )
        def send_email_alerts_x(self):
                cust_email_id = []
                internal      = frappe._dict()
                msg_subject   = ""
                msg_header    = ""
                msg_body      = ""
                msg_footer    = ""
                recipients    = []
                cc            = []
                bcc           = ['siva@bt.bt']


                
                if cint(self.notify_customer):
                        cust_email_id.append(self.email_id)
                
                if cint(self.notify_internal):
                        int_list = frappe.db.sql("""
                                select
                                        (case
                                                when hr.role in ('Billing User','Billing Admin') then 'Billing'
                                                when hr.role in ('Systems User','Systems Admin') then 'Systems'
                                                else hr.role
                                        end) as role,
                                        hr.parent
                                from `tabHas Role` hr
                                where hr.parenttype = 'User'
                                and hr.parentfield = 'roles'
                                and hr.role in ('Billing User','Billing Admin','Systems User','Systems Admin')
                                and exists(select 1
                                                from `tabUser` u
                                                where u.name = hr.parent
                                                and u.enabled= 1)
                        """, as_dict=True)
                        for i in int_list:
                                internal.setdefault(str(i.role),[]).append(str(i.parent))

                if cint(self.notify_customer) or cint(self.notify_internal):                        
                        if self.order_status == "Systems Pending":
                                recipients = list(set(internal.get('Systems')))
                                cc = list(set(internal.get('Billing')))
                                msg_subject = "Work Order "+self.name+": "+self.document_title
                                msg_header = "Dear Systems,"
                                msg_body = "Work Order {0} for Service Disconnection for the following services assigned to you.".format(self.name) if self.action_method == "After Service Expiry" \
                                           else "Work Order {0} assigned to you for necessary action.".format(self.name)
                                msg_body += "<br/><b>Order Title: {0}</b>".format(self.order_title) if self.order_title else ""
                                msg_body += "<br/><b>Remarks: </b>{0}".format(self.remarks) if self.remarks else ""
                        elif self.order_status == "Billing Pending":
                                recipients = list(set(internal.get('Billing')))
                                cc = list(set(internal.get('Systems'))) if self.order_type == "Ticket" else []
                                msg_subject = "Work Order "+self.name+": "+self.document_title
                                msg_header = "Dear Billing,"
                                msg_body = "Work Order {0} for Service Disconnection for the following services assigned to you.".format(self.name) if self.action_method == "After Service Expiry" \
                                           else "Work Order {0} assigned to you for necessary action.".format(self.name)
                                msg_body += "<br/><br/><b>Order Title: {0}</b>".format(self.order_title) if self.order_title else ""
                                msg_body += "<br/><b>Remarks: </b>{0}".format(self.remarks) if self.remarks else ""
                        else:
                                if self.order_status == "Closed":
                                        if self.order_type == "Notification":
                                                msg_header = "Dear Customer,"
                                                if cint(self.notify_customer):
                                                        if len(cust_email_id):
                                                                #recipients = cust_email_id     # Temporarily commented
                                                                recipients = ['siva@bt.bt']
                                                                msg_subject = "["+self.order_type+"]"+" "+(("Your Subscription expires in {0} days".format(self.action_days) if self.action_days else "Your Subscription Expired") if self.action_method == "Before Service Expiry" else "Your Subscription Expired")
                                                                msg_body = "This is a reminder that your subscription for the following mentioned package expires within {0} days.".format(self.action_days) if self.action_days \
                                                                           else "This is to notify you that your subscription for the following mentioned package expired today."
                                                                msg_body += "<br/><br/><b>Remarks: </b>{0}".format(self.remarks) if self.remarks else ""
                                                        else:
                                                                recipients = list(set(internal.get('Billing')))
                                                                msg_subject = str(self.customer_code)+" Email address missing"

                        if len(recipients):
                                email_body = self.get_customer_service_table()
                                
                                # Sending mail
                                email.make(
                                        doctype = 'Customers',
                                        name = self.customers,
                                        content = "{msg_header}<br/><br/>{msg_body}<br/>{email_body}<br/><br/>{msg_footer}".format(
                                                        msg_header=msg_header,
                                                        msg_body=msg_body,
                                                        email_body=email_body,
                                                        msg_footer=msg_footer
                                                  ),
                                        subject = msg_subject,
                                        recipients=",".join(recipients),
                                        cc = ",".join(cc),
                                        bcc = ",".join(bcc),
                                        communication_medium='Email',
                                        send_email=True,
                                        send_me_a_copy=True, #Sends a copy to bia@bt.bt
                                        #print_html=email_body   #Sends the print_html content as html attachment
                                )

        
        def update_tags(self):
                DocTags(self.doctype).remove_all(self.name)
                DocTags(self.doctype).add(self.name, self.order_status)
                DocTags(self.doctype).add(self.name, 'Total '+self.order_type)                        

@frappe.whitelist()
def get_service(doctype, txt, searchfield, start, page_len, filters):
        if filters.get('customer'):
                query = 'select name, des, currency, price from `tabService`'
                return frappe.db.sql(query)
                '''
                return frappe.db.sql("""
                        select
                                s.name,
                                s.des,
                                s.currency
                        from `tabEquipment` e
                        where e.equipment_type = '{0}'
                        and e.branch = '{1}'
                        and e.is_disabled != 1
                        and e.not_cdcl = 0
                        and not exists (select 1
                                        from `tabEquipment Reservation Entry` a
                                        where (
                                                ('{2}' between concat(from_date,' ',from_time) and concat(to_date,' ',to_time)
                                                or
                                                '{3}' between concat(from_date,' ',from_time) and concat(to_date,' ',to_time)
                                                or
                                                ('{2}' <= concat(from_date,' ',from_time) and '{3}' >= concat(to_date,' ',to_time))
                                        )
                                                )
                                        and a.equipment = e.name)
                        """.format(equipment_type, branch, from_datetime, to_datetime))
                '''
        else:
                return ()
