

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
    this.page.set_indicator('No Selected Pharmacy', 'green')
    this.page.sidebar.html(`<ul class="standard-sidebar leaderboard-sidebar overlay-sidebar"></ul>`);
    this.$sidebar_list = this.page.sidebar.find('ul');
    this.patientPrescription = []
    this.session_warehouse = null
    this.setAllocatedPharmacies()

    this.make();


  },
  make: function () {
    let me = $(this)

    this.renderPatientPrescription()

    this.setupFields()

    this.$container = $(frappe.render_template(frappe.pharmacy_page_body.body, this)).appendTo(this.page.main)




  },
  // 192.81.130.56
  setAllocatedPharmacies() {
    frappe.call({
      method: "lonius_health.api.patients.get_allocated_warehouses"
    }).then(r => {
      this.allocated_warehouses = r.message || []
      if (!this.allocated_warehouses) {
        frappe.throw("Sorry no Pharmacy(ies) havebeen assigned to you for purposes of Billing")
      }

      let selectedWarehouse = r.message[0]
      this.warehouse_select = this.page.add_select(__("Pharmacy"),
        this.allocated_warehouses.map(d => {
          return { "warehouse": __(frappe.model.unscrub(d)), value: d };
        })
      );
      //First  Warehouse is Default

      this.page.set_indicator(selectedWarehouse, 'green')
      this.session_warehouse = selectedWarehouse
      //Get Encounters now
      this.populateEncounters()
      //Event
      this.warehouse_select.on("change", (e) => {
        this.session_warehouse = e.currentTarget.value;
        this.page.set_indicator(this.session_warehouse, 'green')
        this.populateEncounters()
      });
    })


  },
  setupFields() {




    this.actions_button = this.page.add_action_item('Dispense Prescription', () => this.dispenseDrugs())

    this.actions_button = this.page.add_action_item('Raise Bill', () => this.raiseBill())

    // this.warehouse_select = this.page.add_inner_button('RMBH Pharmacy', () => this.setPharmacy(), 'Select Warehouse')
    this.prescription_history = this.page.add_inner_button('Show Prescription History', () => showPrescriptionHistory())

    this.add_prescription = this.page.add_inner_button('Add Prescription', () => this.addPrescription())





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
    this.patient_select = this.page.add_field({
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
    this.encounters = []

    let selectedWarehouse = this.session_warehouse
    if (!selectedWarehouse) {
      frappe.throw("Warehouse not assigned", "Please Request for Warehouse(Pharmacy) Permissions for Sales Invoice")
    }
    let payload = []
    frappe.call({
      method: "lonius_health.api.patients.get_pending_encounter_prescriptions",
      args: {
        warehouse: selectedWarehouse
      }
    }).then(r => {
      payload = r.message
      console.log(r)
      this.encounters = payload
      this.encounters.map(e => {
        const icon = 'users';
        this.get_sidebar_item(e.patient_name || e.patient, icon).appendTo(this.$sidebar_list);
      })
    })


  },
  get_sidebar_item(item, icon) {
    let icon_html = icon ? frappe.utils.icon(icon, 'md') : '';
    return $(`<li class="standard-sidebar-item" >
			<span>${icon_html}</span>
			<a class="sidebar-link">
				<span class="doctype-text" doctype-value="${item}">${__(item)}</span>
			</a>
		</li>`);
  },
  get_item_cart_section(prescription) {
    return prescription.map(row => {
      let amount = row.rate * row.qty
      return `
    <div class="cart-item-wrapper" data-row-name="new-pos-invoice-item-2" style="background-color: var(--gray-50);">
      <div class="item-image item-abbr">P5</div>
      <div class="item-name-desc">
        <div class="item-name"> ${row.drug_code} </div>
        <div class="item-desc">${row.drug_name}</div>
      </div>
      <div class="item-qty-rate">
        <div class="item-qty">
          <span>${row.qty}</span>
        </div>
        <div class="item-rate-amount" style="width: 64px;">
          <div class="item-rate">${row.rate}</div>
          <div class="item-amount">${amount}</div>
        </div>
      </div>
    </div>
    <div class="seperator"></div>`})

  },

  actionPayload() {
    this.actionPayload = {}
  },
  renderPatientPrescription() {

    this.actionPayload = {}

    this.$sidebar_list.on("click", "li", (e) => {

      let $li = $(e.currentTarget);

      let patient = $li.find(".doctype-text").attr("doctype-value");

      this.patientPrescription = this.encounters.filter(function (el) {
        return el.patient_name == patient

      });


      this.context = this.get_item_cart_section(this.patientPrescription[0].prescription)

      this.cart_area = this.$container.find(".cart-items-section").html(this.context);;

      // this.$container 
      // frappe.msgprint()

      // console.log(JSON.stringify(this.patientPrescription))

      // this.options.selected_company = frappe.defaults.get_default("company");
      // this.options.selected_doctype = doctype;
      // this.options.selected_filter = this.filters[doctype];
      // this.options.selected_filter_item = this.filters[doctype][0];

      // this.type_select.empty().add_options(
      // 	this.options.selected_filter.map(d => {
      // 		return {"label": __(frappe.model.unscrub(d)), value: d };
      // 	})
      // );
      // if (this.leaderboard_config[this.options.selected_doctype].company_disabled) {
      // 	$(this.parent).find("[data-original-title=Company]").hide();
      // } else {
      // 	$(this.parent).find("[data-original-title=Company]").show();
      // }

      this.$sidebar_list.find("li").removeClass("active selected");
      $li.addClass("active selected");

      // frappe.set_route("pharmacy_page", this.options.selected_doctype);
      // this.make_request();
    });
  }

})
/* let body = `<div class="leaderboard page-main-content">

<div id="datatable" class="page-main-content"><h1>FFF</h1></div>
</div>`;*/

