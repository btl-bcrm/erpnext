# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint, getdate, get_datetime, get_url, nowdate, now_datetime, \
     money_in_words, add_days, add_months, add_years

class EmailSettings(Document):
	def validate(self):
                self.check_duplicate_entries()
                self.validate_email_settings()
                
        def check_duplicate_entries(self):
                if frappe.db.exists("Email Settings", {"action_type": self.action_type, "action_method": self.action_method, "name":("!=",self.name), "action_days": cint(self.action_days)}):
                        frappe.throw(_("Duplicate entry found for action type <b>{0}</b> and action method <b>{1}</b> with action days <b>{2}</b>").format(self.order_type, self.action_method, self.action_days), title="Duplicate Entry")

        def validate_email_settings(self):
                if cint(self.action_days) < 0:
                        frappe.throw(_("Action days cannot be a negative value"), title="Invalid Data")
                elif self.action_method == "On Service Expiry" and cint(self.action_days) != 0:
                        frappe.throw(_("Action days should be <b>zero</b> for action method <b>On Service Expiry</b>"), title="Invalid Data")
                elif self.action_method != "On Service Expiry" and cint(self.action_days) == 0:
                        frappe.throw(_("Action days can only be zero for action method <b>On Service Expiry</b>"), title="Invalid Data")
                else:
                        pass
