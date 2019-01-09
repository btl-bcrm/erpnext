// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

cur_frm.add_fetch('customers','customer_code','customer_code');
cur_frm.add_fetch('customers','company_name','company_name');
cur_frm.add_fetch('customers','first_name','first_name');
cur_frm.add_fetch('customers','last_name','last_name');
cur_frm.add_fetch('customers','email_id','email_id');
cur_frm.add_fetch('customers','contact1','contact1');
cur_frm.add_fetch('service','des','des');
cur_frm.add_fetch('service','price','price');

frappe.ui.form.on('Work Order', {
	refresh: function(frm) {
		enable_disable(frm);
		toggle_actions(frm);
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