# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class EmailSettings(Document):
	def validate(self):
                self.validate_email_settings()

        def validate_email_settings(self):
                if frappe.db.exists("Email Settings", {"order_type": self.order_type, "action_method": self.action_method, "name":("!=",self.name)}):
                        frappe.throw(_("Duplicate entry found for order type <b>{0}</b> and action method <b>{1}</b>").format(self.order_type, self.action_method), title="Duplicate Entry")
