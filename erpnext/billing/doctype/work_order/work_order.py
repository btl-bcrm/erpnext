# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.desk.tags import DocTags

class WorkOrder(Document):
        def validate(self):
                self.update_status()
                pass

        def on_update(self):
                self.update_tags()
                
        def on_submit(self):
                pass
        
        def on_cancel(self):
                pass

        def update_status(self):
                if self.order_status == 'Closed':
                        self.docstatus = 1
                elif self.order_status in ('Billing Cancelled','Systems Cancelled'):
                        self.docstatus = 2
                else:
                        self.docstatus = 0
                        
        def update_tags(self):
                DocTags(self.doctype).remove_all(self.name)
                DocTags(self.doctype).add(self.name, self.order_status)
                
        def get_customer_info(self):
                if self.customers:
                        doc = frappe.get_doc('Customers', self.customers)
                        self.customer_code = doc.customer_code
                        self.company_name = doc.company_name
                        self.first_name = doc.first_name
                        self.last_name = doc.last_name
                        self.email_id = doc.email_id
                        self.contact1 = doc.contact1
                        
        def get_service_info(self):
                pass

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
