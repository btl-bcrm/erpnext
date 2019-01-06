# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Ticket(Document):
        def validate(self):
                pass

        def on_submit(self):
                pass

        def get_customer_info(self):
                if self.customer_id:
                        doc = frappe.get_doc('Customers', self.customer_id)
                        self.company_name = doc.company_name
                        self.first_name = doc.first_name
                        self.last_name = doc.last_name
