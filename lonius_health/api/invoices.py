# from warnings import filters
import frappe
import datetime
from frappe import _, msgprint
from frappe.utils import flt, get_defaults
from frappe.utils.data import now_datetime

import lonius_health
# CAN WE PLEASE AVOID HARD CODING ANYTHING! "Lonius Limited"


def open_invoice_exists(patient):
	invoices = frappe.get_list('Sales Invoice', filters={
		'status': 'Draft',
		'patient': patient
	})
	if len(invoices) > 0:
		return True
	return False


@frappe.whitelist()
def is_visit_active(patient):
	frappe.local.response.update(
		{"status": open_invoice_exists(patient=patient)})
	return


@frappe.whitelist()
def is_checked_in(patient):
	encounters = frappe.get_list('Patient Encounter', filters={
		'workflow_state': ('in', ('Checked In', 'Vitals Taken', 'Consultation', )),
		'patient': patient
	})
	if len(encounters) > 0:
		frappe.local.response.update({"status": True})
		return
	frappe.local.response.update({"status": False})
	return


@frappe.whitelist()
def check_in(patient, practitioner):
	# on check-in create draft encounter document
	new_encounter = frappe.get_doc({
		"doctype": "Patient Encounter",
		"patient": patient,
		"status": "Checked In",
		"practitioner": practitioner
	})
	new_encounter.append('queue_log', {
		"action": "Checked In",
		"timestamp": datetime.datetime.now(),
		"user": frappe.session.user
	})
	new_encounter.run_method('set_missing_values')
	new_encounter.insert()
	frappe.msgprint(_("Patient has successfully been checked in."),)
	return


def create_draft_vitals_doc(patient):
	encounter_doc = pending_patient_encounters(patient)
	vital_signs_doc = frappe.get_doc({
		"doctype": "Vital Signs",
		"patient": patient,
		"status": "Draft",
		"encounter": encounter_doc.get('name')
	})
	vital_signs_doc.run_method('set_missing_values')
	vital_signs_doc.insert()
	return


@frappe.whitelist()
def start_patient_visit(patient, customer):
	consultation_item = frappe.get_doc('Healthcare Settings')
	consultation_item = consultation_item.op_consulting_charge_item
	company = frappe.defaults.get_user_default("company")
	if not open_invoice_exists(patient=patient):
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"patient": patient,
			"status": "Draft",
			"company": company,
			'due_date': datetime.date.today(),
			"currency": "KES",
			"customer": customer,
			"allocate_advances_automatically": 1
		})
		invoice.append('items', {
			"item_code": consultation_item,
			"qty": 1,
		})
		invoice.run_method('set_missing_values')
		invoice.insert()
		create_draft_vitals_doc(patient=patient)
		frappe.msgprint(
			_("Patient visit for {} has been started".format(patient)),)
		return
	frappe.msgprint(_("Patient visit is already ongoing"),)
	return


def get_open_invoice(patient, customer=None):
	invoices = frappe.get_list('Sales Invoice', filters={
		'status': 'Draft',
		'patient': patient
	})
	# If customer is provided, return a list of invoices for this customer
	if customer:
		invoices = None
		invoices = frappe.get_list('Sales Invoice', filters={
			'status': 'Draft',
			'patient': patient,
			'customer': customer
		})
	if len(invoices) > 0:
		invoice = invoices[0]
		invoice = frappe.get_doc('Sales Invoice', invoice['name'])
		return invoice
	return False


def pending_procedures(patient):
	procedures = frappe.get_list('Clinical Procedure', filters={
		'status': 'Draft',
		'patient': patient
	})
	if len(procedures) > 0:
		return True
	return False


def pending_lab_tests(patient):
	lab_tests = frappe.get_list('Lab Test', filters={
		'status': 'Draft',
		'patient': patient
	})
	if len(lab_tests) > 0:
		return True
	return False


def pending_patient_encounters(patient):
	patient_encounter = frappe.get_list('Patient Encounter', filters={
		'docstatus': 0,
		'patient': patient
	})
	if len(patient_encounter) > 0:
		return patient_encounter[0]
	return False


