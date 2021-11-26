

frappe.pages['pharmacy-page'].on_page_load = function (wrapper) {
	new MyPage(wrapper);
}
MyPage = Class.extend({
	init: function (wrapper) {
		
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Pharmacy Page',
			single_column: false
		});
		// let me =$(this)
		
		this.parent = wrapper
		this.page = this.parent.page
		this.page.set_indicator('Incoming Prescriptions(2)', 'green')
		this.page.sidebar.html(`<ul class="standard-sidebar leaderboard-sidebar overlay-sidebar"></ul>`);
		this.$sidebar_list = this.page.sidebar.find('ul');
		this.make();


	},
	make: function () {
		let me = $(this)
		// import "frappe-datatable/dist/frappe-datatable.min.css";
		// let DataTable =  import DataTable from "frappe-datatable"
		this.encounters = ["Salim Omar", "Aileen Mohammed"]

		// this.$container = $(frappe.pharmacy_page_body.body).appendTo(this.page.main)
		$(frappe.render_template(frappe.pharmacy_page_body.body, this)).appendTo(this.page.main)
		
		this.encounters.map(e => {
			const icon = 'users';
			this.get_sidebar_item(e, icon).appendTo(this.$sidebar_list);
		});

		this.setupFields()

	},
	// 192.81.130.56
	setupFields() {




		this.actions_button = this.page.add_action_item('Dispense Prescription', () => dispenseDrugs())

		this.actions_button = this.page.add_action_item('Raise Bill', () => raiseBill())

		this.warehouse_select = this.page.add_inner_button('RMBH Pharmacy', () => new_post(), 'Select Warehouse')
		this.prescription_history = this.page.add_inner_button('Show Prescription History', () => showPrescriptionHistory())

		this.add_prescription = this.page.add_inner_button('Add Prescription', () => addPrescription())

		

	

		this.company_select = this.page.add_field({
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			read_only: 1,
			default: frappe.defaults.get_default("company"),
			reqd: 1,
			change: (e) => {
				if (e) {

					this.options.selected_company = e.currentTarget.value;
					frappe.msgprint(this.options.selected_company)
					// this.make_request();
				}
			}
		});
		this.company_select = this.page.add_field({
			fieldname: "patient",
			label: __("Prescription Search"),
			fieldtype: "Link",
			options: "Patient",
			// default: frappe.defaults.get_default("company"),
			reqd: 0,
			change: (e) => {
				if (!e) {
					return
				}
				this.options.selected_patient = e.currentTarget.value;
				frappe.msgprint(this.options.selected_patient)
				// this.make_request();
			}
		});
		

	},

	populateEncounters() {
		this.encounters = ["Salim Omar", "Aileen Mohammed"]

		// frappe.call({method: "lonius_health.api.patients.get_pending_encounter_prescriptions"}).then(payload => {
		// 	this.payload = payload
		// 	for (let patient in this.payload) {
		// 		encounters.push(patient.patient_name)
		// 	}
		// })
		this.make()
	},
	get_sidebar_item(item, icon) {
		let icon_html = icon ? frappe.utils.icon(icon, 'md') : '';
		return $(`<li class="standard-sidebar-item">
			<span>${icon_html}</span>
			<a class="sidebar-link">
				<span class="doctype-text" doctype-value="${item}">${__(item)}</span>
			</a>
		</li>`);
	},



})
/* let body = `<div class="leaderboard page-main-content">

<div id="datatable" class="page-main-content"><h1>FFF</h1></div>
</div>`;*/

