import frappe
from frappe.model.rename_doc import rename_doc

@frappe.whitelist()
def create_procedure(doc, handler=None):
	procedure_list = doc.procedure_prescription
	if len(procedure_list) < 1:return
	patient = frappe.get_doc("Patient", doc.patient)
	for i in procedure_list:
		procedure = frappe.get_doc({
				'doctype':"Clinical Procedure",
				"status":"Draft",
				"patient": patient.name,
				"procedure_template": i.procedure_name
		})
		procedure.run_method('set_missing_values')
		procedure.insert()
	return

def procedure_template_after_insert(self):
	create_item_from_template(self)

def create_item_from_template(doc):
	disabled = doc.disabled
	if doc.is_billable and not doc.disabled:
		disabled = 0

	uom = frappe.db.exists('UOM', 'Unit') or frappe.db.get_single_value('Stock Settings', 'stock_uom')
	item = frappe.get_doc({
		'doctype': 'Item',
		'item_code': doc.template,
		'item_name':doc.template,
		'item_group': doc.item_group,
		'description':doc.description,
		'is_sales_item': 1,
		'is_service_item': 1,
		'is_purchase_item': 0,
		'is_stock_item': 0,
		'show_in_website': 0,
		'is_pro_applicable': 0,
		'disabled': disabled,
		'stock_uom': uom
	}).insert(ignore_permissions=True, ignore_mandatory=True)

	make_item_price(item.name, doc.rate)
	doc.db_set('item_code', item.name)
	doc.db_set('item', item.name)

def make_item_price(item, item_price):
	price_list_name = frappe.db.get_value('Price List', {'selling': 1})
	frappe.get_doc({
		'doctype': 'Item Price',
		'price_list': price_list_name,
		'item_code': item,
		'price_list_rate': item_price
	}).insert(ignore_permissions=True, ignore_mandatory=True)