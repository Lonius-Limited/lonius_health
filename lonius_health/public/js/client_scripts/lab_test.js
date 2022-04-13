frappe.ui.form.on('Lab Test', {
	onload(frm){
		if(!frm.is_new() && frm.doc.docstatus==1){ 
			// updateSchemeDashboardLT(frm)
			// frm.dirty()
			// frm.save()
			// frappe.call({
			// 	method:"lonius_health.lonius_laboratory.api.lab_test.consolidated_lab_tests_endpoint",
			// 	args:{
			// 		"docname":frm.doc.name
			// 	}

			// }).then(
			// 	// frm.reload_doc()
			// 	)
		}
	},
    refresh:(frm)=>{
        if(!frm.is_new()){ 
	       updateSchemeDashboardLT(frm)
	   }
    },
    before_workflow_action: (frm) => {
        let promise = new Promise((resolve, reject) => {
            if (frm.selected_workflow_action === "Reject"){
    		    frappe.prompt(
    		        {
    		            fieldtype:"Data", 
        		        label: "Reason",
        		        fieldname:"reason",
        		        reqd: 1,
        			    description: "Reason for rejecting the Lab Test"
    		        }, 
    		        function(data) {
    		            if (data && !data.exc){
    						frappe.call({
    							method: 'frappe.client.set_value',
    							args: {
    								doctype: frm.doctype,
    								name: frm.docname,
    								fieldname: 'lab_test_comment',
    								value: data.reason
    							},
    							callback: function(res){
    								frm.reload_doc();
    							}
    						});
    						resolve();
    					} else {
    					    reject();
    					}
            			
    		        }, __("Provide Reason"), __("Reject Test")
    	        );
    		} 
        });
	},
	
	 after_workflow_action: (frm) => {
		if (frm.doc.workflow_state === "Sample Taken"){
		    // frappe.set_route("Form", "Sample Collection");
		} 
	}
})

function updateSchemeDashboardLT(frm){
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