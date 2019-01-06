// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Order', {
	refresh: function(frm) {
		enable_disable(frm);
		toggle_actions(frm);
	},
	customers: function(frm){
		get_customer_info(frm.doc);
		
		/*
		frm.set_query("service", function() {
			return {
				query: "erpnext.billing.doctype.work_order.work_order.get_service",
				filters: {
						customer: frm.doc.customer_id
				}
			};
		});
		*/
	},
});

function toggle_form_fields(frm, fields, flag){
        fields.forEach(function(field_name){
                frm.set_df_property(field_name, "read_only", flag);
        });

        if(flag){
                frm.disable_save();
        } else {
                frm.enable_save();
        }
		
		//cur_frm.appframe.buttons.Submit.remove();
}

function enable_disable(frm){
        var toggle_fields = [];
        var meta = frappe.get_meta(frm.doctype);

        for(var i=0; i<meta.fields.length; i++){
                if(meta.fields[i].hidden === 0 && meta.fields[i].read_only === 0 && meta.fields[i].allow_on_submit === 0){
                        toggle_fields.push(meta.fields[i].fieldname);
                }
        }

        toggle_form_fields(frm, toggle_fields, 1);

		if(in_list(frappe.user_roles, "Billing User") || in_list(frappe.user_roles, "Billing Admin")){
				if(frm.doc.__islocal){
					frm.set_value("order_status", "Billing Draft");
				}
				
				if (["Billing Draft","Billing Pending","Systems Rejected"].indexOf(frm.doc.order_status) >= 0){
					toggle_form_fields(frm, toggle_fields, 0);
				}
				else {
					toggle_form_fields(frm, toggle_fields, 1);
				}
		} else if (in_list(frappe.user_roles, "Systems User") || in_list(frappe.user_roles, "Systems Admin")){
				if(frm.doc.__islocal){
					frm.set_value("order_status", "Systems Draft");
				}

				if (["Systems Draft","Systems Pending","Billing Rejected"].indexOf(frm.doc.order_status) >= 0){
					toggle_form_fields(frm, toggle_fields, 0);
				}
				else {
					toggle_form_fields(frm, toggle_fields, 1);
				}
		} 
		
		if((frappe.session.user === "Administrator") || (in_list(frappe.user_roles, "System Manager"))){
			toggle_form_fields(frm, toggle_fields, 0);
		}
}

var toggle_actions = function(frm){
	if(!frm.doc.__islocal){
		if (["Billing Draft", "Billing Pending"].indexOf(frm.doc.order_status) >= 0 && 
				(in_list(frappe.user_roles, "Billing User") || in_list(frappe.user_roles, "Billing Admin"))){
			frm.add_custom_button(__("Forward to Systems"), function(){
							frm.set_value("order_status","Systems Pending");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
			frm.add_custom_button(__("Close"), function(){
							frm.set_value("order_status","Closed");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
			frm.add_custom_button(__("Cancel"), function(){
							frm.set_value("order_status","Billing Cancelled");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
		} else if (["Systems Draft", "Systems Pending"].indexOf(frm.doc.order_status) >= 0 &&
				(in_list(frappe.user_roles, "Systems User") || in_list(frappe.user_roles, "Systems Admin"))){
			frm.add_custom_button(__("Forward to Billing"), function(){
							frm.set_value("order_status","Billing Pending");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
			frm.add_custom_button(__("Close"), function(){
							frm.set_value("order_status","Closed");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
			frm.add_custom_button(__("Cancel"), function(){
							frm.set_value("order_status","Billing Cancelled");
							frm.save();
					},__("Actions"), "icon-file-alt"
			);
		}
	}
}

var get_customer_info = function(doc){
	cur_frm.call({
			method: "get_customer_info",
			doc: doc
	});
}