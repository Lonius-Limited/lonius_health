frappe.ui.form.on('Patient Encounter', {
	refresh(frm) {
	    if(!frm.is_new()){ 
	       updateSchemeDashboardpe(frm)
           quickVitalsEncounter(frm)
	   }
	    if(frm.doc.docstatus==1){
    	    frm.add_custom_button(__("Review Patient"), function(){
    	       // 	var content = $(this).parents('.timeline-item:first').find('.timeline-item-content').html();
    				var doc = frappe.model.get_new_doc('Patient Encounter');
    				doc.patient = frm.doc.patient;
    				
    				doc.practitioner = frm.doc.practitioner;
    				frappe.set_route('Form', 'Patient Encounter', doc.name);
                })
	    }
	},
	lab_profiles: (frm)=> {
	    var picked_lab_profile = frm.doc.lab_profiles;
	    console.log('Lab Profiles Picked + ' + picked_lab_profile);
	    frappe.call({
            method: "lonius_health.api.encounter.get_lab_profile_tests",
            args:{
                docname: picked_lab_profile
            }
        }).then(r =>{
            console.log(r);
            for (let i = 0; i < r.message.length; i++) {
                 frm.add_child('lab_test_prescription', {
                    lab_test_code: r.message[i].lab_test
                });
                
                frm.refresh_field('lab_test_prescription');
            }
        });
	}
});
function reviewPt(frm){
    	// your code here
		frappe.prompt([
		     {
                options: '<p>You can enter review notes and also add prescriptions</p>Ps: this will create another Encounter Document for this patient, and can only be done once',
                fieldtype: 'HTML'
            },
            {
                label: 'Add Notes',
                fieldname: 'notes',
                fieldtype: 'Text'
            },
            {
                label: 'Prescriptions',
                fieldname: 'presc1',
                reqd: 1,
                fieldtype: 'Section Break'
            },
           
            {
            label: "Additional Pharmacy Prescription(Optional)",
            fieldname: "prescription",
            fieldtype: "Table",
            read_only: 1,
            options: "Prescription",
            fields: [

                {
                    fieldtype: "Link",
                    options: "Item",
                    fieldname: "item",
                    in_list_view: 1,
                    label: "Item",
                    "get_query": function () {
                        return {
                            filters: {
                                is_stock_item: 0,
                            }
                        }
                    }
                },
                {
                    fieldtype: "Link",
                    fieldname: "dosage",
                    read_only: 1,
                    in_list_view: 1,
                    label: "Dosage",
                    options: "Prescription Dosage"
                },
                {
                    fieldtype: "Link",
                    fieldname: "duration",
                    read_only: 1,
                    in_list_view: 1,
                    label: "Duration",
                    options: "Prescription Duration"
                },{
                    fieldtype: "Link",
                    fieldname: "dosage_form",
                    read_only: 1,
                    in_list_view: 1,
                    label: "Duration",
                    options: "Dosage Form"
                },
                                
            ],
        },
        ], (values) => {
            frappe.call({
                method: "lonius_health.api.patients.make_encounter_review",
                args:{
                    docname: frm.doc.name,
                    data : values
                }
            })
        })
}
function get_linked_review(frm){
    // let docname = frm.doc.linked_encounter
    // frappe.throw(docname)
    let review = ''
    frappe.call({
        method: "lonius_health.api.patients.get_linked_review",
        args:{
            docname: frm.doc.linked_encounter
        }
    }).then(r =>{
        console.log(r)
        review = r.message
    })
    return review
}
function updateSchemeDashboardpe(frm){
    //Pass
    frappe.call({
        method:"lonius_health.api.invoices.get_insurance_limit_html",
        args:{
            "patient":frm.doc.patient,
            // "insurance": frm.doc.customer
        }
    }).then(r=>{
        console.log(r)
        frm.dashboard.add_section(r.message);
        frm.dashboard.show();
    })
}

function quickVitalsEncounter(frm){
    //Pass
    let patient = frm.doc.patient
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