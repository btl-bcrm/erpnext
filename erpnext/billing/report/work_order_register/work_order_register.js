// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Order Register"] = {
	"filters": [
		{		
			"fieldname":"order_type",
			"label": ("Order Type"),
			"fieldtype": "Select",
			"options": "All\nNotifications\nTickets",
			"default": "All"
		},
		{		
			"fieldname":"customer_id",
			"label": ("Customer ID"),
			"fieldtype": "Link",
			"options": "Customers"
		},
		{		
			"fieldname":"workorder",
			"label": ("Order Number"),
			"fieldtype": "Data"
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