let body = `
<div class="point-of-sale-app">
<section class ="items-selector">
</section>

<section class="item-details-container">
    <div class="item-details-header">
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
    <div class="form-container"></div>
  </section>
  <section class="customer-cart-container" style="display: flex;">
    
    <div class="cart-container">
      <div class="abs-cart-container">
        <div class="cart-label">Item Cart</div>
        <div class="cart-header" style="display: none;">
          <div class="name-header">Item</div>
          <div class="qty-header">Qty</div>
          <div class="rate-amount-header">Amount</div>
        </div>
        <div class="cart-items-section">
          <div class="no-item-wrapper">No items in cart</div>
        </div>
        <div class="cart-totals-section">
          <div class="add-discount-wrapper" title="Ctrl+D" style="display: none;">
            <svg class="discount-icon" width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 15.6213C19 15.2235 19.158 14.842 19.4393 14.5607L20.9393 13.0607C21.5251 12.4749 21.5251 11.5251 20.9393 10.9393L19.4393 9.43934C19.158 9.15804 19 8.7765 19 8.37868V6.5C19 5.67157 18.3284 5 17.5 5H15.6213C15.2235 5 14.842 4.84196 14.5607 4.56066L13.0607 3.06066C12.4749 2.47487 11.5251 2.47487 10.9393 3.06066L9.43934 4.56066C9.15804 4.84196 8.7765 5 8.37868 5H6.5C5.67157 5 5 5.67157 5 6.5V8.37868C5 8.7765 4.84196 9.15804 4.56066 9.43934L3.06066 10.9393C2.47487 11.5251 2.47487 12.4749 3.06066 13.0607L4.56066 14.5607C4.84196 14.842 5 15.2235 5 15.6213V17.5C5 18.3284 5.67157 19 6.5 19H8.37868C8.7765 19 9.15804 19.158 9.43934 19.4393L10.9393 20.9393C11.5251 21.5251 12.4749 21.5251 13.0607 20.9393L14.5607 19.4393C14.842 19.158 15.2235 19 15.6213 19H17.5C18.3284 19 19 18.3284 19 17.5V15.6213Z" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M15 9L9 15" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M10.5 9.5C10.5 10.0523 10.0523 10.5 9.5 10.5C8.94772 10.5 8.5 10.0523 8.5 9.5C8.5 8.94772 8.94772 8.5 9.5 8.5C10.0523 8.5 10.5 8.94772 10.5 9.5Z" fill="white" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M15.5 14.5C15.5 15.0523 15.0523 15.5 14.5 15.5C13.9477 15.5 13.5 15.0523 13.5 14.5C13.5 13.9477 13.9477 13.5 14.5 13.5C15.0523 13.5 15.5 13.9477 15.5 14.5Z" fill="white" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg> Add Discount
          </div>
          <div class="net-total-container">
            <div>Net Total</div>
            <div>Sh 0.00</div>
          </div>
          <div class="taxes-container" style="display: none;"></div>
          <div class="grand-total-container">
            <div>Grand Total</div>
            <div>Sh 0.00</div>
          </div>
          <div class="checkout-btn" title="Ctrl+Enter" style="background-color: var(--blue-200); display: flex;">Checkout</div>
          <div class="edit-cart-btn" title="Ctrl+E" style="display: none;">Edit Cart</div>
        </div>
        <div class="numpad-section">
          <div class="numpad-totals">
            <span class="numpad-net-total">
              <div>Net Total: <span>Sh 0.00</span>
              </div>
            </span>
            <span class="numpad-grand-total">
              <div>Grand Total: <span>Sh 0.00</span>
              </div>
            </span>
          </div>
          <div class="numpad-container">
            <div class="numpad-btn " data-button-value="1">1</div>
            <div class="numpad-btn " data-button-value="2">2</div>
            <div class="numpad-btn " data-button-value="3">3</div>
            <div class="numpad-btn col-span-2" data-button-value="qty" title="Ctrl+Q">Quantity</div>
            <div class="numpad-btn " data-button-value="4">4</div>
            <div class="numpad-btn " data-button-value="5">5</div>
            <div class="numpad-btn " data-button-value="6">6</div>
            <div class="numpad-btn col-span-2" data-button-value="discount_percentage" title="Ctrl+D">Discount</div>
            <div class="numpad-btn " data-button-value="7">7</div>
            <div class="numpad-btn " data-button-value="8">8</div>
            <div class="numpad-btn " data-button-value="9">9</div>
            <div class="numpad-btn col-span-2" data-button-value="rate" title="Ctrl+R">Rate</div>
            <div class="numpad-btn " data-button-value="." title="Ctrl+>">.</div>
            <div class="numpad-btn " data-button-value="0">0</div>
            <div class="numpad-btn " data-button-value="delete" title="Ctrl+Backspace">Delete</div>
            <div class="numpad-btn col-span-2 remove-btn" data-button-value="remove" title="Shift+Ctrl+Backspace">Remove</div>
          </div>
          <div class="numpad-btn checkout-btn" data-button-value="checkout" title="Ctrl+Enter" style="background-color: var(--blue-200);">Checkout</div>
        </div>
      </div>
    </div>
  </section>
  <section class="payment-container">
    <div class="section-label payment-section">Payment Method</div>
    <div class="payment-modes"></div>
    <div class="fields-numpad-container">
      <div class="fields-section">
        <div class="section-label">Additional Information</div>
        <div class="invoice-fields"></div>
      </div>
      <div class="number-pad">
        <div class="numpad-container">
          <div class="numpad-btn " data-button-value="1">1</div>
          <div class="numpad-btn " data-button-value="2">2</div>
          <div class="numpad-btn " data-button-value="3">3</div>
          <div class="numpad-btn " data-button-value="4">4</div>
          <div class="numpad-btn " data-button-value="5">5</div>
          <div class="numpad-btn " data-button-value="6">6</div>
          <div class="numpad-btn " data-button-value="7">7</div>
          <div class="numpad-btn " data-button-value="8">8</div>
          <div class="numpad-btn " data-button-value="9">9</div>
          <div class="numpad-btn " data-button-value=".">.</div>
          <div class="numpad-btn " data-button-value="0">0</div>
          <div class="numpad-btn " data-button-value="delete">Delete</div>
        </div>
      </div>
    </div>
    <div class="totals-section">
      <div class="totals"></div>
    </div>
    <div class="submit-order-btn" title="Ctrl+Enter">Complete Order</div>
  </section>
  <section class="past-order-list">
    <div class="filter-section">
      <div class="label">Recent Orders</div>
      <div class="search-field">
        <div class="frappe-control input-max-width" data-fieldtype="Data">
          <div class="form-group">
            <div class="clearfix">
              <label class="control-label hide" style="padding-right: 0px;">Search</label>
            </div>
            <div class="control-input-wrapper">
              <div class="control-input">
                <input type="text" autocomplete="off" class="input-with-feedback form-control" maxlength="140" data-fieldtype="Data" placeholder="Search by invoice id or customer name">
              </div>
              <div class="control-value like-disabled-input" style="display: none;">null</div>
              <p class="help-box small text-muted"></p>
            </div>
          </div>
        </div>
      </div>
      <div class="status-field">
        <div class="frappe-control input-max-width" data-fieldtype="Select">
          <div class="form-group">
            <div class="clearfix">
              <label class="control-label hide" style="padding-right: 0px;">Invoice Status</label>
            </div>
            <div class="control-input-wrapper">
              <div class="control-input flex align-center">
                <select type="text" autocomplete="off" class="input-with-feedback form-control ellipsis" maxlength="140" data-fieldtype="Select" placeholder="Filter by invoice status">
                  <option value="Draft">Draft</option>
                  <option value="Paid">Paid</option>
                  <option value="Consolidated">Consolidated</option>
                  <option value="Return">Return</option>
                </select>
                <div class="select-icon ">
                  <svg class="icon  icon-sm" style="">
                    <use class="" href="#icon-select"></use>
                  </svg>
                </div>
                <div class="placeholder ellipsis text-extra-muted " style="display: none;">
                  <span>Filter by invoice status</span>
                </div>
              </div>
              <div class="control-value like-disabled-input" style="display: none;">Draft</div>
              <p class="help-box small text-muted"></p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="invoices-container"></div>
  </section>
  <section class="past-order-summary">
    <div class="no-summary-placeholder"> Select an invoice to load summary data </div>
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
  </section>
</div>
`
frappe.pharmacy_page_body = {
  body: body,
  columns: ["Item", "Qty", "Rate", "Amount"],
  data: ["Bacitracin", 1, 10, 10]
}
