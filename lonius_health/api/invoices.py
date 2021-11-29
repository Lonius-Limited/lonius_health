# from warnings import filters
import frappe
import datetime
from frappe import _

def open_invoice_exists(patient):
    invoices = frappe.get_list('Sales Invoice', filters={
        'status':'Draft',
        'patient': patient
    })
    if len(invoices) > 0:
        return True
    return False

@frappe.whitelist()
def is_visit_active(patient):
    frappe.local.response.update({"status": open_invoice_exists(patient=patient)})
    return

@frappe.whitelist()
def check_in(patient, practitioner):


    pass



@frappe.whitelist()
def start_patient_visit(patient):
    consultation_item = frappe.get_doc('Healthcare Settings')
    consultation_item = consultation_item.op_consulting_charge_item
    if not open_invoice_exists(patient=patient):
        invoice = frappe.get_doc({
            "doctype":"Sales Invoice",
            "patient": patient,
            "status":"Draft",
            "company": frappe.defaults.get_user_default("Company"),
            'due_date': datetime.date.today(),
            "currency":"KES",
            "customer":patient
        })
        invoice.append('items', {
                "item_code": consultation_item,
                "qty": 1,
        })
        invoice.run_method('set_missing_values')
        invoice.insert()
        frappe.msgprint(_("Patient visit for {} has been started".format(patient)),)
        return
    frappe.msgprint(_("Patient visit is ongoing"),)
    return


def get_open_invoice(patient):
    invoices = frappe.get_list('Sales Invoice', filters={
        'status':'Draft',
        'patient': patient
    })
    if len(invoices) > 0:
        invoice = invoices[0]
        invoice = frappe.get_doc('Sales Invoice', invoice['name'])
        return invoice
    return

def append_lab_invoice(doc, handler=None):
    invoice = get_open_invoice(doc.patient)
    invoice.append('items',{
        "item_code": doc.lab_test_name,
        "qty": 1
    })
    invoice.run_method('set_missing_values')
    invoice.save()
    return


def append_procedure_invoice(doc, handler=None):
    invoice = get_open_invoice(doc.patient)
    invoice.append('items',{
        "item_code": doc.procedure_template,
        "qty": 1
    })
    invoice.run_method('set_missing_values')
    invoice.save()
    return