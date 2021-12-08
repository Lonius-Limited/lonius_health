import frappe
from frappe.model.rename_doc import rename_doc

@frappe.whitelist()
def create_lab_test(doc, handler=None):
    lab_tests = doc.lab_test_prescription
    if len(lab_tests) < 1:return
    patient = frappe.get_doc("Patient", doc.patient)
    for i in lab_tests:
        lab_test = frappe.get_doc({
                'doctype':"Lab Test",
                "status":"Draft",
                "patient": patient.name,
                "template": i.lab_test_name,
                "patient_sex": patient.sex
            })
        lab_test.run_method('set_missing_values')
        lab_test.insert()
    return 

def lab_test_template_price_exists(self):
    item_price = frappe.db.exists({'doctype': 'Item Price', 'item_code': self.item})
    if item_price:
        return item_price[0][0]
    return False

def lab_test_template_on_save(self):
    # If change_in_item update Item and Price List
    if self.change_in_item and self.is_billable and self.item:
        self.update_item()
        item_price = self.item_price_exists()
        if not item_price:
            if self.lab_test_rate and self.lab_test_rate > 0.0:
                price_list_name = frappe.db.get_value('Selling Settings', None, 'selling_price_list') or frappe.db.get_value('Price List', {'selling': 1})
                make_item_price(self.item, price_list_name, self.lab_test_rate)
        else:
            frappe.db.set_value('Item Price', item_price, 'price_list_rate', self.lab_test_rate)

        self.db_set('change_in_item', 0)

    elif not self.is_billable and self.item:
        frappe.db.set_value('Item', self.item, 'disabled', 1)

    #SYNCHRONIZE ITEM AND LAB IF THERE IS A NAMING SERIES FOR ITEMS. ITEM CODE AND LAB TEMPLATE CODE HAVE TO BE THE SAME
    if frappe.db.exists({'doctype': 'Item', 'item_code': self.lab_test_code}):
        rename_doc('Item', self.lab_test_code, self.name, ignore_permissions=True)
        frappe.db.set_value('Item', self.lab_test_code, 'item_name', self.lab_test_name)
    else:
        rename_doc('Item', self.item, self.name, ignore_permissions=True)
        frappe.db.set_value('Item', self.name, 'item_name', self.lab_test_name)
    self.reload()

def make_item_price(item, price_list_name, item_price):
	frappe.get_doc({
		'doctype': 'Item Price',
		'price_list': price_list_name,
		'item_code': item,
		'price_list_rate': item_price
	}).insert(ignore_permissions=True, ignore_mandatory=True)