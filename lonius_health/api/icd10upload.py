# from .icd10 import icd10codes

import frappe
import icd10

MEDICAL_STANDARD = "ICD10"
DOCTYPE = "Medical Code"
ALL_CODES = icd10.codes


def upload():
    codes = list(ALL_CODES.keys())
    if not frappe.get_value("Medical Code Standard", MEDICAL_STANDARD,'name'):
        frappe.get_doc(dict(doctype="Medical Code Standard",
                            medical_code=MEDICAL_STANDARD)).insert()
        frappe.db.commit()
    list(map(lambda x: upload_code(x), codes))


def upload_code(code):
    payload = ALL_CODES[code]
    description, is_billable = payload[1], payload[0]
    if frappe.get_value(DOCTYPE, dict(code=code)):
        print("{} {}: =>Already exists".format(code,description))
        return
    args = dict(doctype=DOCTYPE, medical_code_standard=MEDICAL_STANDARD,
                code=code, description=description, is_billable=is_billable)
    print(args)
    frappe.get_doc(args).insert()
    frappe.db.commit()
