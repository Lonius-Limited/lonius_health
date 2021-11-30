// Copyright (c) 2021, Lonius Limited Innovation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pharmacy Prescription', {

	refresh: (frm) => {
		frm.disable_save();
		frm.get_field("prescription_items").grid.cannot_add_rows = true;
		frm.get_field("prescription_items").grid.only_sortable();
		refresh_field('prescription_items')


		if (frm.doc.status == 'Prescription Ready') {
			frm.remove_custom_button(__("Make a Prescription Refill"))
			frm.add_custom_button(__("Change Payer"), function () {
				//perform desired action such as routing to new form or fetching etc.
				changePayerDialog(frm)
			});
			frm.add_custom_button(__("Dispense Prescription"), function () {
				//perform desired action such as routing to new form or fetching etc.
				dispensePrescription(frm)
			});
			frm.fields_dict['prescription_items'].grid.add_custom_button('Add Drug', () => { addDrug(frm) }, 'primary')
			frm.fields_dict['prescription_items'].grid.add_custom_button('Check Alternatives for Selected Drug', () => { drugAlternativeDialog(frm) }, 'primary')


			// frm.fields_dict['prescription_items'].grid.change_custom_button_type('danger');

			// }
		}
		if (frm.doc.status == 'Prescription Serviced') {
			frm.set_intro('This prescription has already been serviced. Please Click <strong>Make a Prescription Refill</strong> to dispense/bill remaining quantities.');
			// frm.disable_save();
			frm.add_custom_button(__("Make a Prescription Refill"), function () {
				//perform desired action such as routing to new form or fetching etc.	

			});
		}
	},
	onload_post_render: (frm) => {

		frm.get_field("prescription_items").grid.cannot_add_rows = true;
		frm.get_field("prescription_items").grid.only_sortable();
		refresh_field('prescription_items')
	},
	warehouse: (frm) => {

	},
	prescription_items: (frm) => {
		frm.refresh_field("prescription_items")

	},
	customer: (frm) => {
		// frappe.freeze()
		let customer = frm.doc.customer
		if (!customer) {
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
					'customer_type'
				]
			},
			callback: function (r) {
				if (!r.exc) {
					// code snippet
					r.message = "Company" ? frm.doc.is_insurance_patient = 1 : frm.doc.is_insurance_patient = 0
					refresh_field("is_insurance_patient")
				}
			}
		});

	}

});
frappe.ui.form.on('Pharmacy Prescription Item', {
	refresh(frm) {
		frm.get_field("prescription_items").grid.cannot_add_rows = true;


	},
	prescription_items_add: (frm) => {

	},
	qty(frm, cdt, cdn) {
		const row = locals[cdt][cdn]
		if (row.qty && row.rate) {
			console.log(JSON.stringify(row.drug_name));
			var quantity = row.qty
			var rate = row.rate
			var amount = parseFloat(quantity * rate)
			row.amount = amount
			refresh_field("prescription_items")
			refreshTotals(frm)
		}
		// if(row.qty && row.maximum_prescription_quantity){
		// 	console.log(row.qty , row.maximum_prescription_quantity);
		// 	if (parseFloat(row.qty) > parseFloat(row.maximum_prescription_quantity)){

		// 		frappe.throw(`Sorry, prescription exceeds maximum prescription qusntity of ${parseFloat(row.maximum_prescription_quantity)}`)
		// 	}
		// }
	},
	rate(frm, cdt, cdn) {
		const row = locals[cdt][cdn]
		if (row.qty && row.rate) {
			console.log(JSON.stringify(row.drug_name));
			var quantity = row.qty
			var rate = row.rate
			var amount = parseFloat(quantity * rate)
			row.amount = amount
			refresh_field("prescription_items")
			refreshTotals(frm)
		}
		// if(row.qty && row.maximum_prescription_quantity){
		// 	console.log(row.qty , row.maximum_prescription_quantity);
		// 	if (parseFloat(row.qty) > parseFloat(row.maximum_prescription_quantity)){
		// 		frappe.throw(`Sorry, prescription exceeds maximum prescription qusntity of ${parseFloat(row.maximum_prescription_quantity)}`)
		// 	}
		// }
	}
})
function changePayerDialog(frm) {
	frappe.call({
		method: "lonius_health.api.patients.get_payers_linked_to_patient",
		args: {
			patient: frm.doc.patient
		}

	}).then(res => {
		console.log.res
		frappe.prompt({
			label: 'Payer/Insurance',
			fieldname: 'payer',
			fieldtype: 'Link',
			reqd: 1,
			options: 'Customer',
			get_query: () => {
				return {
					filters: [
						["Customer", "name", "IN", res.message]
					]
				};
			}
		}, (values) => {
			console.log(values);
			// frm.doc.customer = values.payer
			frm.set_value({
				customer: values.payer,
				//description: 'New description'
			})
			// refresh_field('customer')
			// frm.dirty()
			frm.save()
			frappe.msgprint("Payer Changed Successfully", values.payer)
		})
	})


}
function drugAlternativeDialog(frm) {
	let data = frm.get_selected().prescription_items

	if (!data || data == null || data == undefined) {
		frappe.throw("You have not selected any items")
	}
	let selected = frm.doc.prescription_items.filter(row => { return row.name == data })[0]

	if (data.length > 1) {
		frappe.throw("Sorry, you can work with only one(1) item at a time.")
	}

	frappe.msgprint(`You have selected ${data} ${JSON.stringify(data.length)}`)
}

{/* <input type="checkbox" class="grid-row-check pull-left"></input> */ }

function dispensePrescription(frm) {
	// 6609
	frappe.warn('Are you sure to post the Items to the invoice?',
		`There are ${frm.doc.prescription_items.length} items to be dispensed`,
		() => {
			// action to perform if Continue is selected
			postPrescription(frm)
		},
		'Continue',
		true // Sets dialog as minimizable
	)



}
function postPrescription(frm) {
	frappe.call({
		method: "lonius_health.api.patients.dispense_prescription_slip",
		freeze: true,
		freeze_message:"Posting invoice...Please Wait",
		args: {
			docname: frm.doc.name
		}
	})
}

function addDrug(frm) {

}
function refreshTotals(frm) {
	let total = 0.00
	frm.doc.prescription_items.forEach(row => {
		let amount = parseFloat(row.amount)
		total = total + amount
		return total
	})

	console.log(total)
	frm.doc.total_invoice_amount = total
	refresh_field("total_invoice_amount")

}