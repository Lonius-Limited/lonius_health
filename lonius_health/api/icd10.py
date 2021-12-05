# import icd10, frappe

# ALL_CODES = icd10.codes

# MEDICAL_STANDARD ="ICD10"
# DOCTYPE = "Medical Code"
# def upload():  
#     codes = list(ALL_CODES.keys())
#     list(map(lambda x: upload_code(x),codes))
# def upload_code(code):
#     if frappe.get_value(DOCTYPE, dict(code=code)): return
#     payload = ALL_CODES[code]
#     description, is_billable= payload[1], payload[0]
#     args = dict(doctype=DOCTYPE, medical_code_standard=MEDICAL_STANDARD,code=code,description=description,is_billable=is_billable)
#     print(args)
#     frappe.get_doc(args).insert()
#     frappe.db.commit()