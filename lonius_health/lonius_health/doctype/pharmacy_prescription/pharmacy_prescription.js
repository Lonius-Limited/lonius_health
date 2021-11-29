// Copyright (c) 2021, Lonius Limited Innovation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pharmacy Prescription', {
	onload_post_render: (frm) => {

	},
	customer: (frm) => {
		// frappe.freeze()
		let customer = frm.doc.customer
		if (!customer){
			frappe.throw("Customer not selected!")
		}
		frappe.call({
			method: 'frappe.client.get_value',
			freeze: true,
			freeze_message: 'Reloading Form...Please Wait',
			async: True,
			args: {
				'doctype': 'Customer',
				'filters': { 'name': customer },
				'fieldname': [
					'item_name',
					'web_long_description',
					'description',
					'image',
					'thumbnail'
				]
			},
			callback: function (r) {
				if (!r.exc) {
					// code snippet
				}
			}
		});

	}
	// refresh: function(frm) {

	// }
});
