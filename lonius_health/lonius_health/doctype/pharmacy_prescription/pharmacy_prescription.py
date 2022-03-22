# Copyright (c) 2021, Lonius Limited Innovation and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpnext.stock.get_item_details import get_item_details, get_valuation_rate
from lonius_health.api.patients import get_prescription_qty


class PharmacyPrescription(Document):
	def before_submit(self):
		self.refresh_prices()
		self.dispense_prescription()

	def dispense_prescription(self):
		# pass
		self.compute_totals()
		self.validate_prescription_expiry()
		self.validate_drug_availability()
		invoice = self.post_invoice()
		self.dispense_stock(invoice)

	def before_save(self):
		self.refresh_prices()

	def refresh_prices(self):
		for row in self.get("prescription_items"):
			kwargs = {
				"patient": self.get("patient"),
				"customer": self.get("customer"),
				"warehouse": self.get("pharmacy"),
				"drug": row.drug_code,
				"dosage": row.dosage,
				"period": row.period,
				"interval": row.interval or 1
			}
			res = get_prescription_qty(**kwargs)
			if row.qty == 0: row.qty = res[0] or 0
			row.rate = res[1] or 0
			row.amount = row.rate * row.qty
			row.in_stock = res[2].get('actual_qty')
			row.unit_of_measure = res[2].get('uom')
		self.compute_totals()
		# frappe.msgprint("{}".format(res))

	def compute_totals(self):
		total = 0.0
		for item in self.get("prescription_items"):
			amount = item.get("qty") * item.get("rate")
			total = total + amount
		self.set('total_invoice_amount', total)

	def validate_prescription_expiry(self):
		if not self.encounter:
			return
		for item in self.get("prescription_items"):
			if item.get("qty") > item.get("maximum_prescription_quantity"):
				default_uom = frappe.get_value(
					"Item", item.get("drug_code"), 'stock_uom')
				frappe.throw("<p>{0} has exceeded maximum prescription of {1} {2}. Please rectify this.</p><p>If you need to dispense a new prescription, please submit a new document.</p>".format(
					item.get("drug_name"), item.get("maximum_prescription_quantity"), default_uom))

	def validate_drug_availability(self):
		warehouse = self.get("pharmacy")
		for item in self.get("prescription_items"):
			if not frappe.get_value("Item", item.get("drug_code"), "is_stock_item"):
				continue
			ordered_qty = item.get("qty")
			item_code = item.get("drug_code")
			available_stock = get_stock_availability(
				item_code, warehouse) or 0.0
			if isinstance(available_stock, tuple):
				available_stock = available_stock[0] or 0.0
			if ordered_qty > available_stock:
				frappe.throw("There is no sufficient stock to dispense this prescription for {0}. Available balance in {1} is {2}".format(
					item.get("drug_name"), warehouse, available_stock))

	def post_invoice(self):
		items = self.get_invoice_items(self.get("prescription_items"))
		from lonius_health.api.invoices import make_invoice_endpoint
		invoice = make_invoice_endpoint(patient=self.get('patient'),
										customer=self.get("customer"), items=items)
		self.set('status', 'Prescription Serviced')
		# self.save()
		return invoice

	def get_invoice_items(self, prescription):
		to_return = []
		for x in prescription:
			item, item_group = x.get("drug_code"), frappe.get_value(
				"Item", x.get("drug_code"), 'item_group')
			uom = frappe.get_value("Item", x.get("drug_code"), 'stock_uom')
			income_account = frappe.get_value("Item Default", dict(parent=item), 'income_account') or frappe.get_value(
				"Item Default", dict(parent=item_group), 'income_account')
			if not income_account:
				frappe.throw(f"Sorry, revenue account for {item} is not set.")
			row = dict(item_code=item, item_name=x.get("drug_name"), description=x.get("drug_name"), uom=uom,
					   income_account=income_account, qty=x.get("qty"), rate=x.get("rate"), conversion_factor=1)
			to_return.append(row)

		return to_return

	def dispense_stock(self, invoice):
		for x in self.get("prescription_items"):
			if not frappe.get_value("Item", x.get("drug_code"), "is_stock_item"):
				continue
			item, item_group = x.get("drug_code"), frappe.get_value(
				"Item", x.get("drug_code"), 'item_group')
			expense_account = frappe.get_value("Item Default", dict(parent=item), 'expense_account') or frappe.get_value(
				"Item Default", dict(parent=item_group), 'expense_account')
			company = frappe.defaults.get_user_default("company")
			valuation_rate = self.get_valuation_rate(
				item, company, self.get("pharmacy"))
			row = dict(company=company, item_code=item,
					   expense_account=expense_account, qty=x.get("qty"),
					   rate=valuation_rate, conversion_factor=1, from_warehouse=self.get("pharmacy"), sales_invoice_no=invoice.get("name"))
			make_stock_entry(**frappe._dict(row))

	def get_valuation_rate(self, item, warehouse, company):
		return get_valuation_rate(item, company, warehouse=warehouse).get("valuation_rate") or 0.0
# import icd10
# icd10.codes
