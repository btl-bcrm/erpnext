// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ticket', {
	refresh: function(frm) {
		
	},
	customer_id: function(frm){
		get_customer_info(frm.doc);
	}
});

var get_customer_info = function(doc){
	cur_frm.call({
			method: "get_customer_info",
			doc: doc
	});
}
