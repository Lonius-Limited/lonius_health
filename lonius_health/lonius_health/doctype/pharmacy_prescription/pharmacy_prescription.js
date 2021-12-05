// Copyright (c) 2021, Lonius Limited Innovation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pharmacy Prescription', {

	refresh: (frm) => {
		if (!frm.is_new()) {
			frm.disable_save();
		}

		if (frm.doc.encounter) {//DISABLE ADDING DRUGS FOR ENCOUNTER PRESCRIPTIONS
			frm.get_field("prescription_items").grid.cannot_add_rows = true;
			frm.get_field("prescription_items").grid.only_sortable();
			refresh_field('prescription_items')
		}
		// frm.get_field("prescription_items").grid.only_sortable();

		if (frm.doc.status == 'Prescription Ready') {
			frm.remove_custom_button(__("Make a Prescription Refill"))
			frm.add_custom_button(__("Change Payer"), function () {
				//perform desired action such as routing to new form or fetching etc.
				changePayerDialog(frm)
			});
			frm.add_custom_button(__("Dispense Prescription"), function () {
				//perform desired action such as routing to new form or fetching etc.
				frm.save()
				dispensePrescription(frm)
			});
			// frm.fields_dict['prescription_items'].grid.add_custom_button('Add Drug', () => { addDrug(frm) }, 'primary')
			frm.fields_dict['prescription_items'].grid.add_custom_button('Check Alternatives for Selected Drug', () => { drugAlternativeDialog(frm) }, 'primary')


			// frm.fields_dict['prescription_items'].grid.change_custom_button_type('danger');

			// }
		}
		if (frm.doc.status == 'Prescription Serviced') {
			frm.set_intro('This prescription has already been serviced. Please Click <strong>Make a Prescription Refill</strong> to dispense/bill remaining quantities.');
			// frm.disable_save();
			frm.add_custom_button(__("Make a Prescription Refill"), function () {
				//perform desired action such as routing to new form or fetching etc.	
				if(!frm.doc.encounter){
					frappe.throw("Operation not permitted for external prescriptions")
				}

			});
		}
	},
	onload_post_render: (frm) => {

		// frm.get_field("prescription_items").grid.cannot_add_rows = true;
		// frm.get_field("prescription_items").grid.only_sortable();
		// refresh_field('prescription_items')
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
					r.message = "Company" ? frm.doc.is_insurance_patient = 1 : frm.doc.is_insurance_patient = 0
					refresh_field("is_insurance_patient")
				}
			}
		});

	}

});
frappe.ui.form.on('Pharmacy Prescription Item', {
	refresh(frm) {
		// frm.get_field("prescription_items").grid.cannot_add_rows = true;
		// frm.doc.encounter ? frm.set_df_property('prescription_item','drug_code', 'read_only', 1) : frm.set_df_property('prescription_item','drug_code', 'read_only', 0)

	},
	prescription_items_add: (frm) => {

	},
	prescription_items_remove: (frm) => {
		refreshTotals(frm)
	},
	period: (frm, cdt, cdn) => {
		const row = locals[cdt][cdn]
		console.log(row.dosage);
		if (!row.dosage) {
			frappe.throw("Sorry, you have to provide Dosage first! i.e 1-1-1,1-0-1 etc")
		}
		// let qty = frappe.get_doc("Drug Prescription",row.drug_code).get_quantity()
// UPDATE `tabProcurement Plan` set docstatus=2 where name = 'PROC-CEOs OFFICE - MTRH-2021-2022-108312-2';
		console.log(row.period, row.interval,frm.doc.patient,frm.doc.customer);
		frappe.call({
			method: "lonius_health.api.patients.get_prescription_qty",
			freeze:true,
			freeze_message:"Computing Stock Qty and Fetching Price... Please Wait",
			args: {
				patient:frm.doc.patient,
				customer: frm.doc.customer,
				warehouse:frm.doc.pharmacy,
				drug: row.drug_code,
				dosage: row.dosage,
				period: row.period,
				interval: row.interval
			}
		}).then(res => {
			console.log(res)
			row.qty = res.message[0] || 0
			row.rate = res.message[1] || 0
			row.amount = row.rate * row.qty
			refresh_field("prescription_items")
			refreshTotals(frm)
			
		})


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
	}
})
function changePayerDialog(frm) {
	frappe.call({
		method: "lonius_health.api.patients.get_payers_linked_to_patient",
		freeze: true,
		freeze_message: "Please wait as we fetch applicable Payers for patient",
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
			frm.set_value({
				customer: values.payer,
			})
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

	// frappe.msgprint(`You have selected ${data} ${JSON.stringify(selected)}`)
	// let route =
	let filters = [
		["Item Alternative", "item_code", "IN", [selected.drug_code]],
		["Item Alternative", "alternative_item_code", "IN", [selected.drug_code]]
	]

	let d = new frappe.ui.Dialog({
		title: 'Drug Alternative Search',
		fields: [
			{
				fieldname: 'html_title',
				options: `<p>You will find alternatives for <em>${selected.drug_name}</em> if it is setup in Item Alternative DocType <hr><strong>NB: There might be slight price changes.</strong>`,
				fieldtype: 'HTML'
			},
			{
				label: 'Alternative Drug',
				fieldname: 'last_name',
				fieldtype: 'Link',
				reqd: 1,
				options: 'Item Alternative',
				get_query: () => {
					return {
						or_filters:
							filters
					};
				}
			}
		],
		primary_action_label: 'Submit',
		primary_action(values) {
			console.log(values);//
			d.hide();
			//Go to DB, fetch rate of alternative and replace on this table.
		}
	});

	d.show();

}

// {/* <input type="checkbox" class="grid-row-check pull-left"></input> */ }

function dispensePrescription(frm) {
	// 6609
	frappe.warn('Are you sure to post the Items to the invoice ?',
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
		freeze_message: "Posting invoice...Please Wait",
		args: {
			docname: frm.doc.name
		}
	}).then(result => {
		frappe.msgprint("Prescription dispensed successfully.")
		// frm.set('status', 'Prescription Serviced')
		frm.reload_doc()
		frm.refresh();
	})
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