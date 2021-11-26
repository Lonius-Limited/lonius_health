import frappe

@frappe.whitelist()
def create_procedure(doc, handler=None):
    procedure_list = doc.procedure_prescription
    if len(procedure_list) < 1:return
    patient = frappe.get_doc("Patient", doc.patient)
    for i in procedure_list:
        procedure = frappe.get_doc({
                'doctype':"Clinical Procedure",
                "status":"Draft",
                "patient": patient.name,
                "procedure_template": i.procedure_name
        })
        procedure.run_method('set_missing_values')
        procedure.insert()
    return