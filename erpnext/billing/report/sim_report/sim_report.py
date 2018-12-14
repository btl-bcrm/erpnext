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
    """.format(cond)
    result = frappe.db.sql(query)
    data.extend(result)
    data.append(tuple([None]))

    return data

def get_conditions(filters):
    cond = []

    if filters.get("from_iccid") and filters.get("to_iccid"):
        cond.append("name between '{0}' and '{1}'".format(filters.get("from_iccid"), filters.get("to_iccid")))
    elif filters.get("from_iccid"):
        cond.append("name = '{0}'".format(filters.get("from_iccid")))
    elif filters.get("to_iccid"):
        cond.append("name = '{0}'".format(filters.get("to_iccid")))
    else:
        pass


    if filters.get("from_imsi") and filters.get("to_imsi"):
        cond.append("imsi between '{0}' and '{1}'".format(filters.get("from_imsi"), filters.get("to_imsi")))
    elif filters.get("from_imsi"):
        cond.append("imsi = '{0}'".format(filters.get("from_imsi")))
    elif filters.get("to_imsi"):
        cond.append("imsi = '{0}'".format(filters.get("to_imsi")))
    else:
        pass


    if len(cond):
        return "where "+" and ".join(cond)
    else:
        return "limit 100"
