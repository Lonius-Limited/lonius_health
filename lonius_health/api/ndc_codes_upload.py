import frappe,json, datetime
from lonius_health.api.ndc_codes import ndc_codes
"""
{
 "ndc_codes": [
        {
            "ndc_code": "0002-1200",
            "medicine_name": "Florbetapir F 18",
            "uom": "INJECTION, SOLUTION",
            "dosage_form": "INTRAVENOUS",
            "strength": "51 mCi/mL",
            "classification": "Radioactive Diagnostic Agent [EPC],Positron Emitting Activity [MoA]"
        },
....]
}
"""
def upload():
    ALL_CODES = ndc_codes().get("ndc_codes")
    frappe.db.sql("DELETE FROM `tabDrug`")
    frappe.db.sql("DELETE FROM `tabDrug Stock Detail`")
    frappe.db.sql("DELETE FROM `tabDrug Classification`")
    frappe.db.sql("DELETE FROM `tabDosage Form` WHERE name!='Per Oral'")
    frappe.db.commit()
    for args in ALL_CODES:
        ###MEDICINE
        if len(args.get("strength")) > 139: continue
        if len(args.get("medicine_name")) > 139: continue
        if len(args.get("dosage_form")) > 139: continue
        if not frappe.get_value("Dosage Form",args.get("dosage_form")) and args.get("dosage_form"):
            frappe.get_doc(dict(doctype="Dosage Form",dosage_form=args.get("dosage_form"))).insert()
        ####CLASSIFICATION
        if not frappe.get_value("Drug Classification",args.get("classification")) and args.get("classification"):
            frappe.get_doc(dict(doctype="Drug Classification",classification=args.get("classification"))).insert()
        ###UOM
        if not frappe.get_value("UOM",args.get("uom")) and args.get("uom"):
            frappe.get_doc(dict(doctype="UOM",uom_name=args.get("uom"))).insert()
        frappe.db.commit()
        # if len(args.get("classification")) > 139: continue
        ###Actual Drug now
        drug = frappe.get_value("Drug",dict(medicine_name=args.get("medicine_name")),'name')
        doc = None
        if drug:
            doc= frappe.get_doc("Drug",drug)
            doc.append("drug_stock_detail",dict(dosage_form=args.get("dosage_form"),ndc_code=args.get("ndc_code"),uom=args.get("uom"), strength=args.get("strength")))
            doc.save()
            continue 
        doc = frappe.get_doc(dict(doctype="Drug",medicine_name=args.get("medicine_name")))
        doc.append("drug_stock_detail",dict(dosage_form=args.get("dosage_form"),ndc_code=args.get("ndc_code"),uom=args.get("uom"), strength=args.get("strength")))
        # doc.append()
        doc.save()
        print(args)
        frappe.db.commit()
