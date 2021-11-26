import frappe, json
from frappe.utils import (
	get_files_path,
	cstr,
	getdate,
	get_hook_method,
	call_hook_method,
	random_string,
	get_fullname,
	today,
	cint,
	flt,
	get_url_to_form,
	strip_html,
	money_in_words,
)

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
@frappe.whitelist()
def make_encounter_review(docname , data):
    payload = json.loads(data)
    linked_doc = frappe.get_doc("Patient Encounter", docname)
    args = dict(doctype="Patient Encounter",patient = linked_doc.get("patient"),
    encounter_date =linked_doc.get("encounter_date"),
    encounter_time=linked_doc.get("encounter_time"),practitioner=linked_doc.get("practitioner"), encounter_comment=payload.get("notes"))
    doc = frappe.get_doc(args)
    prescription = payload.get("prescription")
    if prescription:
        for drug in prescription:
            row = doc.append('drug_prescription',{})
            row.drug_code = drug.get("item")
            row.dosage = drug.get("dosage")
            row.period = drug.get("duration")
            row.dosage_form = drug.get("dosage_form")
    doc.insert()
    frappe.db.set_value("Patient Encounter", docname, dict(is_reviewed=1,linked_encounter=doc.get("name")))
    review = get_link_to_form_new_tab("Patient Encounter", doc.get("name"),label='Review Document')
    frappe.msgprint("Review document posted here {}. Please Click the link to Submit the document.".format(review))
@frappe.whitelist()
def get_linked_review(docname):
    review = get_link_to_form_new_tab("Patient Encounter", docname,label='Review Document')
    frappe.throw(f'Sorry, a review has already been made for this document. Click on this {review} to proceed')
    return review
    # return frappe.get_value("Patient Encounter", dict(linked_encounter=docname)) or ''
def get_link_to_form_new_tab(doctype, name, label=None):
	if not label: 
		label = name

	return """<a target="_blank" href="{0}">{1}</a>""".format(
		get_url_to_form(doctype, name), label
	)
