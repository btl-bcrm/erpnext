from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Customers",
					"description": _("Billing customer master.")
				},
				{
					"type": "doctype",
					"name": "Service",
					"description": _("Service master.")
				},
			]
		},
	]
