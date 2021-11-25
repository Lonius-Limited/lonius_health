import frappe

@frappe.whitelist()
def get_pending_encounter_prescriptions():
    return {}
    payload = dict(_dt="encounters")
    todays_encounters = frappe.get_all("Patient Encounter",filters=dict(invoiced=0))
    for encounter in todays_encounters:
        obj ={}
        doc = frappe.get_doc("Patient Encounter", encounter.get("name"))
        patient_name = doc.patient_name
        payload[patient_name] = obj


    return obj