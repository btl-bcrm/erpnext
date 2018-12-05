# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
     return [
                ("SIM ID") + ":Data:150",
                ("IMSI") + ":Data:150",
                ("PIN1") + ":Data:80",
		("PUK1") + ":Data:80",
                ("PIN2")+ ":Data:80",
                ("PUK2") + ":Data:80",
                ("EKI") + ":Data:250",
                ("Sim Upload") + ":Data:100",
                ("Vendor") + ":Data:100"
        ]

def get_data(filters):
    cond = get_conditions(filters)

    data = []
    query = """
        select
                name, imsi, pin1, puk1, pin2, puk2, eki,
                sim_upload, sim_vendor
        from `tabSIM Entry`
        {0}
        limit 100
    """.format(cond)
    result = frappe.db.sql(query)
    data.extend(result)
    data.append(tuple([None]))

    return data

def get_conditions(filters):
    cond = []

    if filters.get("iccid"):
        cond.append("name = '{0}'".format(filters.get("iccid")))

    if filters.get("imsi"):
        cond.append("imsi = '{0}'".format(filters.get("imsi")))

    if len(cond):
        return "where "+" and ".join(cond)
