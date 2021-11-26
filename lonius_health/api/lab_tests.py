import frappe


@frappe.whitelist()
def create_lab_test(doc, handler=None):
    lab_tests = doc.lab_test_prescription
    if len(lab_tests) < 1:return
    patient = frappe.get_doc("Patient", doc.patient)
    for i in lab_tests:
        lab_test = frappe.get_doc({
                'doctype':"Lab Test",
                "status":"Draft",
                "patient": patient.name,
                "template": i.lab_test_name,
                "patient_sex": patient.sex
            })
        lab_test.run_method('set_missing_values')
        lab_test.insert()
        
    return 