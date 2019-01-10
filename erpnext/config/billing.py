from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Masters"),
			"items": [
                                {
					"type": "doctype",
					"name": "Service",
					"description": _("Service master.")
				},
				{
					"type": "doctype",
					"name": "Customers",
					"description": _("Billing customer master.")
				},
				{
					"type": "doctype",
					"name": "Contract",
					"description": _("Customer contract master.")
				},
                                {
					"type": "doctype",
					"name": "Contract Service",
					"description": _("Contract service master.")
				},
			]
		},
                {
			"label": _("Transactions"),
			"items": [
                                {
					"type": "doctype",
					"name": "Work Order",
					"description": _("Work orders.")
				},
			]
		},
                {
			"label": _("Settings"),
			"items": [
                                {
					"type": "doctype",
					"name": "User",
					"description": _("System users control panel")
				},
                                {
					"type": "doctype",
					"name": "Email Settings",
					"description": _("Email Settings")
				},
                                {
					"type": "doctype",
					"name": "Email Queue",
					"description": _("Email Queue")
				},
                                {
					"type": "doctype",
					"name": "Error Log",
					"description": _("Error Log")
				},
			]
		},
                {
			"label": _("SIM Management"),
			"items": [
                                {
					"type": "doctype",
					"name": "SIM Vendor",
					"description": _("SIM Vendor.")
				},
				{
					"type": "doctype",
					"name": "SIM Upload",
					"description": _("SIM Upload.")
				},
				{
					"type": "doctype",
					"name": "SIM Entry",
					"description": _("SIM Entry.")
				},
                                {
					"type": "report",
					"name": "SIM Report",
					"doctype": "SIM Entry",
					"is_query_report": True,
                                        "style": {"color":"red"}
				},
			]
		},
	]
