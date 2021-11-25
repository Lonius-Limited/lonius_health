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
	make:function() {
		let me =$(this)
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
	setupFields(){
		this.warehouse_select = this.page.add_inner_button('RMBH Pharmacy', () => new_post(), 'Select Warehouse')


		this.company_select = this.page.add_field({
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_default("company"),
			reqd: 1,
			change: (e) => {
				if(!e){
					return
				}
				this.options.selected_company = e.currentTarget.value;
				frappe.msgprint(this.options.selected_company)
				// this.make_request();
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
				if(!e){
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
				<span class="doctype-text" doctype-value="${item}">${ __(item) }</span>
			</a>
		</li>`);
	},
	
	

})
let body =`<div class="leaderboard page-main-content">
<div class="leaderboard-graph"></div>
<div class="leaderboard-list"></div>
</div>`;
frappe.pharmacy_page_body = {
	body: body
} 