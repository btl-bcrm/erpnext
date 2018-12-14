// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["SIM Report"] = {
	"filters": [
		{		
			"fieldname":"from_iccid",
			"label": ("FROM SIM ID"),
			"fieldtype": "Data",
			"width": "100"
		},
		{		
			"fieldname":"to_iccid",
			"label": ("TO SIM ID"),
			"fieldtype": "Data",
			"width": "100"
		},
		{		
			"fieldname":"from_imsi",
			"label": ("FROM IMSI"),
			"fieldtype": "Data",
			"width": "100"
		},
		{		
			"fieldname":"to_imsi",
			"label": ("TO IMSI"),
			"fieldtype": "Data",
			"width": "100"
		},
	]
}
