import frappe

def execute():
    # INSERT SCHEDULED JOB FOR REQUESTING REQUIRED DRUGS
    the_job = 'icd10.upload'
    if not frappe.get_value("Scheduled Job Type",the_job):
        doc = frappe.get_doc({"name":the_job,"owner":"Administrator","creation":"2021-05-31 14:36:26.237459","docstatus":0,"stopped":0,"method":"lonius_health.after_migrate_functions.icd10.upload","frequency":"Cron","cron_format":"0 22 17 12 5","create_log":1,"doctype":"Scheduled Job Type"})
        doc.insert()
    the_job = 'invoices.close_patient_invoices'
    if not frappe.get_value("Scheduled Job Type",the_job):
        doc = frappe.get_doc({"name":the_job,"owner":"Administrator","creation":"2021-05-31 14:36:26.237459","docstatus":0,"stopped":0,"method":"lonius_health.api.invoices.close_patient_invoices","frequency":"Cron","cron_format":"*/30 * * * *","create_log":1,"doctype":"Scheduled Job Type"})
        doc.insert()
    