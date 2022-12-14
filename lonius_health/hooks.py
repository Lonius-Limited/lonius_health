from . import __version__ as app_version

app_name = "lonius_health"
app_title = "Lonius Health"
app_publisher = "Lonius Limited Innovation"
app_description = "App for Lonius Limited"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@lonius.co.ke"
app_license = "MIT"


# fixtures = [d"Medical Code","Medical Code Standard"]
# after_migrate = [
# 	"lonius_health.api.invoices.close_patient_invoices",
# 	"lonius_health.after_migrate_functions.icd10.upload"
# ]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lonius_health/css/lonius_health.css"
app_include_js = [
	"/assets/lonius_health/js/client_scripts/patient.js",
	"/assets/lonius_health/js/client_scripts/patient_encounter.js",
	"/assets/lonius_health/js/client_scripts/clinical_procedure.js",
	"/assets/lonius_health/js/client_scripts/lab_test.js"
]
# app_include_js = [
#     "/assets/js/patient_scripts.min.js",
# ]

# include js, css files in header of web template
# web_include_css = "/assets/lonius_health/css/lonius_health.css"
# web_include_js = "/assets/lonius_health/js/lonius_health.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lonius_health/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "lonius_health.install.before_install"
# after_install = "lonius_health.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lonius_health.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
# OVERWRITE LAB TEST TEMPLATE FUNCTIONS
from erpnext.healthcare.doctype.lab_test_template.lab_test_template import (
    LabTestTemplate as _labTestTemplate,
)
from lonius_health.api.lab_tests import (
	lab_test_template_on_save as _lab_test_template_on_save,
	lab_test_template_price_exists as _lab_test_template_price_exists
)
_labTestTemplate.on_update = _lab_test_template_on_save
_labTestTemplate.item_price_exists = _lab_test_template_price_exists

# OVERWRITE CLINICAL PROCEDURE TEMPLATE FUNCTIONS
from erpnext.healthcare.doctype.clinical_procedure_template.clinical_procedure_template import (
    ClinicalProcedureTemplate as _clinicalProcedureTemplate,
)
from lonius_health.api.procedures import (
	procedure_template_after_insert as _procedure_template_after_insert
)
_clinicalProcedureTemplate.after_insert = _procedure_template_after_insert

doc_events = {
	"Patient Encounter" : {
		"on_submit" : ["lonius_health.api.lab_tests.create_lab_test",
				"lonius_health.api.procedures.create_procedure","lonius_health.api.patients.make_prescription"],
		"before_save" : ["lonius_health.api.encounter.update_queue_state"],
		"before_submit": ["lonius_health.api.encounter.update_queue_state"]
	},
	"Lab Test" : {
		"before_submit": ["lonius_health.api.invoices.append_lab_invoice"],
		"on_submit":["lonius_health.lonius_laboratory.api.lab_test.consolidated_lab_tests"],
		"on_update_after_submit":["lonius_health.lonius_laboratory.api.lab_test.consolidated_lab_tests"]
	},
	"Clinical Procedure" : {
		"before_submit" : ["lonius_health.api.invoices.append_procedure_invoice"]
	},
	"Vital Signs" : {
		"before_submit" : ["lonius_health.api.encounter.vitals_submitted_update_encounter"]
	},
	"Sales Invoice" : {
		"before_save" : ["lonius_health.api.invoices.validate_payment"]
	}
	# "Lab Test Template": {
	# 	"before_insert" : ["lonius_health.api.lab_tests.create_item_from_template"],
	# 	"after_insert" : ["lonius_health.api.lab_tests.match_templatename_with_testname"]
	# },
	# "Clinical Procedure Template": {
	# 	# "before_insert" : ["lonius_health.api.procedures.match_templatename_with_testname"],
	# 	"after_insert" : ["lonius_health.api.procedures.match_templatename_with_testname"]
	# }

}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lonius_health.tasks.all"
# 	],
# 	"daily": [
# 		"lonius_health.tasks.daily"
# 	],
# 	"hourly": [
# 		"lonius_health.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lonius_health.tasks.weekly"
# 	]
# 	"monthly": [
# 		"lonius_health.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "lonius_health.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lonius_health.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lonius_health.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lonius_health.auth.validate"
# ]

jenv = {
	"methods": [
		"get_consolidated_test:lonius_health.lonius_laboratory.api.lab_test.consolidated_lab_tests_endpoint"
	]
}