@frappe.whitelist()
def end_visit(patient):
	invoice = get_open_invoice(patient=patient)
	if invoice:
		if pending_lab_tests(patient):
			frappe.msgprint(
				_("Failed to End Visit. Ensure all Lab Tests have been submitted."),)
			return
		if pending_procedures(patient):
			frappe.msgprint(
				_("Failed to End Visit. Ensure all Clinical Procedures have been submitted."),)
			return
		if pending_patient_encounters(patient):
			frappe.msgprint(
				_("Failed to End Visit. Ensure Patient Encounter has been submitted."),)
			return
		invoice.submit()
		frappe.msgprint(
			_("Patient visit successfully ended. Invoice has been submitted"),)
		return
	frappe.msgprint(_("Sorry, Patient visit was already ended."),)
	return


def append_lab_invoice(doc, handler=None):
	invoice = get_open_invoice(doc.patient)
	if invoice:
		invoice.append('items', {
			"item_code": doc.template,
			"qty": 1
		})
		invoice.run_method('set_missing_values')
		invoice.save()
	else:
		# FOR WHATEVER REASON, THERE IS NO INVOICE. LETS BILL THE PATIENT
		lab_items = [{
			"item_code": doc.template,
			"qty": 1
		}]
		customer = frappe.db.get_value('Patient', doc.patient, 'customer')
		make_invoice_endpoint(patient=doc.patient,
							  customer=customer, items=lab_items)
	return


def append_procedure_invoice(doc, handler=None):
	invoice = get_open_invoice(doc.patient)
	procedure_item = frappe.db.get_value(
		'Clinical Procedure Template', doc.procedure_template, 'item')
	if invoice:
		invoice.append('items', {
			"item_code": procedure_item,
			"qty": 1
		})
		invoice.run_method('set_missing_values')
		invoice.save()
	else:
		# FOR WHATEVER REASON, THERE IS NO INVOICE. LETS BILL THE PATIENT
		procedure_items = [{
			"item_code": procedure_item,
			"qty": 1
		}]
		customer = frappe.db.get_value('Patient', doc.patient, 'customer')
		make_invoice_endpoint(patient=doc.patient,
							  customer=customer, items=procedure_items)
	return


def make_invoice_endpoint(patient='', customer='', items=[]):
	# frappe.throw('2099-01-01')
	invoice = get_open_invoice(patient, customer=customer)
	company = frappe.defaults.get_user_default("company")
	if not invoice:
		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"patient": patient,
			"status": "Draft",
			"company": company,
			'due_date': '2099-01-01',
			'posting_date': datetime.date.today(),
			"currency": "KES",
			"customer": customer,
			"allocate_advances_automatically": 1
		})
		for item in items:
			invoice.append('items', item)
		invoice.run_method('set_missing_values')
		invoice.insert()
		return invoice
	for item in items:
		invoice.append('items', item)
	invoice.set('due_date','2099-01-01')
	invoice.set('payment_schedule',[])
	invoice.run_method('set_missing_values')
	invoice.save()
	return invoice


def validate_payment(doc, handler=None, ignore_zero_balance=False):
	# IF CUSTOMER IS OF TYPE COMPANY, THEN RETURN AS WE WILL ACCEPT INVOICING. IF NOT, THERE BETTER BE MONEY FIRST.
	company = frappe.defaults.get_user_default("company")
	customer_type = frappe.db.get_value(
		"Customer", doc.get('customer'), 'customer_type')
	if customer_type == 'Company':
		return
	# ONLY PROCEED IF THIS CUSTOMER IS ASSOCIATED WITH A PATIENT FILE. NEEDED TO PREVENT INTERFERENCE WITH INVOICES FROM OTHER APPS
	patient_count = frappe.db.count('Patient', {'customer': doc.get('customer')})
	if patient_count == 0: return
	
	from erpnext.selling.doctype.customer.customer import get_customer_outstanding
	from frappe.utils.data import fmt_money
	balance = get_customer_outstanding(doc.get('customer'), company, True) * -1
	if (flt(doc.get('total')) > flt(balance)):
		needed_to_proceed = fmt_money(doc.get('total') - balance)
		balance = fmt_money(balance - (doc.get('total') -
							(doc.get('total') - balance)))
		currency = get_defaults().get('currency')

		# INSERT DRAFT PAYMENT ENTRY
		amount = flt(doc.get('total')) - flt(balance)
		# payment_doc = create_payment_entry(doc.get('customer'), amount)
		link_to_latest_p_entr = None if "Accounts User" not in frappe.get_roles(frappe.session.user) else get_link_to_latest_p_entr(doc.get("customer"),float(needed_to_proceed.replace(",","")))
		message = f'The client needs to pay {currency}<b> {needed_to_proceed} </b> in order to proceed with this service. There is only {currency}<b> {balance} </b> available in their account.'
		print(doc.ignore_customer_balance_check)
		if doc.ignore_customer_balance_check==1:
			frappe.msgprint(message)
			return
		if link_to_latest_p_entr: frappe.msgprint(link_to_latest_p_entr)
		frappe.throw(message)
	return
