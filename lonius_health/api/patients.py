import frappe
import json
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
import datetime
from erpnext.stock.get_item_details import get_item_details

price_list,price_list_currency = frappe.db.get_values('Price List', {'selling': 1}, ['name', 'currency'])[0]


@frappe.whitelist()
def get_pending_encounter_prescriptions(warehouse=None):
	to_return = []
	todays_encounters = frappe.get_all("Patient Encounter", filters=dict(
		prescription_serviced=0, encounter_date=datetime.date.today()), fields=["*"])
	for encounter in todays_encounters:
		prescription = encounter_has_drugs(encounter.get("name"), patient=encounter.get("patient"), warehouse=warehouse)
		if not prescription: continue
		row = {}
		row = dict(patient=encounter.get("patient"),
				   patient_name=encounter.get("patient_name"), encounter=encounter.get("name"),
				   practitioner_name=encounter.get("practitioner_name"), prescription=prescription)
		to_return.append(row)

	return to_return
def dispense_prescription(payload):
	pass

	#frappe.get_all("Patient Encounter",filters=dict(encounter_date=datetime.date.today()), fields=["drug_prescription"])


@frappe.whitelist()
def make_encounter_review(docname, data):
	payload = json.loads(data)
	linked_doc = frappe.get_doc("Patient Encounter", docname)
	args = dict(doctype="Patient Encounter", patient=linked_doc.get("patient"),
				encounter_date=linked_doc.get("encounter_date"),
				encounter_time=linked_doc.get("encounter_time"), practitioner=linked_doc.get("practitioner"), encounter_comment=payload.get("notes"))
	doc = frappe.get_doc(args)
	prescription = payload.get("prescription")
	if prescription:
		for drug in prescription:
			row = doc.append('drug_prescription', {})
			row.drug_code = drug.get("item")
			row.dosage = drug.get("dosage")
			row.period = drug.get("duration")
			row.dosage_form = drug.get("dosage_form")
	doc.insert()
	frappe.db.set_value("Patient Encounter", docname, dict(
		is_reviewed=1, linked_encounter=doc.get("name")))
	review = get_link_to_form_new_tab(
		"Patient Encounter", doc.get("name"), label='Review Document')
	frappe.msgprint(
		"Review document posted here {}. Please Click the link to Submit the document.".format(review))


@frappe.whitelist()
def get_linked_review(docname):
	review = get_link_to_form_new_tab(
		"Patient Encounter", docname, label='Review Document')
	frappe.throw(
		f'Sorry, a review has already been made for this document. Click on this {review} to proceed')
	return review
	# return frappe.get_value("Patient Encounter", dict(linked_encounter=docname)) or ''


def get_link_to_form_new_tab(doctype, name, label=None):
	if not label:
		label = name

	return """<a target="_blank" href="{0}">{1}</a>""".format(
		get_url_to_form(doctype, name), label
	)


def encounter_has_drugs(encounter, patient=None, warehouse=None):
	prescription = frappe.get_all("Drug Prescription", filters=dict(parent=encounter), fields=["*"])
	drugs = []
	for drug in prescription:
		row = frappe._dict(drug)
		qty = frappe.get_doc("Drug Prescription",drug.get("name")).get_quantity()
		row["qty"] = qty
		if not warehouse:
			row["rate"] = 0.0
		customer = frappe.get_value("Patient",patient,'customer')
		args = {
				'doctype': 'Sales Invoice',
				'item_code': drug.get("drug_code"),
				'company': frappe.defaults.get_user_default("Company"),
				'warehouse': warehouse,
				'customer': customer,
				'selling_price_list': price_list,
				'price_list_currency': price_list_currency,
				'plc_conversion_rate': 1.0,
				'conversion_rate': 1.0
				}
		item_details = get_item_details(args)
		item_price = item_details.price_list_rate or 0.0
		row["rate"] = item_price 
		drugs.append(row)
	return drugs
@frappe.whitelist()
def get_allocated_warehouses(user=None):
	if not user: user = frappe.session.user
	perms = frappe.get_all("User Permission",filters=dict(user=user,allow="Warehouse",applicable_for="Sales Invoice"),fields=["for_value"])
	if not perms: return []
	return [x.get("for_value") for x in perms]