import frappe
from frappe.desk.query_report import run
#lonius_health.lonius_laboratory.api.lab_test.consolidated_lab_tests
from frappe.utils import add_to_date, getdate,get_link_to_form, getdate, nowdate

@frappe.whitelist()
def consolidated_lab_tests_endpoint(docname):
	doc = frappe.get_doc("Lab Test", docname)
	return consolidated_lab_tests(doc, "endpoint")
def consolidated_lab_tests(doc, state):
	frappe.msgprint("Consolidating lab tests....")
	patient = doc.get('patient')
	report_name ='Lab Test Report'
	to_date = doc.get('creation').date()
	from_date=add_to_date(to_date,days=-1)#1 day or 24 hour report
	filters = dict(patient=patient,status='Completed',from_date=from_date, to_date=to_date)
	# result_date = doc.get('result_date')
	pl = run(report_name, filters, user="Administrator")
	res = pl.get('result')

	if not res : return "<em style='color:blue'>Sorry, no *Completed* results were found for the last 24 hours of the patient's encounter.</em>"
	data = [x for x in res if not isinstance(x,list)]

	text ="<h3 style='color:blue'>Consolidated Lab Test Results</h3><hr>"
	num = 0
	for row in data:
		num += 1
		l_doc  = frappe.get_doc('Lab Test', row.get('test'))
		test_name = l_doc.get("lab_test_name")
		comments = l_doc.get("lab_test_comment") or '-'
		requested_by = l_doc.get("practitioner_name") or  '-'
		posted_by = l_doc.get('employee_name') or '-'
		result_date = l_doc.get("result_date") or  ''
		result_time = l_doc.get("approved_date") or ''
		
		####Results
		normal_tests = l_doc.get("normal_test_items")
		t_results = get_normal_result_html(normal_tests)
		text += f"""
		<div class="card">
			<div class="card-header">
				<b>{num}.{test_name}</b>
			</div>
			<div class="card-body">
				<h5 class="card-title">Comments: {comments}</h5>
				
				<hr>
				{t_results}
			</div>
			<div class="card-footer text-muted">
				<em>Requesting Practitioner: {requested_by}</em>
				<em>Posted by: {posted_by} on {result_date} {result_time}</em>
			</div>
		</div><p style='text-align: center;'>-------------------------------------------------------------</p>
		"""
	if state =="endpoint":
		doc.db_set('consolidated_results',text)
	frappe.msgprint("Done")
	return text
	# doc.set('consolidated_results',text)
def get_normal_result_html(normal_test_items):#Lab Test Normal Items Child Table
	text = "<table class='table table-responsive table-striped'><thead><tr> <td><b>Test/Event</b></td> <td><b>Result/UOM</b></td> <td><b>Normal Range</b></td> </tr></thead>"
	text += "<tbody>"
	for row in normal_test_items:
		test_event,result_uom, normal_range = "{} {}".format(row.get("lab_test_name"), row.get("lab_test_event") or ''), "{} {}".format(row.get("result_value"),row.get("lab_test_uom") or ''), "{}".format(row.get("normal_range") or '')
		text += "<tr><td>{}</td> <td>{}</td> <td>{}</td>".format(test_event,result_uom, normal_range)
	text += "<tbody>"
	text += "</table>"
	return text


#Normal Test Result
# descriptive_tests = doc.get("descriptive_test_items")
# organism_tests = doc.get("normal_test_items")
# sensitivity_tests = doc.get("normal_test_items")
# normal_tests = doc.get("normal_test_items")