def get_link_to_latest_p_entr(customer, amount):
	latest = frappe.get_value("Payment Entry",dict(party=customer,party_type="Customer",paid_amount=amount,docstatus="Draft"),'name') or create_payment_entry(customer, amount)
	if latest:
		return f"<a target='_blank' href='/app/payment-entry/{latest}'>Click here to submit a payment of {amount} before proceeding :Ref:{latest}</a>"

def create_payment_entry(customer, amount):
	company = frappe.defaults.get_user_default("company")
	currency = get_defaults().get('currency')
	account = frappe.db.get_values('Mode of Payment Account', {'company': company, 'parenttype': 'Mode of Payment', 'parent': 'Cash'},['default_account'])[0][0]
	doc = frappe.get_doc({
		"doctype": "Payment Entry",
		"payment_type": 'Receive',
		"posting_date": datetime.date.today(),
		"company": company,
		'party_type': 'Customer',
		'party': customer,
		"currency": "KES",
		"mode_of_payment": 'Cash',
		"paid_amount": amount,
		"received_amount": amount,
		"custom_remarks ": 1,
		"target_exchange_rate": 1,
		"paid_to": account,
		"paid_to_account_currency": currency
		# "remarks": remarks,
		# "reference__doc": ref_doc.get('doctype'),
		# "reference_name" ref_doc.get()
	})
	doc.run_method('set_missing_values')
	doc.insert()
	frappe.db.commit()
	return doc.get('name')
def close_patient_invoices():
	from datetime import datetime, timedelta, date
	# Syntax for UOM : datetime.timedelta(days, hours, weeks) All Lower case
	'''
	:param acceptable_expiry: Integer value of the acceptable expiry of an invoice
	:param acceptable_expiry_uom: String value of the unit of measure to measure expiry of an invoice; Can be days,hours or weeks

	'''
	# We can get this from a settings doctype
	acceptable_expiry, acceptable_expiry_uom = 24, 'hours'
	#######################################################
	
	kwargs ={acceptable_expiry_uom:acceptable_expiry}
	now_datetime = datetime.now()
	expiry_datetime = now_datetime - timedelta(**kwargs)
	overdue_drafts = frappe.get_all("Sales Invoice",filters=dict(docstatus=0,posting_date=["<",expiry_datetime]))
	if not overdue_drafts: return
	def _close_invoice(doc):
		#####Do not close if patient has Inpatient Record with Status ["Admission Scheduled","Admitted","Discharge Scheduled"]
		if frappe.get_all("Inpatient Record",filters=dict(patient=doc.patient,status=["IN",["Admission Scheduled","Admitted","Discharge Scheduled"]])): return
		doc.set('allocate_advances_automatically', 1)
		# if getdate(due_date) < getdate(posting_date):
		doc.set('posting_date', date.today())
		doc.set('payment_schedule',[])
		doc.set('due_date', date.today() + timedelta(weeks=4))
		doc.set('ignore_customer_balance_check',1)
		doc.save(ignore_permissions=True)
		doc.reload()
		doc.submit()
		frappe.db.commit()
		print("{} submitted".format(doc.get("name")))
	docs = [frappe.get_doc("Sales Invoice",x.get("name")) for x in overdue_drafts[:5]]
	list(map(lambda x: _close_invoice(x),docs))
	return overdue_drafts
