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
        if filters.get("customer_id"):
                cond.append("eq.reference_doctype = 'Customers' and eq.reference_name = '{0}'".format(filters.get("customer_id")))
        if filters.get("status") and filters.get("status") != "All":
                cond.append("eq.status = '{0}'".format(filters.get("status")))

        if len(cond):
                return "and " + " and ".join(cond)
        else:
                return ""

def get_data(filters):
        cond = get_conditions(filters)
        query = """
                select 
                        eq.name,
                        date(eq.creation) creation,
                        eq.status,
                        eq.reference_doctype,
                        eq.reference_name,
                        eq.communication,
                        eq.sender,
                        group_concat(eqr.recipient separator ',') recipients,
                        eq.show_as_cc,
                        eq.error
                from `tabEmail Queue` eq, `tabEmail Queue Recipient` eqr
                where eqr.parent = eq.name
                and date(eq.creation) between '{from_date}' and '{to_date}'
                {cond}
                group by eq.name, eq.status, eq.reference_doctype, eq.reference_name,
                        eq.communication, eq.sender, eq.show_as_cc, eq.error
        """.format(
                from_date = filters.get("from_date"),
                to_date = filters.get("to_date"),
                cond = cond
        )

        return frappe.db.sql(query)

def get_columns():
        return [
                {
                        "fieldname": "name",
                        "label": _("Queue ID"),
                        "fieldtype": "Link",
                        "options": "Email Queue",
                        "width": 100,
                },
                {
                        "fieldname": "creation",
                        "label": _("Date"),
                        "fieldtype": "Date",
                        "width": 80,
                },
                {
                        "fieldname": "status",
                        "label": _("Status"),
                        "fieldtype": "Data",
                        "width": 80,
                },
                {
                        "fieldname": "reference_doctype",
                        "label": _("Reference Type"),
                        "fieldtype": "Data",
                        "width": 80,
                },
                {
                        "fieldname": "reference_name",
                        "label": _("Reference Name"),
                        "fieldtype": "Dynamic Link",
                        "options": "reference_doctype",
                        "width": 80,
                },
                {
                        "fieldname": "communication",
                        "label": _("Communication"),
                        "fieldtype": "Link",
                        "options": "Communication",
                        "width": 80,
                },
                {
                        "fieldname": "sender",
                        "label": _("Sender"),
                        "fieldtype": "Data",
                        "width": 150,
                },
                {
                        "fieldname": "recipients",
                        "label": _("Recipients"),
                        "fieldtype": "Data",
                        "width": 180,
                },
                {
                        "fieldname": "show_as_cc",
                        "label": _("CC"),
                        "fieldtype": "Data",
                        "width": 180,
                },
                {
                        "fieldname": "error",
                        "label": _("Error"),
                        "fieldtype": "Data",
                        "width": 250,
                },
        ]
