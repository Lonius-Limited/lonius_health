# Copyright (c) 2021, Lonius Limited Innovation and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry


class PharmacyPrescription(Document):
    def dispense_prescription(self):
        # pass
        self.compute_totals()
        self.validate_prescription_expiry()
        self.validate_drug_availability()
        self.post_invoice()

    def compute_totals(self):
        total = 0.0
        for item in self.get("prescription_items"):
            amount = item.get("qty") * item.get("rate")
            total = total + amount
        self.set('total_invoice_amount', total)

    def validate_prescription_expiry(self):
        for item in self.get("prescription_items"):
            if item.get("qty") > item.get("maximum_prescription_quantity"):
                default_uom = frappe.get_value(
                    "Item", item.get("drug_code"), 'stock_uom')
                frappe.throw("<p>{0} has exceeded maximum prescription of {1} {2}. Please rectify this.</p><p>If you need to dispense a new prescription, please submit a new encounter.</p>".format(
                    item.get("drug_name"), item.get("maximum_prescription_quantity"), default_uom))

    def validate_drug_availability(self):
        warehouse = self.get("pharmacy")
        for item in self.get("prescription_items"):
            ordered_qty = item.get("qty")
            item_code = item.get("drug_code")
            available_stock = get_stock_availability(
                item_code, warehouse) or 0.0
            if ordered_qty > available_stock:
                frappe.throw("There is no sufficient stock to dispense this prescription for {0}. Available balance {1} ".format(
                    item.get("drug_name"), available_stock))

    def post_invoice(self):
        items = self.get_invoice_items(self.get("prescription_items"))
        from lonius_health.api.invoices import make_invoice_endpoint
        make_invoice_endpoint(patient=self.get('patient'),
                              customer=self.get("customer"), items=items)
        self.dispense_stock(invoice)
        self.set('status', 'Prescription Serviced')
        self.save()
        return self

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

    def dispense_stock(self,invoice):
        for x in self.get("prescription"):
            item, item_group = x.get("drug_code"), frappe.get_value(
                "Item", x.get("drug_code"), 'item_group')
            uom = frappe.get_value("Item", x.get("drug_code"), 'stock_uom')
            income_account = frappe.get_value("Item Default", dict(parent=item), 'income_account') or frappe.get_value(
                "Item Default", dict(parent=item_group), 'income_account')
            company = frappe.defaults.get_user_default("company")
            row = dict(company=company,item_code=item, uom=uom,
                       income_account=income_account, qty=x.get("qty"), rate=x.get("rate"), conversion_factor=1, from_warehouse=self.get("pharmacy"), sales_invoice=invoice.get("name"))
