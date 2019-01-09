# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Customers(Document):
	def onload(self):
                if not self.get('__unsaved'):
                        self.load_customers_contract()
                        self.load_customers_contract_service()

        '''
        def __setup__(self):
                self.onload()
        '''

        def validate(self):
                # Resetting child tables
                self.customers_contract = []
                self.customers_contract_service = []
        
        def load_customers_contract(self):
                """Load `contracts` from the database"""
                self.customers_contract = []
                for co in self.get_customers_contract():
                        self.append("customers_contract",{
                                "customer_id": co.customer_id,
                                "co_id": co.co_id,
                                "co_code": co.co_code,
                                "contract_status": co.contract_status,
                                "co_installed": co.co_installed,
                                "co_moddate": co.co_moddate,
                                "dn_num": co.dn_num,
                                "dn_status": co.dn_status
                        })

        def load_customers_contract_service(self):
                """Load `services` from the database"""
                self.customers_contract_service = []
                for cs in self.get_customers_contract_service():
                        self.append("customers_contract_service",{
                                "transaction_id": cs.transaction_id,
                                "customer_id": cs.customer_id,
                                "co_id": cs.co_id,
                                "sncode": cs.sncode,
                                "des": cs.des,
                                "service_status": cs.service_status,
                                "valid_from_date": cs.valid_from_date
                        })

        def get_customers_contract(self):
                return frappe.get_all("Contract","*",{"customer_id": str(self.name)},order_by="name")

        def get_customers_contract_service(self):
                return frappe.get_all("Contract Service","*",{"customer_id": self.name},order_by="co_id, sncode, valid_from_date desc")
