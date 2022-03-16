# Copyright (c) 2022, Lonius Limited Innovation and contributors
# For license information, please see license.txt

import frappe,json
from frappe.model.document import Document

class Drug(Document):
	pass
@frappe.whitelist()
def drug_mapping(drug,strength=None):
	# return kwargs
	args = dict(parent=["LIKE",drug],strength=["LIKE",strength], item=["!=",""])
	if not strength: 
		args.pop("strength")
	# data = kwargs.pop("cmd")
	# return data
	return frappe.get_list("Drug Stock Detail", filters=args,fields=["*"])
