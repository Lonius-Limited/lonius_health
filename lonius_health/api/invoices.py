# from warnings import filters
import frappe
import datetime
from frappe import _, msgprint

# CAN WE PLEASE AVOID HARD CODING ANYTHING! "Lonius Limited"
COMPANY = frappe.defaults.get_user_default("company")


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
    vital_signs_doc = frappe.get_doc({
        "doctype": "Vital Signs",
        "patient": patient,
        "status": "Draft"
    })
    vital_signs_doc.run_method('set_missing_values')
    vital_signs_doc.insert()
    return


@frappe.whitelist()
def start_patient_visit(patient, customer):
    consultation_item = frappe.get_doc('Healthcare Settings')
    consultation_item = consultation_item.op_consulting_charge_item
    if not open_invoice_exists(patient=patient):
        invoice = frappe.get_doc({
            "doctype": "Sales Invoice",
            "patient": patient,
            "status": "Draft",
            "company": COMPANY,
            'due_date': datetime.date.today(),
            "currency": "KES",
            "customer": customer
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
    #If customer is provided, return a list of invoices for this customer
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
        return True
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
            "item_code": doc.lab_test_name,
            "qty": 1
        })
        invoice.run_method('set_missing_values')
        invoice.save()
    else:
        # FOR WHATEVER REASON, THERE IS NO INVOICE. LETS BILL THE PATIENT
        lab_items = [{
            "item_code": doc.lab_test_name,
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
    invoice = get_open_invoice(patient, customer=customer)
    if not invoice:
        invoice = frappe.get_doc({
            "doctype": "Sales Invoice",
            "patient": patient,
            "status": "Draft",
            "company": COMPANY,
            'due_date': datetime.date.today(),
            'posting_date': datetime.date.today(),
            "currency": "KES",
            "customer": customer
        })
        for item in items:
            invoice.append('items', item)
        invoice.run_method('set_missing_values')
        invoice.insert()
        return invoice
    for item in items:
        invoice.append('items', item)
    invoice.run_method('set_missing_values')
    invoice.save()
    return invoice


def validate_payment(doc, handler=None):
    # IF CUSTOMER IS OF TYPE COMPANY, THEN RETURN AS WE WILL ACCEPT INVOICING. IF NOT, THERE BETTER BE MONEY FIRST.
    customer_type = frappe.db.get_value(
        "Customer", doc.get('customer'), 'customer_type')
    if customer_type == 'Company':
        return
    from erpnext.selling.doctype.customer.customer import get_customer_outstanding
    from frappe.utils import get_defaults
    from frappe.utils.data import fmt_money
    balance = get_customer_outstanding(doc.get('customer'), COMPANY, True) * -1
    if (doc.get('total') > balance):
        needed_to_proceed = fmt_money(doc.get('total') - balance)
        balance = fmt_money(balance)
        currency = get_defaults().get('currency')
        frappe.throw(
            f'The client needs to pay {currency}<b> {needed_to_proceed} </b> in order to proceed with this service. There is only {currency}<b> {balance} </b> available in their account.')
    return
