# from warnings import filters
import frappe
import datetime

CONSULATION_ITEM = "CONSULTATION"
COMPANY = "Lonius Limited"
def open_invoice_exists(patient):
    invoices = frappe.get_list('Sales Invoice', filters={
        'status':'Draft',
        'patient': patient
    })
    if len(invoices) > 0:
        return True
    return False

@frappe.whitelist()
def start_patient_visit(patient):
    if not open_invoice_exists(patient=patient):
        invoice = frappe.get_doc({
            "doctype":"Sales Invoice",
            "patient": patient,
            "status":"Draft",
            "company": COMPANY,
            'due_date': datetime.date.today(),
            "currency":"KES",
            "customer":patient
        })
        invoice.append('items', {
                "item_code": CONSULATION_ITEM,
                "qty": 1,
        })
        invoice.run_method('set_missing_values')
        invoice.insert()
        return
    
    return

