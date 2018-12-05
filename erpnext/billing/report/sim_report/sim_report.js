// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["SIM Report"] = {
	"filters": [
		{		
			"fieldname":"iccid",
			"label": ("SIM ID"),
			"fieldtype": "Data",
			"width": "100"
		},
		{		
			"fieldname":"imsi",
			"label": ("IMSI"),
			"fieldtype": "Data",
			"width": "100"
		},
	]
}
