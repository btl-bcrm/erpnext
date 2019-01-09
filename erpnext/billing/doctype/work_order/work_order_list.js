frappe.listview_settings["Work Order"] = {
		onload: function(lsitview){
			/*
			if(!frappe.route_options){
				if(in_list(frappe.user_roles, "Billing User") || in_list(frappe.user_roles, "Billing Admin")){
					frappe.route_options = {
						"order_status": ["in", "Billing Draft, Billing Pending"]
					};
				}
				
				if(in_list(frappe.user_roles, "Systems User") || in_list(frappe.user_roles, "Systems Admin")){
					frappe.route_options = {
						"order_status": ["in", "Systems Draft, Systems Pending"]
					};
				}
			}
			*/
		},
        add_fields: ["order_status"],
        filters:[["order_status","=", "Billing Draft"]],
        get_indicator: function(doc) {
                if(doc.order_status === "Billing Draft"){
                        return [__("{0}", [doc.order_status]), "lightblue", "order_status,=,Billing Draft"];
                } else if(doc.order_status === "Systems Draft"){
                        return [__("{0}", [doc.order_status]), "lightblue", "order_status,=,Systems Draft"];
                } else if(doc.order_status === "Billing Pending"){
                        return [__("{0}", [doc.order_status]), "orange", "order_status,=,Billing Pending"];
				} else if(doc.order_status === "Systems Pending"){
                        return [__("{0}", [doc.order_status]), "orange", "order_status,=,Systems Pending"];
				} else if(doc.order_status === "Billing Rejected"){
                        return [__("{0}", [doc.order_status]), "orange", "order_status,=,Billing Rejected"];
				} else if(doc.order_status === "Systems Rejected"){
                        return [__("{0}", [doc.order_status]), "orange", "order_status,=,Systems Rejected"];
				} else if(doc.order_status === "Billing Cancelled"){
                        return [__("{0}", [doc.order_status]), "red", "order_status,=,Billing Cancelled"];
				} else if(doc.order_status === "Systems Cancelled"){
                        return [__("{0}", [doc.order_status]), "red", "order_status,=,Systems Cancelled"];
				} else {
                        return [__(doc.order_status), frappe.utils.guess_colour(doc.order_status), "order_status,=," + doc.order_status];
                }
        },
};
