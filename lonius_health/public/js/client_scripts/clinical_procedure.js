// alert("cp S Working...")
frappe.ui.form.on('Clinical Procedure', {
	refresh(frm) {
		if(!frm.is_new()){ 
	       updateSchemeDashboardcp(frm)
	   }
	}
})

function updateSchemeDashboardcp(frm){
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