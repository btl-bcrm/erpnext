# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_conditions(filters):
        cond = []
        if filters.get("workorder"):
                cond.append("name = '{0}'".format(filters.get("workorder")))
        if filters.get("customer_id"):
                cond.append("customers = '{0}'".format(filters.get("customer_id")))
        if filters.get("order_type") and filters.get("order_type") != "All":
                cond.append("order_type = '{0}'".format("Notification" if filters.get("order_type") == "Notifications" else "Ticket"))        

        if len(cond):
                return "and " + " and ".join(cond)
        else:
                return ""

def get_data(filters):
        cond = get_conditions(filters)
        query = """
                select
                        name workorder, order_type, order_date, order_status, document_title, 
                        customers, customer_code, company_name, first_name, last_name,
                        email_id, contact1, des, valid_from_date, expiry_date,
                        action_method, action_days, action_date
                from `tabWork Order`
                where order_date between '{from_date}' and '{to_date}'
                {cond}
                order by name
        """.format(
                from_date = filters.get("from_date"),
                to_date = filters.get("to_date"),
                cond = cond
        )

        return frappe.db.sql(query)

def get_columns():
        return [
                {
                        "fieldname": "workorder",
                        "label": _("Order#"),
                        "fieldtype": "Link",
                        "options": "Work Order",
                        "width": 100,
                },
                {
                        "fieldname": "order_type",
                        "label": _("Order Type"),
                        "fieldtype": "Data",
                        "width": 80,
                },
                {
                        "fieldname": "order_date",
                        "label": _("Date"),
                        "fieldtype": "Date",
                        "width": 80,
                },
                {
                        "fieldname": "order_status",
                        "label": _("Status"),
                        "fieldtype": "Data",
                        "width": 80,
                },
                {
                        "fieldname": "document_title",
                        "label": _("Title"),
                        "fieldtype": "Data",
                        "width": 180,
                },
                {
                        "fieldname": "customers",
                        "label": _("Customer ID"),
                        "fieldtype": "Link",
                        "options": "Customers",
                        "width": 80,
                },
                {
                        "fieldname": "customer_code",
                        "label": _("Customer Code"),
                        "fieldtype": "Data",
                        "width": 80,
                },
                {
                        "fieldname": "company_name",
                        "label": _("Company Name"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "first_name",
                        "label": _("First Name"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "last_name",
                        "label": _("Last Name"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "email_id",
                        "label": _("Email ID"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "contact1",
                        "label": _("Contact No"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "des",
                        "label": _("Service"),
                        "fieldtype": "Data",
                        "width": 120,
                },
                {
                        "fieldname": "valid_from_date",
                        "label": _("Activation Date"),
                        "fieldtype": "Date",
                        "width": 80,
                },
                {
                        "fieldname": "expiry_date",
                        "label": _("Expiry Date"),
                        "fieldtype": "Date",
                        "width": 80,
                },
                {
                        "fieldname": "action_method",
                        "label": _("Notification Method"),
                        "fieldtype": "Data",
                        "width": 180,
                },
                {
                        "fieldname": "action_days",
                        "label": _("Days"),
                        "fieldtype": "Int",
                        "width": 80,
                },
                {
                        "fieldname": "action_date",
                        "label": _("Notification Date"),
                        "fieldtype": "Date",
                        "width": 100,
                },
        ]
