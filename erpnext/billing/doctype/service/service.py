# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint, getdate, get_datetime, get_url, nowdate, now_datetime, \
     money_in_words, add_days, add_months, add_years

class Service(Document):
	def validate(self):
                self.validate_action_days()
                
        def validate_action_days(self):
                for i in self.get('items'):
                        if cint(i.action_days) < 0:
                                frappe.throw(_("Row#{0}: Action days cannot be a negative value").format(i.idx), title="Invalid Data")
                        elif i.action_method == "On Service Expiry" and cint(i.action_days) != 0:
                                frappe.throw(_("Row#{0}: Action days should be zero for {1}").format(i.idx,i.action_method), title="Invalid Data")
                        elif i.action_method != "On Service Expiry" and cint(i.action_days) ==  0:
                                frappe.throw(_("Row#{0}: Please use On Service Expiry for action days zero").format(i.idx), title="Invalid Data")
                        else:
                                pass

                        # Checking Email Settings for correspondent entry
                        if cint(i.notify_customer) or cint(i.notify_internal):
                                if not frappe.db.exists("Email Settings",{"action_type": i.action_type,"action_method": i.action_method,"action_days": cint(i.action_days)}):
                                        frappe.throw(_("Row#{0}: Please create corresponding entry for the following event under <b>Email Settings</b> first. <br>[{1}, {2}, {3}]").format(i.idx,i.action_type,i.action_method,i.action_days), title="Data Missing")
