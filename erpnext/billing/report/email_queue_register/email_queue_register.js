// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Email Queue Register"] = {
	"filters": [
		{		
			"fieldname":"customer_id",
			"label": ("Customer ID"),
			"fieldtype": "Link",
			"options": "Customers"
		},
		{		
			"fieldname":"status",
			"label": ("Status"),
			"fieldtype": "Select",
			"options": "All\nSent\nNot Sent\nSending\nError\nPartially Errored\nExpired",
			"default": "All"
		},
		{		
			"fieldname":"from_date",
			"label": ("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{		
			"fieldname":"to_date",
			"label": ("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
	]
}
