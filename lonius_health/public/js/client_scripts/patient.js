frappe.ui.form.on('Patient', {
    onload_post_render(frm){
        if(!frm.is_new()){ 
            // frappe.throw(frm.doc.name+" ->")  
            let pt = frm.doc.name 
            frappe.msgprint("Updating dashboard for "+pt)   
            updateSchemeDashboardPt(frm, pt)
            quickVitals(frm)
        }
    },
	refresh(frm) {
        if(!frm.is_new()){ 
            // frappe.throw(frm.doc.name+" ->")  
            let pt = frm.doc.name 
            frappe.msgprint("Fetching dashboard for "+pt)   
            updateSchemeDashboardPt(frm, pt)
            quickVitals(frm)
        }
        ///////
		let d = new frappe.ui.Dialog({
            title: 'Provide the following details',
            fields: [
                {
                    fieldtype: "Link",
                    fieldname: "practitioner",
                    label: "Consultation Practioner",
                    reqd: 1,
                    options: "Healthcare Practitioner",
                },
            ],
            primary_action_label: 'Check In',
            primary_action(values) {
                var patient = frm.doc.name
                console.log(values);
                frappe.call({
                    method: "lonius_health.api.invoices.check_in", //dotted path to server method
                    args: {patient:patient, practitioner: values.practitioner},
                    callback: function(r) {
                        // code snippet
                        console.log(r)
                    }
                 })
                d.hide();
            }
        });
        
        let insurance_list =[]
		frm.doc.insurance_details.forEach(row=>insurance_list.push(row.insurance_name))
		if(frm.doc.customer){
		    insurance_list.push(frm.doc.customer)
		}
		
        let startVisitDialog = new frappe.ui.Dialog({
            title: 'Provide the following details',
            fields: [
                { 
                    fieldtype: "Link", 
                    fieldname: "insurance", 
                    label: "Payer", 
                    options: "Customer", 
                    get_query: function() { 
                        return { 
                            filters: [["Customer","name", 'IN', insurance_list]] 
                        }
                    }
                },
            ],
            primary_action_label: 'Start Visit',
            primary_action(values) {
                var patient = frm.doc.name
                console.log(values);
                console.log(patient);
                frappe.call({
                    method: "lonius_health.api.invoices.start_patient_visit", //dotted path to server method
                    args: {patient:frm.doc.name, customer: values.insurance},
                    callback: function(r) {
                        // code snippet
                        console.log(r)
                        frm.refresh()
                    }
                })
                // do if (patient === Smart Patient) Validation Check
                frappe.call({
                    method: "smartlink_integration.smart.initiate_visit", //dotted path to server method
                    args: {patient:frm.doc.name, customer: values.insurance},
                    callback: function(r) {
                        // code snippet
                        console.log(r)
                        if(r.message.status !== "success"){
                            msgprint('Failed to initiate visit on Smart. \nConfirm that the correct details were captured.');
                        }
                    }
                })
                startVisitDialog.hide();
            }
        });
        
		frappe.call({
            method: "lonius_health.api.invoices.is_checked_in", //dotted path to server method
            args: {patient:frm.doc.name},
            callback: function(r) {
                if(r.status === false){
                    frm.add_custom_button(__("Check In"), function() {
                        // When this button is clicked, do this
                        d.show();
            		});
                }
            }
		})
		    
		
		frappe.call({
            method: "lonius_health.api.invoices.is_visit_active", //dotted path to server method
            args: {patient:frm.doc.name},
            callback: function(r) {
                console.log(r)
                if(r.status === true){
                    frm.add_custom_button(__("End Visit"), function() {
                        // When this button is clicked, do this
                        frappe.call({
                            method: "lonius_health.api.invoices.end_visit", //dotted path to server method
                            args: {patient:frm.doc.name},
                            callback: function(r) {
                                console.log(r)
                            }
                        })
		            });
                } else {
                    frm.add_custom_button(__("Start Visit"), function() {
                        // When this button is clicked, do this
                        startVisitDialog.show();
    		        });
                }
            }
        })
	}
})

function updateSchemeDashboardPt(frm, patient){
    frappe.call({
        method:"lonius_health.api.invoices.get_insurance_limit_html",
        args:{
            "patient":patient
        }
    }).then(r=>{
        console.log(r)
        frm.dashboard.add_section(r.message);
        frm.dashboard.show();
    })
}
function quickVitals(frm){
    //Pass
    let patient = frm.doc.name
    frappe.call({
        method:"lonius_health.api.patients.get_latest_vitals",
        args:{
            "patient":patient
        }
    }).then(r=>{
        console.log(r)
        frm.dashboard.add_section(r.message);
        frm.dashboard.show();
    })
}