let body =`
<div class="point-of-sale-app"><section class="items-selector">
				<div class="filter-section">
					<div class="label">All Items</div>
					<div class="search-field" title="Ctrl+I"><div class="frappe-control input-max-width" data-fieldtype="Data">				<div class="form-group">					<div class="clearfix">						<label class="control-label hide" style="padding-right: 0px;">Search</label>					</div>					<div class="control-input-wrapper">						<div class="control-input"><input type="text" autocomplete="off" class="input-with-feedback form-control" maxlength="140" data-fieldtype="Data" placeholder="Search by item code, serial number or barcode"></div>						<div class="control-value like-disabled-input" style="display: none;">null</div>						<p class="help-box small text-muted"></p>					</div>				</div>			</div></div>
					<div class="item-group-field" title="Ctrl+G"><div class="frappe-control input-max-width" data-fieldtype="Link">				<div class="form-group">					<div class="clearfix">						<label class="control-label hide" style="padding-right: 0px;">Item Group</label>					</div>					<div class="control-input-wrapper">						<div class="control-input"><div class="link-field ui-front" style="position: relative;">
			<div class="awesomplete"><input type="text" class="input-with-feedback form-control" maxlength="140" data-fieldtype="Link" placeholder="Select item group" data-target="Item Group" autocomplete="off" aria-expanded="false" aria-owns="awesomplete_list_2" role="combobox"><ul hidden="" role="listbox" id="awesomplete_list_2"></ul><span class="visually-hidden" role="status" aria-live="assertive" aria-atomic="true">Begin typing for results.</span></div>
			<span class="link-btn">
				<a class="btn-open no-decoration" title="Open Link">
					<svg class="icon  icon-xs" style="">
			<use class="" href="#icon-arrow-right"></use>
		</svg>
				</a>
			</span>
		</div></div>						<div class="control-value like-disabled-input" style="display: none;"></div>						<p class="help-box small text-muted"></p>					</div>				</div>			</div></div>
				</div>
				<div class="items-container"><div class="item-wrapper" data-item-code="ABC" data-serial-no="undefined" data-batch-no="undefined" data-uom="Nos" data-rate="20" title="Paracetamol 500MG">

				<div class="item-qty-pill">
							<span class="indicator-pill whitespace-nowrap green">200</span>
						</div>
						<div class="item-display abbr">P5</div>

				<div class="item-detail">
					<div class="item-name">
						Paracetamol 500MG
					</div>
					<div class="item-rate">Sh 20</div>
				</div>
			</div></div>
			</section><section class="item-details-container"><div class="item-details-header">
				<div class="label">Item Details</div>
				<div class="close-btn" title="Esc">
					<svg width="32" height="32" viewBox="0 0 14 14" fill="none">
						<path d="M4.93764 4.93759L7.00003 6.99998M9.06243 9.06238L7.00003 6.99998M7.00003 6.99998L4.93764 9.06238L9.06243 4.93759" stroke="#8D99A6"></path>
					</svg>
				</div>
			</div>
			<div class="item-display">
				<div class="item-name-desc-price">
					<div class="item-name"></div>
					<div class="item-desc"></div>
					<div class="item-price"></div>
				</div>
				<div class="item-image"></div>
			</div>
			<div class="discount-section"></div>
			<div class="form-container"></div></section><section class="customer-cart-container" style="display: flex;"><div class="customer-section">
			<div class="customer-field"><div class="frappe-control input-max-width" data-fieldtype="Link">				<div class="form-group">					<div class="clearfix">						<label class="control-label hide" style="padding-right: 0px;">Customer</label>					</div>					<div class="control-input-wrapper">						<div class="control-input"><div class="link-field ui-front" style="position: relative;">
			<div class="awesomplete"><input type="text" class="input-with-feedback form-control" maxlength="140" data-fieldtype="Link" placeholder="Search by customer name, phone, email." data-target="Customer" autocomplete="off" aria-expanded="false" aria-owns="awesomplete_list_35" role="combobox" aria-activedescendant="awesomplete_list_35_item_0"><ul role="listbox" id="awesomplete_list_35" hidden=""><li aria-selected="true"><a><p title="Walk In"><strong>Walk In</strong><br><span class="small">All Customer Groups, All Territories</span></p></a></li><li><a><p title="Create a new Customer"><span class="text-primary link-option"><i class="fa fa-plus" style="margin-right: 5px;"></i> Create a new Customer</span></p></a></li><li><a><p title="Advanced Search"><span class="text-primary link-option"><i class="fa fa-search" style="margin-right: 5px;"></i> Advanced Search</span></p></a></li></ul><span class="visually-hidden" role="status" aria-live="assertive" aria-atomic="true" hidden="">3 results found</span></div>
			<span class="link-btn" style="display: none;">
				<a class="btn-open no-decoration" title="Open Link">
					<svg class="icon  icon-xs" style="">
			<use class="" href="#icon-arrow-right"></use>
		</svg>
				</a>
			</span>
		</div></div>						<div class="control-value like-disabled-input" style="display: none;"></div>						<p class="help-box small text-muted"></p>					</div>				</div>			</div></div>
		</div><div class="cart-container">
				<div class="abs-cart-container">
					<div class="cart-label">Item Cart</div>
					<div class="cart-header" style="display: none;">
						<div class="name-header">Item</div>
						<div class="qty-header">Qty</div>
						<div class="rate-amount-header">Amount</div>
					</div>
					<div class="cart-items-section"><div class="no-item-wrapper">No items in cart</div></div>
					<div class="cart-totals-section"><div class="add-discount-wrapper" title="Ctrl+D" style="display: none;">
				<svg class="discount-icon" width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M19 15.6213C19 15.2235 19.158 14.842 19.4393 14.5607L20.9393 13.0607C21.5251 12.4749 21.5251 11.5251 20.9393 10.9393L19.4393 9.43934C19.158 9.15804 19 8.7765 19 8.37868V6.5C19 5.67157 18.3284 5 17.5 5H15.6213C15.2235 5 14.842 4.84196 14.5607 4.56066L13.0607 3.06066C12.4749 2.47487 11.5251 2.47487 10.9393 3.06066L9.43934 4.56066C9.15804 4.84196 8.7765 5 8.37868 5H6.5C5.67157 5 5 5.67157 5 6.5V8.37868C5 8.7765 4.84196 9.15804 4.56066 9.43934L3.06066 10.9393C2.47487 11.5251 2.47487 12.4749 3.06066 13.0607L4.56066 14.5607C4.84196 14.842 5 15.2235 5 15.6213V17.5C5 18.3284 5.67157 19 6.5 19H8.37868C8.7765 19 9.15804 19.158 9.43934 19.4393L10.9393 20.9393C11.5251 21.5251 12.4749 21.5251 13.0607 20.9393L14.5607 19.4393C14.842 19.158 15.2235 19 15.6213 19H17.5C18.3284 19 19 18.3284 19 17.5V15.6213Z" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path>
				<path d="M15 9L9 15" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path>
				<path d="M10.5 9.5C10.5 10.0523 10.0523 10.5 9.5 10.5C8.94772 10.5 8.5 10.0523 8.5 9.5C8.5 8.94772 8.94772 8.5 9.5 8.5C10.0523 8.5 10.5 8.94772 10.5 9.5Z" fill="white" stroke-linecap="round" stroke-linejoin="round"></path>
				<path d="M15.5 14.5C15.5 15.0523 15.0523 15.5 14.5 15.5C13.9477 15.5 13.5 15.0523 13.5 14.5C13.5 13.9477 13.9477 13.5 14.5 13.5C15.0523 13.5 15.5 13.9477 15.5 14.5Z" fill="white" stroke-linecap="round" stroke-linejoin="round"></path>
			</svg> Add Discount
			</div>
			<div class="net-total-container"><div>Net Total</div><div>Sh 0.00</div></div>
			<div class="taxes-container" style="display: none;"></div>
			<div class="grand-total-container"><div>Grand Total</div><div>Sh 0.00</div></div>
			<div class="checkout-btn" title="Ctrl+Enter" style="background-color: var(--blue-200); display: flex;">Checkout</div>
			<div class="edit-cart-btn" title="Ctrl+E" style="display: none;">Edit Cart</div></div>
					<div class="numpad-section"><div class="numpad-totals">
				<span class="numpad-net-total"><div>Net Total: <span>Sh 0.00</span></div></span>
				<span class="numpad-grand-total"><div>Grand Total: <span>Sh 0.00</span></div></span>
			</div><div class="numpad-container">
				<div class="numpad-btn " data-button-value="1">1</div><div class="numpad-btn " data-button-value="2">2</div><div class="numpad-btn " data-button-value="3">3</div><div class="numpad-btn col-span-2" data-button-value="qty" title="Ctrl+Q">Quantity</div><div class="numpad-btn " data-button-value="4">4</div><div class="numpad-btn " data-button-value="5">5</div><div class="numpad-btn " data-button-value="6">6</div><div class="numpad-btn col-span-2" data-button-value="discount_percentage" title="Ctrl+D">Discount</div><div class="numpad-btn " data-button-value="7">7</div><div class="numpad-btn " data-button-value="8">8</div><div class="numpad-btn " data-button-value="9">9</div><div class="numpad-btn col-span-2" data-button-value="rate" title="Ctrl+R">Rate</div><div class="numpad-btn " data-button-value="." title="Ctrl+>">.</div><div class="numpad-btn " data-button-value="0">0</div><div class="numpad-btn " data-button-value="delete" title="Ctrl+Backspace">Delete</div><div class="numpad-btn col-span-2 remove-btn" data-button-value="remove" title="Shift+Ctrl+Backspace">Remove</div>
			</div><div class="numpad-btn checkout-btn" data-button-value="checkout" title="Ctrl+Enter" style="background-color: var(--blue-200);">Checkout</div></div>
				</div>
			</div></section><section class="payment-container">
				<div class="section-label payment-section">Payment Method</div>
				<div class="payment-modes"></div>
				<div class="fields-numpad-container">
					<div class="fields-section">
						<div class="section-label">Additional Information</div>
						<div class="invoice-fields"></div>
					</div>
					<div class="number-pad"><div class="numpad-container">
				<div class="numpad-btn " data-button-value="1">1</div><div class="numpad-btn " data-button-value="2">2</div><div class="numpad-btn " data-button-value="3">3</div><div class="numpad-btn " data-button-value="4">4</div><div class="numpad-btn " data-button-value="5">5</div><div class="numpad-btn " data-button-value="6">6</div><div class="numpad-btn " data-button-value="7">7</div><div class="numpad-btn " data-button-value="8">8</div><div class="numpad-btn " data-button-value="9">9</div><div class="numpad-btn " data-button-value=".">.</div><div class="numpad-btn " data-button-value="0">0</div><div class="numpad-btn " data-button-value="delete">Delete</div>
			</div></div>
				</div>
				<div class="totals-section">
					<div class="totals"></div>
				</div>
				<div class="submit-order-btn" title="Ctrl+Enter">Complete Order</div>
			</section><section class="past-order-list">
				<div class="filter-section">
					<div class="label">Recent Orders</div>
					<div class="search-field"><div class="frappe-control input-max-width" data-fieldtype="Data">				<div class="form-group">					<div class="clearfix">						<label class="control-label hide" style="padding-right: 0px;">Search</label>					</div>					<div class="control-input-wrapper">						<div class="control-input"><input type="text" autocomplete="off" class="input-with-feedback form-control" maxlength="140" data-fieldtype="Data" placeholder="Search by invoice id or customer name"></div>						<div class="control-value like-disabled-input" style="display: none;">null</div>						<p class="help-box small text-muted"></p>					</div>				</div>			</div></div>
					<div class="status-field"><div class="frappe-control input-max-width" data-fieldtype="Select">				<div class="form-group">					<div class="clearfix">						<label class="control-label hide" style="padding-right: 0px;">Invoice Status</label>					</div>					<div class="control-input-wrapper">						<div class="control-input flex align-center"><select type="text" autocomplete="off" class="input-with-feedback form-control ellipsis" maxlength="140" data-fieldtype="Select" placeholder="Filter by invoice status"><option value="Draft">Draft</option><option value="Paid">Paid</option><option value="Consolidated">Consolidated</option><option value="Return">Return</option></select><div class="select-icon ">
				<svg class="icon  icon-sm" style="">
			<use class="" href="#icon-select"></use>
		</svg>
			</div><div class="placeholder ellipsis text-extra-muted " style="display: none;">
				<span>Filter by invoice status</span>
			</div></div>						<div class="control-value like-disabled-input" style="display: none;">Draft</div>						<p class="help-box small text-muted"></p>					</div>				</div>			</div></div>
				</div>
				<div class="invoices-container"></div>
			</section><section class="past-order-summary">
				<div class="no-summary-placeholder">
					Select an invoice to load summary data
				</div>
				<div class="invoice-summary-wrapper">
					<div class="abs-container">
						<div class="upper-section"></div>
						<div class="label">Items</div>
						<div class="items-container summary-container"></div>
						<div class="label">Totals</div>
						<div class="totals-container summary-container"></div>
						<div class="label">Payments</div>
						<div class="payments-container summary-container"></div>
						<div class="summary-btns"></div>
					</div>
				</div>
			</section></div>
`
frappe.pharmacy_page_body = {
	body: body,
	columns: ["Item", "Qty","Rate","Amount"],
	data:["Bacitracin", 1, 10, 10]
}
